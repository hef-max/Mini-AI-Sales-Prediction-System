from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import sys

# Import routes
from backend.routes import auth, sales, predict
from backend.utils.data import load_sales_data
from backend.utils.ml import load_model

# ===== LOGGING SETUP =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # tanpa encoding
        logging.FileHandler('backend/backend.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


# ===== STARTUP & SHUTDOWN HANDLERS =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup dan shutdown event handler
    
    Startup:
    - Load sales data dari CSV
    - Load ML model dan scaler
    
    Shutdown:
    - Log shutdown
    """
    # STARTUP
    logger.info("=" * 50)
    logger.info("Starting FastAPI application...")
    
    try:
        logger.info("Loading sales data...")
        load_sales_data()
        logger.info("✓ Sales data loaded successfully")
    except Exception as e:
        logger.error(f"✗ Error loading sales data: {str(e)}")
        logger.warning("Application will continue but GET /api/sales will fail")
    
    try:
        logger.info("Loading ML model and scaler...")
        load_model()
        logger.info("✓ ML model and scaler loaded successfully")
    except Exception as e:
        logger.error(f"✗ Error loading ML model: {str(e)}")
        logger.warning("Application will continue but POST /api/predict will fail")
    
    logger.info("Application startup complete!")
    logger.info("=" * 50)
    
    yield
    
    # SHUTDOWN
    logger.info("=" * 50)
    logger.info("Shutting down FastAPI application...")
    logger.info("Goodbye!")
    logger.info("=" * 50)


# ===== CREATE FASTAPI APP =====
app = FastAPI(
    title="AI Sales Prediction System API",
    description="REST API untuk prediksi status penjualan produk menggunakan Machine Learning",
    version="1.0.0",
    lifespan=lifespan
)

# ===== CORS MIDDLEWARE =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change ini ke specific origins di production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== INCLUDE ROUTERS =====
app.include_router(auth.router)
app.include_router(sales.router)
app.include_router(predict.router)


# ===== ROOT ENDPOINT =====
@app.get("/",
         tags=["Root"])
def root():
    """
    Root endpoint untuk check API status
    
    Returns:
    - message: Welcome message
    - documentation: Link ke API documentation
    """
    return {
        "message": "AI Sales Prediction System API",
        "version": "1.0.0",
        "documentation": "/docs",
        "redoc_documentation": "/redoc",
        "openapi_schema": "/openapi.json"
    }


@app.get("/health",
         tags=["Health"])
def health_check():
    """
    Health check endpoint
    
    Returns:
    - status: "ok" jika API berjalan
    """
    return {
        "status": "ok",
        "message": "API is running"
    }


# ===== ERROR HANDLERS =====
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    General exception handler untuk error yang tidak tertangani
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return {
        "error": "Internal Server Error",
        "detail": str(exc),
        "status_code": 500
    }


# ===== RUN COMMAND =====
if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting uvicorn server...")
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
