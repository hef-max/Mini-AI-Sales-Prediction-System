from fastapi import APIRouter, status, HTTPException
from backend.models import LoginRequest, TokenResponse, ErrorResponse
from backend.utils.auth import authenticate_user, create_access_token
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", 
             response_model=TokenResponse,
             status_code=status.HTTP_200_OK,
             responses={
                 400: {"model": ErrorResponse, "description": "Invalid credentials"},
                 500: {"model": ErrorResponse, "description": "Server error"}
             })

def login(credentials: LoginRequest):
    """
    Endpoint untuk login dan mendapatkan JWT token
    
    **Dummy users yang tersedia:**
    - username: `admin`, password: `password123`
    - username: `user`, password: `user123`
    - username: `hefri`, password: `hefri123`
    
    **Returns:**
    - access_token: JWT token yang bisa digunakan di header Authorization
    - token_type: Selalu "bearer"
    """
    
    try:
        # Authenticate user
        if not authenticate_user(credentials.username, credentials.password):
            logger.warning(f"Login attempt failed untuk user: {credentials.username}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username atau password salah"
            )
        
        # Create token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": credentials.username},
            expires_delta=access_token_expires
        )
        
        logger.info(f"User {credentials.username} login berhasil")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            message=f"Login berhasil untuk user {credentials.username}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Terjadi error saat login"
        )
