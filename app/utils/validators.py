import re
from datetime import date, datetime
from typing import Optional
from pathlib import Path

from exceptions import ValidationException
from config import settings


class Validators:
    """Collection of input validators"""
    
    @staticmethod
    def validate_mobile_number(mobile: str, country_code: str = "+91") -> str:
        """
        Validate mobile number format.
        Returns formatted mobile number.
        """
        # Remove spaces and special characters
        clean_mobile = re.sub(r'[^\d+]', '', mobile)
        
        # Check if starts with country code
        if not clean_mobile.startswith(country_code):
            clean_mobile = country_code + clean_mobile
        
        # Validate format: +XX followed by 10 digits
        pattern = r'^\+\d{1,3}\d{10}$'
        if not re.match(pattern, clean_mobile):
            raise ValidationException(
                "Invalid mobile number format. Must be +CCXXXXXXXXXX (10 digits after country code)"
            )
        
        return clean_mobile
    @staticmethod
    def validate_email(email: str) -> str:
        """Validate email format"""
        email = email.strip().lower()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            raise ValidationException("Invalid email format")
        
        return email
    
    @staticmethod
    def validate_password(password: str) -> None:
        """
        Validate password strength.
        Requirements: 8+ chars, uppercase, lowercase, digit, special char
        """
        if len(password) < 8:
            raise ValidationException("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', password):
            raise ValidationException("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            raise ValidationException("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            raise ValidationException("Password must contain at least one digit")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationException("Password must contain at least one special character")

    @staticmethod
    def validate_gender(gender: str) -> str:
        """Validate gender value"""
        gender = gender.upper().strip()
        if gender not in ['M', 'F']:
            raise ValidationException("Gender must be 'M' or 'F'")
        return gender

    @staticmethod
    def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize string input.
        Removes leading/trailing whitespace and validates length.
        """
        text = text.strip()
        
        if not text:
            raise ValidationException("Input cannot be empty")
        
        if max_length and len(text) > max_length:
            raise ValidationException(f"Input exceeds maximum length of {max_length} characters")
        
        return text
