from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status

# ===== CONFIG =====
SECRET_KEY = '_5#y2L"F4Q8z\n\xec]//'  # DUMMY, change ini di production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ===== DUMMY USER DATABASE =====
DUMMY_USERS = {
    "admin": "password123",
    "user": "user123",
    "hefri": "hefri123"
}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create JWT token
    
    Args:
        data: Data yang mau di-encode ke token
        expires_delta: Durasi token expiry (opsional)
    
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify JWT token dan return payload
    
    Args:
        token: JWT token dari header
    
    Returns:
        Token payload (dict)
    
    Raises:
        HTTPException: Jika token tidak valid atau expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tidak valid",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {"username": username}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate user dengan username dan password
    
    Args:
        username: Username dari request
        password: Password dari request
    
    Returns:
        True jika credentials valid, False sebaliknya
    """
    if username not in DUMMY_USERS:
        return False
    
    return DUMMY_USERS[username] == password
