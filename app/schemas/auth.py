from pydantic import BaseModel, Field
from typing import Optional

class MobileInput(BaseModel):
    mobileNumber: str
    countryCode: str = "+91"

class OTPRequest(BaseModel):
    mobile_number: str = Field(..., description="Mobile number with country code, e.g., +919876543210")

class OTPVerify(BaseModel):
    mobileNumber: str
    otp: str
