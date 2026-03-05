import random
import logging
import httpx
import pytz
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from config import settings
from services.redis_service import redis_service

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def generate_otp(length: int = 4) -> str:
        """Generate a numeric OTP."""
        return "".join([str(random.randint(0, 9)) for _ in range(length)])

    async def send_sms_otp(self, mobile: str, message: str) -> bool:
        """Send OTP via SMS Country API"""
        try:
            url = f"https://restapi.smscountry.com/v0.1/Accounts/{settings.SMSCOUNTRY_AUTH_KEY}/SMSes/"
            
            payload = {
                "Text": message,
                "Number": mobile,
                "SenderId": settings.SMSCOUNTRY_SENDER_ID,
                "DRNotifyUrl": "",
                "DRNotifyHttpMethod": "POST",
                "Tool": "API"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=payload,
                    auth=(settings.SMSCOUNTRY_AUTH_KEY, settings.SMSCOUNTRY_AUTH_TOKEN),
                    headers={"Content-Type": "application/json"},
                    timeout=10.0
                )
                
                if response.status_code in [200, 202]:
                    logger.info(f"OTP sent successfully to {mobile}: {response.text}")
                    return True
                else:
                    logger.error(f"SMS Country API failed: {response.status_code} - {response.text}")
                    return False
        except Exception as e:
            logger.error(f"Failed to send SMS to {mobile}: {e}")
            return False

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(tz=pytz.utc) + expires_delta
        else:
            expire = datetime.now(tz=pytz.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def create_user_token(self, mobile_number: str, user_type: str, expires_delta: Optional[timedelta] = None):
        return self.create_access_token(
            data={"sub": mobile_number, "user_type": user_type},
            expires_delta=expires_delta
        )

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            return None

    async def initiate_otp(self, mobile: str) -> bool:
        """Generate, store, and send OTP."""
        otp = self.generate_otp()
        success = redis_service.set(f"otp:login:{mobile}", otp, ttl=settings.OTP_EXPIRE_SECONDS)
        if not success:
            return False
        
        msg = f"OTP for Login Transaction on CelebHub is {otp}. Do not share this OTP to anyone. -CelebHub"
        return await self.send_sms_otp(mobile.replace("+", ""), msg)

    def verify_otp(self, mobile: str, otp: str) -> bool:
        """Verify OTP against Redis."""
        stored_otp = redis_service.get(f"otp:login:{mobile}")
        if stored_otp and stored_otp == otp:
            redis_service.delete(f"otp:login:{mobile}")
            return True
        return False

auth_service = AuthService()
