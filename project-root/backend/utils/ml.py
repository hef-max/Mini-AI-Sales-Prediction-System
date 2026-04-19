import joblib
import numpy as np
import os
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

# ===== PATHS =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR = os.path.join(BASE_DIR, "..", "ml", "model")
MODEL_PATH = os.path.join(ML_DIR, "model.joblib")
SCALER_PATH = os.path.join(ML_DIR, "scaler.joblib")

# ===== GLOBAL MODEL & SCALER =====
MODEL = None
SCALER = None


def load_model():
    """
    Load ML model dan scaler dari disk
    
    Returns:
        Tuple of (model, scaler)
    
    Raises:
        FileNotFoundError: Jika model atau scaler tidak ditemukan
    """
    global MODEL, SCALER
    
    try:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        
        if not os.path.exists(SCALER_PATH):
            raise FileNotFoundError(f"Scaler file not found: {SCALER_PATH}")
        
        MODEL = joblib.load(MODEL_PATH)
        SCALER = joblib.load(SCALER_PATH)
        
        logger.info("Model dan scaler berhasil di-load")
        return MODEL, SCALER
    
    except FileNotFoundError as e:
        logger.error(f"Error loading model: {str(e)}")
        raise


def predict_status(jumlah_penjualan: int, harga: float, diskon: float) -> Tuple[str, float]:
    """
    Predict status produk (Laris / Tidak Laris)
    
    Args:
        jumlah_penjualan: Jumlah unit terjual
        harga: Harga satuan produk
        diskon: Diskon dalam persen (0-100)
    
    Returns:
        Tuple of (prediction_label, confidence_score)
    
    Raises:
        RuntimeError: Jika model belum di-load
        ValueError: Jika input tidak valid
    """
    if MODEL is None or SCALER is None:
        raise RuntimeError("Model belum di-load. Jalankan load_model() terlebih dahulu")
    
    # Validate input
    if jumlah_penjualan < 0 or harga < 0 or diskon < 0 or diskon > 100:
        raise ValueError("Input values tidak valid")
    
    try:
        # Prepare features
        features = np.array([[jumlah_penjualan, harga, diskon]])
        
        # Scale features menggunakan scaler yang sama saat training
        features_scaled = SCALER.transform(features)
        
        # Get prediction
        prediction = MODEL.predict(features_scaled)[0]
        
        # Get probability untuk confidence
        if hasattr(MODEL, 'predict_proba'):
            probabilities = MODEL.predict_proba(features_scaled)[0]
            confidence = float(np.max(probabilities))
        else:
            confidence = 0.0
        
        # Map prediction ke label
        label = "Laris" if prediction == 1 else "Tidak Laris"
        
        logger.info(f"Prediction: {label} (confidence: {confidence:.2f})")
        return label, confidence
    
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise


def is_model_loaded() -> bool:
    """
    Check apakah model sudah di-load
    
    Returns:
        True jika model sudah di-load, False sebaliknya
    """
    return MODEL is not None and SCALER is not None
