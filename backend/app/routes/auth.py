"""
AgroGrade AI - Authentication Routes
Complete login and user management system
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
import sqlite3
from pathlib import Path
import uuid

# Configuration
router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = "agrograde-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup
DB_PATH = Path(__file__).parent.parent.parent / "agrograde_users.db"

class UserCreate(BaseModel):
    """User registration model"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
    farm_name: Optional[str] = None

class UserLogin(BaseModel):
    """User login model"""
    username: str
    password: str

class Token(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str
    expires_in: int
    user: Dict[str, Any]

class UserResponse(BaseModel):
    """User information response"""
    id: str
    username: str
    email: str
    full_name: Optional[str]
    farm_name: Optional[str]
    created_at: str
    is_active: bool

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                farm_name TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        """)
        conn.commit()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT * FROM users WHERE username = ? AND is_active = 1",
            (username,)
        )
        user = cursor.fetchone()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    return dict(user)

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    """Register a new user"""
    init_db()
    
    # Check if user already exists
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT id FROM users WHERE username = ? OR email = ?",
            (user.username, user.email)
        )
        existing_user = cursor.fetchone()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )
    
    # Create new user
    user_id = str(uuid.uuid4())
    password_hash = get_password_hash(user.password)
    
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO users (id, username, email, password_hash, full_name, farm_name)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, user.username, user.email, password_hash, user.full_name, user.farm_name)
        )
        conn.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Get user info
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT id, username, email, full_name, farm_name, created_at FROM users WHERE id = ?",
            (user_id,)
        )
        user_data = dict(cursor.fetchone())
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user_data
    }

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    """Login user and return access token"""
    init_db()
    
    # Verify user credentials
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT * FROM users WHERE username = ? AND is_active = 1",
            (user.username,)
        )
        db_user = cursor.fetchone()
        
        if db_user is None or not verify_password(user.password, db_user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    # Update last login
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?",
            (db_user["id"],)
        )
        conn.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user["username"]}, expires_delta=access_token_expires
    )
    
    # Get user info
    user_data = {
        "id": db_user["id"],
        "username": db_user["username"],
        "email": db_user["email"],
        "full_name": db_user["full_name"],
        "farm_name": db_user["farm_name"],
        "created_at": db_user["created_at"]
    }
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user": user_data
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(**current_user)

@router.post("/logout")
async def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Logout user (token invalidation would be handled client-side)"""
    return {"message": "Successfully logged out"}

@router.put("/profile")
async def update_profile(
    full_name: Optional[str] = None,
    farm_name: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update user profile"""
    with get_db() as conn:
        conn.execute(
            """
            UPDATE users 
            SET full_name = COALESCE(?, full_name),
                farm_name = COALESCE(?, farm_name)
            WHERE id = ?
            """,
            (full_name, farm_name, current_user["id"])
        )
        conn.commit()
    
    return {"message": "Profile updated successfully"}

@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Change user password"""
    # Verify current password
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT password_hash FROM users WHERE id = ?",
            (current_user["id"],)
        )
        user_data = cursor.fetchone()
        
        if not verify_password(current_password, user_data["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
    
    # Update password
    new_password_hash = get_password_hash(new_password)
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (new_password_hash, current_user["id"])
        )
        conn.commit()
    
    return {"message": "Password changed successfully"}

# Initialize database on import
init_db()
