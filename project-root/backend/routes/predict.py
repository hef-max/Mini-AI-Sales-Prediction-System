from fastapi import APIRouter, status, HTTPException, Depends, Header
from typing import Optional
from backend.models import PredictRequest, PredictionResponse, ErrorResponse
from backend.utils.ml import predict_status, is_model_loaded
from backend.utils.auth import verify_token
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/predict", tags=["Prediction"])


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


@router.post("/",
             response_model=PredictionResponse,
             status_code=status.HTTP_200_OK,
             responses={
                 400: {"model": ErrorResponse, "description": "Invalid input"},
                 401: {"model": ErrorResponse, "description": "Unauthorized"},
                 500: {"model": ErrorResponse, "description": "Server error"}
             })
def predict(request: PredictRequest, current_user: dict = Depends(get_current_user)):
    """
    Endpoint untuk prediksi status produk (Laris / Tidak Laris)
    
    **Requires:**
    - Authorization header dengan JWT token (format: "Bearer <token>")
    
    **Input:**
    - jumlah_penjualan: Jumlah unit yang terjual (integer)
    - harga: Harga satuan produk dalam rupiah (float)
    - diskon: Diskon dalam persen, 0-100 (float)
    
    **Returns:**
    - prediction: "Laris" atau "Tidak Laris"
    - confidence: Score kepercayaan prediksi (0.0 - 1.0)
    - input_data: Data input yang digunakan
    - message: Response message
    
    **Example:**
    ```
    POST /api/predict
    Headers:
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    
    Body:
    {
        "jumlah_penjualan": 120,
        "harga": 4500000,
        "diskon": 8
    }
    ```
    """
    
    try:
        # Check apakah model sudah di-load
        if not is_model_loaded():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Model ML belum di-load. Hubungi administrator."
            )
        
        # Validate input range
        if request.jumlah_penjualan < 0 or request.harga < 0 or request.diskon < 0 or request.diskon > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input values tidak valid. Pastikan jumlah_penjualan >= 0, harga >= 0, dan 0 <= diskon <= 100"
            )
        
        # Perform prediction
        prediction, confidence = predict_status(
            request.jumlah_penjualan,
            request.harga,
            request.diskon
        )
        
        logger.info(f"User {current_user['username']} melakukan prediksi: {prediction} (confidence: {confidence:.2f})")
        
        return PredictionResponse(
            prediction=prediction,
            confidence=round(confidence, 4),
            input_data=request,
            message=f"Prediksi berhasil. Produk diprediksi {prediction} dengan confidence {confidence:.2%}"
        )
    
    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Validation error dari user {current_user['username']}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Input error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Terjadi error saat prediksi: {str(e)}"
        )


@router.get("/health",
            status_code=status.HTTP_200_OK)
def health_check():
    """
    Endpoint untuk check apakah model dan data sudah siap
    
    **Returns:**
    - model_loaded: Status model ML
    - data_loaded: Status sales data
    - status: "ready" atau "not ready"
    """
    
    return {
        "model_loaded": is_model_loaded(),
        "status": "ready" if is_model_loaded() else "not ready",
        "message": "Model ML siap untuk prediksi" if is_model_loaded() else "Model ML belum di-load"
    }
