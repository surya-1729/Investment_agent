"""
Authentication service for user management and JWT tokens
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.core.config import settings
from backend.models.user import User
from backend.schemas.user import UserCreate


class AuthService:
    """Service for handling authentication and user management"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[str]:
        """Verify a JWT token and return the username"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            if username is None:
                return None
            return username
        except JWTError:
            return None
    
    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password"""
        user = self.get_user_by_username(db, username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_user(self, db: Session, user_create: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        if self.get_user_by_username(db, user_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        if self.get_user_by_email(db, user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = self.get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            full_name=user_create.full_name,
            risk_tolerance=user_create.risk_tolerance,
            paper_trading=user_create.paper_trading,
            initial_balance=user_create.initial_balance
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user