# Frontend Setup - Quick Start

Panduan cepat untuk run React frontend locally.

## Prerequisites

- Node.js 16+ (download dari nodejs.org)
- npm (comes with Node.js)
- Backend running di `http://localhost:8000`

## 1. Install Dependencies

```bash
cd frontend
npm install
```

Ini akan install semua dependencies dari package.json:
- react, react-dom
- axios
- bootstrap

**Durasi**: 1-2 menit (tergantung internet speed)

## 2. Check Backend Running

```bash
# Verify backend API is up
curl http://localhost:8000/

# Expected response:
# {"message": "AI Sales Prediction System API", ...}
```

Jika error, start backend terlebih dahulu:
```bash
cd ../backend_project
python -m backend.main
```

## 3. Start Frontend Dev Server

```bash
npm run dev
```

**Output:**
```
VITE v5.0.0  ready in 350 ms

➜  Local:   http://localhost:3000/
➜  press h to show help
```

Frontend sekarang running di `http://localhost:3000`

## 4. Access Application

1. Open browser: `http://localhost:3000`
2. Login page akan appear
3. Enter credentials:
   - Username: `admin`
   - Password: `password123`
4. Click "Login"
5. Dashboard akan load dengan 2 tabs:
   - 📊 Data Penjualan
   - 🔮 Prediksi

## Usage

### Tab 1: Data Penjualan

- View semua products dalam tabel
- See summary: total, laris count, tidak laris count
- Click "Refresh" untuk update data

### Tab 2: Prediksi

- Input jumlah penjualan, harga, diskon
- Click "Lakukan Prediksi"
- Result modal akan pop-up showing:
  - Prediction (Laris atau Tidak Laris)
  - Confidence score
  - Input data recap

## Common Issues

### Port 3000 already in use

Jika error "Port 3000 already in use":

```bash
# Find process using port 3000
lsof -i :3000

# Kill process
kill -9 <PID>

# Try again
npm run dev
```

### Backend not responding

If error "Cannot connect to backend":

1. Check backend running:
   ```bash
   curl http://localhost:8000/
   ```

2. If not running, start in separate terminal:
   ```bash
   cd ../backend_project
   python -m backend.main
   ```

3. Verify API_BASE_URL in `src/utils/api.js` is correct

### Dependencies install error

```bash
# Clear cache
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### CORS Error

If you see CORS error:
- Make sure backend running at `http://localhost:8000`
- Check backend CORS settings allow `http://localhost:3000`

## Build for Production

```bash
npm run build
```

Creates optimized `dist/` folder ready for deployment.

## Stop Development Server

Press `Ctrl+C` in terminal running `npm run dev`

## File Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── LoginPage.jsx        # Login form page
│   │   └── Dashboard.jsx        # Main dashboard
│   ├── components/
│   │   ├── SalesTable.jsx       # Sales data table
│   │   ├── PredictionForm.jsx   # Prediction form
│   │   └── PredictionResult.jsx # Result modal
│   ├── utils/
│   │   └── api.js              # API service + token mgmt
│   ├── styles/
│   │   ├── App.css             # Global styles
│   │   ├── LoginPage.css       # Login styles
│   │   └── PredictionResult.css # Modal styles
│   ├── App.jsx                 # Main app
│   └── main.jsx                # React entry
├── index.html                  # HTML entry
├── vite.config.js              # Build config
├── package.json                # Dependencies
└── README.md                   # Full docs
```

## Next

- Explore the application
- Test with different inputs
- Check DevTools Network tab untuk see API calls
- Review code for learning

## Troubleshoot Commands

```bash
# Check Node version
node --version

# Check npm version
npm --version

# Clear npm cache
npm cache clean --force

# Check if backend API accessible
curl http://localhost:8000/health

# View recent npm logs
npm logs
```

## Tips

1. **Keep both running**: Terminal 1 = backend, Terminal 2 = frontend
2. **Check console**: F12 → Console untuk see any JavaScript errors
3. **Check network**: F12 → Network untuk see API calls
4. **Reload page**: Ctrl+R jika ada strange behavior
5. **Clear cache**: Ctrl+Shift+Delete untuk clear browser cache

---

**Status**: Ready to use! 🚀

Next: Explore the application, make predictions, test functionality.