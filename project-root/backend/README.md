# Quick Start Guide

## Prerequisites

- Python 3.11+
- pip
- Virtual environment (recommended)

## 1. Setup Environment

```bash
# Navigate ke project
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Prepare Required Files

**Create these directories:**
```bash
mkdir -p data backend/ml
```

**Copy/place these files:**
- `data/sales_data.csv` - Sales data file
- `backend/ml/model.joblib` - Trained ML model
- `backend/ml/scaler.joblib` - Feature scaler

## 4. Run Backend

```bash
python -m backend.main
```

Or dengan hot reload:
```bash
uvicorn backend.main:app --reload
```

**Server akan run di:** `http://localhost:8000`

## 5. Test API

### Quick Test dengan cURL

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}' | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

echo "Your token: $TOKEN"

# 2. Get Sales
curl -X GET http://localhost:8000/api/sales/ \
  -H "Authorization: Bearer $TOKEN"

# 3. Predict
curl -X POST http://localhost:8000/api/predict/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jumlah_penjualan":120,"harga":4500000,"diskon":8}'
```

### Using Postman

1. Open Postman
2. Import this collection (JSON):

```json
{
  "info": {
    "name": "AI Sales Prediction API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Login",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/auth/login",
        "body": {
          "mode": "raw",
          "raw": "{\"username\":\"admin\",\"password\":\"password123\"}"
        }
      }
    },
    {
      "name": "Get Sales",
      "request": {
        "method": "GET",
        "url": "http://localhost:8000/api/sales/",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{token}}",
            "type": "text"
          }
        ]
      }
    },
    {
      "name": "Predict",
      "request": {
        "method": "POST",
        "url": "http://localhost:8000/api/predict/",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer {{token}}",
            "type": "text"
          },
          {
            "key": "Content-Type",
            "value": "application/json",
            "type": "text"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"jumlah_penjualan\":120,\"harga\":4500000,\"diskon\":8}"
        }
      }
    }
  ]
}
```

## 6. API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## File Structure

```
backend_project/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # Main application
│   ├── models.py               # Pydantic schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py            # Login endpoint
│   │   ├── sales.py           # Sales endpoints
│   │   └── predict.py         # Prediction endpoint
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth.py            # JWT utilities
│   │   ├── data.py            # CSV loading
│   │   └── ml.py              # ML prediction
├── ml/                        # Machine learning files
│   ├── Training_model.ipynb   # Notebook untuk pelatihan model
│   └── model/                 # Serialized model artifacts
│       ├── model.joblib       # Trained classification model
│       └── scaler.joblib      # Feature scaler
├── data/
│   └── sales_data.csv         # (Copy dari study case)
├── requirements.txt           # Python dependencies
├── README.md                  # Full documentation
├── SETUP.md                   # This file
└── .gitignore                 # Git ignore rules
```

## Dummy Credentials

| Username | Password |
|----------|----------|
| admin | password123 |
| user | user123 |
| hefri | hefri123 |

## Troubleshooting

### Port 8000 already in use

```bash
# Kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -i :8000
kill -9 <PID>
```

### Module not found error

```bash
# Make sure virtual environment is activated
# Check if dependencies installed properly
pip list

# Reinstall if needed
pip install -r requirements.txt --force-reinstall
```

### Model/Scaler not found

Make sure files exist:
```bash
ls -la backend/ml/
# Should show: model.joblib, scaler.joblib
```

## Development Tips

1. **Keep venv activated** selama development
2. **Use reload mode** untuk faster iteration: `uvicorn backend.main:app --reload`
3. **Check logs** di `backend.log` untuk debugging
4. **Test endpoints** di Swagger UI (`/docs`) untuk interactive testing
5. **Monitor startup logs** di console untuk check if model/data loaded successfully

## Next: ML Pipeline

Setelah backend siap, kerjakan ML pipeline untuk generate:
- `backend/ml/model.joblib`
- `backend/ml/scaler.joblib`

ML pipeline akan:
1. Load `data/sales_data.csv`
2. Preprocess data (normalize dengan StandardScaler)
3. Train classification model
4. Save model & scaler dengan joblib

---

**Ready to code!** 🚀
