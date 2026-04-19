from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ===== AUTH MODELS =====
class LoginRequest(BaseModel):
    """Model untuk login request"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "password123"
            }
        }


class TokenResponse(BaseModel):
    """Model untuk JWT token response"""
    access_token: str
    token_type: str
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "message": "Login berhasil"
            }
        }


# ===== SALES DATA MODELS =====
class SalesDataResponse(BaseModel):
    """Model untuk response sales data"""
    product_id: str
    product_name: str
    jumlah_penjualan: int
    harga: float
    diskon: float
    status: str

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "P00001",
                "product_name": "Laptop",
                "jumlah_penjualan": 150,
                "harga": 5000000,
                "diskon": 10,
                "status": "Laris"
            }
        }


class AllSalesResponse(BaseModel):
    """Model untuk response semua sales data"""
    total_products: int
    data: List[SalesDataResponse]
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "total_products": 10,
                "data": [
                    {
                        "product_id": "P00001",
                        "product_name": "Laptop",
                        "jumlah_penjualan": 150,
                        "harga": 5000000,
                        "diskon": 10,
                        "status": "Laris"
                    }
                ],
                "message": "Data berhasil diambil"
            }
        }


# ===== PREDICTION MODELS =====
class PredictRequest(BaseModel):
    """Model untuk prediction request"""
    jumlah_penjualan: int
    harga: float
    diskon: float

    class Config:
        json_schema_extra = {
            "example": {
                "jumlah_penjualan": 120,
                "harga": 4500000,
                "diskon": 8
            }
        }


class PredictionResponse(BaseModel):
    """Model untuk prediction response"""
    prediction: str  # "Laris" atau "Tidak Laris"
    confidence: float
    input_data: PredictRequest
    message: str

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "Laris",
                "confidence": 0.87,
                "input_data": {
                    "jumlah_penjualan": 120,
                    "harga": 4500000,
                    "diskon": 8
                },
                "message": "Prediksi berhasil"
            }
        }


# ===== ERROR RESPONSE =====
class ErrorResponse(BaseModel):
    """Model untuk error response"""
    error: str
    detail: str
    status_code: int

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Unauthorized",
                "detail": "Token tidak valid",
                "status_code": 401
            }
        }
