import pandas as pd
import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

# ===== PATHS =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
CSV_PATH = os.path.join(DATA_DIR, "sales_data.csv")

# ===== GLOBAL DATA =====
SALES_DATA = None


def load_sales_data() -> pd.DataFrame:
    """
    Load sales data dari CSV file
    
    Returns:
        DataFrame dengan sales data
    
    Raises:
        FileNotFoundError: Jika CSV file tidak ditemukan
        Exception: Jika ada error saat membaca CSV
    """
    global SALES_DATA
    
    try:
        if not os.path.exists(CSV_PATH):
            raise FileNotFoundError(f"Sales data file not found: {CSV_PATH}")
        
        SALES_DATA = pd.read_csv(CSV_PATH)
        
        # Validate columns
        required_columns = ['product_id', 'product_name', 'jumlah_penjualan', 'harga', 'diskon', 'status']
        missing_columns = [col for col in required_columns if col not in SALES_DATA.columns]
        
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")
        
        logger.info(f"Sales data loaded successfully. Total rows: {len(SALES_DATA)}")
        return SALES_DATA
    
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error loading sales data: {str(e)}")
        raise


def get_all_sales() -> List[Dict]:
    """
    Get semua sales data sebagai list of dictionaries
    
    Returns:
        List of dicts dengan sales data
    
    Raises:
        RuntimeError: Jika data belum di-load
    """
    if SALES_DATA is None:
        raise RuntimeError("Sales data belum di-load. Jalankan load_sales_data() terlebih dahulu")
    
    try:
        # Convert DataFrame to list of dicts
        data = SALES_DATA.to_dict('records')
        logger.info(f"Retrieved {len(data)} sales records")
        return data
    
    except Exception as e:
        logger.error(f"Error retrieving sales data: {str(e)}")
        raise


def get_sales_by_product_id(product_id: str) -> Dict:
    """
    Get sales data untuk product tertentu
    
    Args:
        product_id: ID produk yang dicari
    
    Returns:
        Dict dengan data produk, atau None jika tidak ditemukan
    
    Raises:
        RuntimeError: Jika data belum di-load
    """
    if SALES_DATA is None:
        raise RuntimeError("Sales data belum di-load")
    
    try:
        product = SALES_DATA[SALES_DATA['product_id'] == product_id]
        
        if product.empty:
            return None
        
        return product.iloc[0].to_dict()
    
    except Exception as e:
        logger.error(f"Error retrieving product data: {str(e)}")
        raise


def is_data_loaded() -> bool:
    """
    Check apakah sales data sudah di-load
    
    Returns:
        True jika data sudah di-load, False sebaliknya
    """
    return SALES_DATA is not None


def get_data_summary() -> Dict:
    """
    Get summary statistics dari sales data
    
    Returns:
        Dict berisi summary data
    """
    if SALES_DATA is None:
        raise RuntimeError("Sales data belum di-load")
    
    return {
        "total_products": len(SALES_DATA),
        "laris_count": len(SALES_DATA[SALES_DATA['status'] == 'Laris']),
        "tidak_laris_count": len(SALES_DATA[SALES_DATA['status'] == 'Tidak']),
        "avg_penjualan": float(SALES_DATA['jumlah_penjualan'].mean()),
        "avg_harga": float(SALES_DATA['harga'].mean()),
        "avg_diskon": float(SALES_DATA['diskon'].mean())
    }
