from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from typing import Optional
import logging
import httpx
from datetime import timedelta

from config import settings
from database import get_db
from schemas.auth import MobileInput, OTPVerify
from services.auth_service import auth_service
from services.redis_service import redis_service
from repositories.user_repository import UserRepository, SessionRepository
from utils.security import SecurityUtils
from utils.validators import Validators
from exceptions import ForbiddenException, ValidationException
from utils.responses import success_response

logger = logging.getLogger(__name__)
router = APIRouter()
security_auth_router = HTTPBearer(auto_error=False)


async def send_sms_country_otp(mobile: str, message: str) -> bool:
    """Send OTP via SMS Country API"""
    return await auth_service.send_sms_otp(mobile, message)
    
@router.post("/send-otp")
async def send_otp(
    data: MobileInput, 
    db: Session = Depends(get_db), 
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_auth_router)
):
    """
    Send OTP to mobile number.
    Validates phone number and initiates verification.
    """
    try:
        
        mobile= Validators.validate_mobile_number(data.mobileNumber, data.countryCode)
       

        # Bypass OTP for test numbers
        if mobile in ["+910987654321", "+911234567890", "+911111111111"]:
            redis_service.set(f"otp:login:{mobile}", "1234", ttl=600)
            return success_response(data=[], message="OTP sent successfully")

        user_repo = UserRepository(db)
        user_data = user_repo.get_by_mobile(mobile)

        if user_data:
            if not user_data.is_active:
                raise ForbiddenException(
                    "User account is inactive. Contact administrator."
                )

        # Generate 4-digit OTP
        otp = SecurityUtils.generate_otp(length=4)
        
        text_msg = f"OTP for Login Transaction on celeqthor is {otp}. Do not share this OTP to anyone. -MySira Labs"

        sms_sent = await send_sms_country_otp(mobile.replace("+", ""), text_msg)

        if not sms_sent:
            raise ValidationException("Failed to send OTP. Please try again.")
        
        # Store OTP in Redis with 10 minute expiry
        redis_service.set(f"otp:login:{mobile}", otp, ttl=600)

        return success_response(data=[], message="OTP sent successfully")

    except (ValidationException, ForbiddenException) as e:
        raise e
    except Exception as e:
        logger.error(f"Error in send_otp: {e}")
        raise ValidationException(f"Unable to send OTP: {str(e)}")


@router.post("/verify-otp")
def verify_otp(
    data: OTPVerify,
    db: Session = Depends(get_db)
):
    """
    Verify OTP and return access token.
    Creates session if user exists, returns new user token otherwise.
    """
    # Validate mobile number format
    mobile= Validators.validate_mobile_number(data.mobileNumber,"+91")
    

    # Verify OTP from Redis
    stored_otp = redis_service.get(f"otp:login:{mobile}")
    
    if not stored_otp or stored_otp != data.otp:
        raise ValidationException("Invalid or expired OTP")
    
    # Delete OTP after successful verification
    redis_service.delete(f"otp:login:{mobile}")

    user_repo = UserRepository(db)
    user_data = user_repo.get_by_mobile(mobile)

    if user_data:
        # Existing user - check if active
        if not user_data.is_active:
            raise ForbiddenException(
                "User account is inactive. Contact administrator."
            )

        # Generate token for existing user
        user_type = user_data.user_type or 'actor'  # Default to actor if not set

        token = auth_service.create_user_token(
            mobile_number=mobile,
            user_type=user_type,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        # Create/update session
        session_repo = SessionRepository(db)
        session_repo.create_session(mobile, token)

        # We need to serialize user_info for response
        user_details = {
            "id": user_data.id,
            "mobile_number": user_data.mobile_number,
            "user_type": user_data.user_type
        }

        return success_response( 
            data={"userExists": True, "details": user_details, "token": token},
            message="OTP verified successfully",
        )
 
    else:
        # New user - generate temporary token
        token = auth_service.create_access_token(
            data={"sub": mobile},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return success_response(
            data={"userExists": False, "details": None, "token": token},
            message="OTP verified successfully",
        )
