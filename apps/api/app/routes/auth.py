"""
Authentication Routes
User authentication and authorization endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

router = APIRouter()
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    """User creation model."""
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login model."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response model."""
    id: str
    email: str
    full_name: Optional[str]
    created_at: datetime
    is_active: bool


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponse


@router.post("/register", response_model=TokenResponse)
async def register_user(user_data: UserCreate):
    """Register a new user account."""
    # Placeholder implementation
    # In production, this would:
    # 1. Validate email is not already registered
    # 2. Hash the password
    # 3. Create user in database
    # 4. Generate JWT token
    
    settings = get_settings()
    
    # Mock user creation
    user = UserResponse(
        id="user_123",
        email=user_data.email,
        full_name=user_data.full_name,
        created_at=datetime.now(),
        is_active=True,
    )
    
    # Generate mock JWT token
    token_data = {
        "sub": user.id,
        "email": user.email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    
    access_token = jwt.encode(
        token_data, 
        settings.SECRET_KEY, 
        algorithm="HS256"
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=86400,  # 24 hours
        user=user,
    )


@router.post("/login", response_model=TokenResponse)
async def login_user(credentials: UserLogin):
    """Authenticate user and return access token."""
    # Placeholder implementation
    # In production, this would:
    # 1. Verify user exists in database
    # 2. Check password hash
    # 3. Generate JWT token
    
    settings = get_settings()
    
    # Mock user authentication
    if credentials.email == "demo@spectraai.com" and credentials.password == "demo123":
        user = UserResponse(
            id="user_demo",
            email=credentials.email,
            full_name="Demo User",
            created_at=datetime.now(),
            is_active=True,
        )
        
        # Generate JWT token
        token_data = {
            "sub": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        }
        
        access_token = jwt.encode(
            token_data, 
            settings.SECRET_KEY, 
            algorithm="HS256"
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=86400,
            user=user,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user information."""
    try:
        settings = get_settings()
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        
        # Mock user retrieval
        user = UserResponse(
            id=payload["sub"],
            email=payload["email"],
            full_name="Demo User",
            created_at=datetime.now(),
            is_active=True,
        )
        
        return user
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


@router.post("/logout")
async def logout_user():
    """Logout user (placeholder for token blacklisting)."""
    return {"message": "Successfully logged out"}


@router.post("/refresh")
async def refresh_token(token: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh access token."""
    # Placeholder implementation
    # In production, this would validate the refresh token
    # and generate a new access token
    
    settings = get_settings()
    
    try:
        payload = jwt.decode(token.credentials, settings.SECRET_KEY, algorithms=["HS256"])
        
        # Generate new token with extended expiry
        new_token_data = {
            "sub": payload["sub"],
            "email": payload["email"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        }
        
        new_access_token = jwt.encode(
            new_token_data, 
            settings.SECRET_KEY, 
            algorithm="HS256"
        )
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 86400,
        }
        
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
