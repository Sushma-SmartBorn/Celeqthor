from sqlalchemy.orm import Session
from models import User, UserSession
from typing import Optional, Dict, Any

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_mobile(self, mobile: str) -> Optional[User]:
        """Fetch user info by mobile number."""
        return self.db.query(User).filter(User.mobile_number == mobile).first()

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, mobile: str, token: str):
        """Create or update user session."""
        session = self.db.query(UserSession).filter(UserSession.mobile_number == mobile).first()
        if session:
            session.session_token = token
            session.is_active = True
        else:
            session = UserSession(mobile_number=mobile, session_token=token)
            self.db.add(session)
        self.db.commit()
        return session
