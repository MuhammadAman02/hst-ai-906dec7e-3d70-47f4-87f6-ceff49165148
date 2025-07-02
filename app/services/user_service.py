"""User service for user management"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from app.models.user import User
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import UserNotFoundError

class UserService:
    """Service for user-related operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, email: str, username: str, password: str) -> User:
        """Create a new user"""
        hashed_password = get_password_hash(password)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        query = select(User).where(User.email == email)
        return self.db.execute(query).scalar_one_or_none()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        query = select(User).where(User.username == username)
        return self.db.execute(query).scalar_one_or_none()
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.get_user_by_email(email)
        if user and verify_password(password, user.hashed_password):
            return user
        return None
    
    def get_user(self, user_id: int) -> User:
        """Get user by ID"""
        user = self.db.get(User, user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user