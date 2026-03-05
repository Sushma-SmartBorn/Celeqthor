import random

class SecurityUtils:
    @staticmethod
    def generate_otp(length: int = 4) -> str:
        """Generate a numeric OTP."""
        return "".join([str(random.randint(0, 9)) for _ in range(length)])
