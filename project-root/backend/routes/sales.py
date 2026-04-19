from fastapi import APIRouter, status, HTTPException, Depends, Header
from typing import Optional
from backend.models import AllSalesResponse, SalesDataResponse, ErrorResponse
from backend.utils.data import get_all_sales, is_data_loaded, get_data_summary
from backend.utils.auth import verify_token
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/sales", tags=["Sales Data"])


def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Dependency untuk verify JWT token dari Authorization header
    
    Args:
        authorization: Authorization header dalam format "Bearer <token>"
    
    Returns:
        Dict dengan username dari token
    
    Raises:
        HTTPException: Jika token tidak valid
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = verify_token(token)
        return user
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/",
            response_model=AllSalesResponse,
            status_code=status.HTTP_200_OK,
            responses={
                401: {"model": ErrorResponse, "description": "Unauthorized"},
                500: {"model": ErrorResponse, "description": "Server error"}
            })
def get_sales(current_user: dict = Depends(get_current_user)):
    """
    Endpoint untuk mendapatkan semua sales data
    
    **Requires:**
    - Authorization header dengan JWT token (format: "Bearer <token>")
    
    **Returns:**
    - total_products: Jumlah produk
    - data: List dari sales records
    - message: Response message
    
    **Example:**
    ```
    GET /api/sales
    Headers:
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    ```
    """
    
    try:
        if not is_data_loaded():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Sales data belum di-load"
            )
        
        sales_data = get_all_sales()
        summary = get_data_summary()
        
        logger.info(f"User {current_user['username']} mengakses sales data")
        
        return AllSalesResponse(
            total_products=len(sales_data),
            data=sales_data,
            message=f"Sales data berhasil diambil. Total {len(sales_data)} produk. Laris: {summary['laris_count']}, Tidak Laris: {summary['tidak_laris_count']}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting sales data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi error saat mengambil data: {str(e)}"
        )


@router.get("/summary",
            status_code=status.HTTP_200_OK,
            responses={
                401: {"model": ErrorResponse, "description": "Unauthorized"},
                500: {"model": ErrorResponse, "description": "Server error"}
            })
def get_sales_summary(current_user: dict = Depends(get_current_user)):
    """
    Endpoint untuk mendapatkan summary statistics dari sales data
    
    **Requires:**
    - Authorization header dengan JWT token
    
    **Returns:**
    - total_products: Total jumlah produk
    - laris_count: Jumlah produk yang laris
    - tidak_laris_count: Jumlah produk yang tidak laris
    - avg_penjualan: Rata-rata jumlah penjualan
    - avg_harga: Rata-rata harga
    - avg_diskon: Rata-rata diskon
    """
    
    try:
        if not is_data_loaded():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Sales data belum di-load"
            )
        
        summary = get_data_summary()
        
        logger.info(f"User {current_user['username']} mengakses sales summary")
        
        return {
            **summary,
            "message": "Summary data berhasil diambil"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting sales summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi error: {str(e)}"
        )
