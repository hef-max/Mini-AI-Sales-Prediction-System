import React, { useState } from 'react';
import SalesTable from '../components/SalesTable';
import PredictionForm from '../components/PredictionForm';
import PredictionResult from '../components/PredictionResult';

/**
 * Dashboard Page
 * 
 * Main page setelah login dengan:
 * - Sales data table
 * - Prediction form
 * - Prediction result display
 * - User info & logout button
 */

function Dashboard({ username, onLogout }) {
  const [predictionResult, setPredictionResult] = useState(null);

  const handlePredictionResult = (result) => {
    setPredictionResult(result);
  };

  const handleClosePrediction = () => {
    setPredictionResult(null);
  };

  return (
    <div className="dashboard-container">
      {/* Header */}
      <nav className="navbar navbar-expand-lg navbar-light bg-light border-bottom mb-4">
        <div className="container-fluid">
          <span className="navbar-brand mb-0 h1">
            🤖 AI Sales Prediction Dashboard
          </span>
          <div className="ms-auto d-flex align-items-center gap-3">
            <span className="text-muted">
              Welcome, <strong>{username}</strong>
            </span>
            <button
              className="btn btn-outline-danger btn-sm"
              onClick={onLogout}
            >
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container-fluid">
        {/* Tabs Navigation */}
        <ul className="nav nav-tabs mb-4" role="tablist">
          <li className="nav-item" role="presentation">
            <button
              className="nav-link active"
              id="sales-tab"
              data-bs-toggle="tab"
              data-bs-target="#sales-content"
              type="button"
              role="tab"
            >
              📊 Data Penjualan
            </button>
          </li>
          <li className="nav-item" role="presentation">
            <button
              className="nav-link"
              id="predict-tab"
              data-bs-toggle="tab"
              data-bs-target="#predict-content"
              type="button"
              role="tab"
            >
              🔮 Prediksi
            </button>
          </li>
        </ul>

        {/* Tab Content */}
        <div className="tab-content">
          {/* Sales Tab */}
          <div
            className="tab-pane fade show active"
            id="sales-content"
            role="tabpanel"
          >
            <SalesTable />
          </div>

          {/* Prediction Tab */}
          <div
            className="tab-pane fade"
            id="predict-content"
            role="tabpanel"
          >
            <div className="row">
              <div className="col-lg-8">
                <PredictionForm onPredictionResult={handlePredictionResult} />
              </div>
              <div className="col-lg-4">
                <div className="card bg-light">
                  <div className="card-body">
                    <h6 className="card-title">📝 Panduan Prediksi</h6>
                    <ul className="small">
                      <li>
                        <strong>Jumlah Penjualan:</strong> Berapa banyak
                        unit yang terjual
                      </li>
                      <li>
                        <strong>Harga:</strong> Harga satuan produk
                        dalam rupiah
                      </li>
                      <li>
                        <strong>Diskon:</strong> Diskon yang diberikan
                        (0-100%)
                      </li>
                    </ul>
                    <hr />
                    <p className="small mb-0">
                      Model ML akan memprediksi apakah produk tersebut akan
                      <strong> Laris</strong> atau{' '}
                      <strong>Tidak Laris</strong> berdasarkan fitur-fitur
                      tersebut.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Prediction Result Modal */}
      {predictionResult && (
        <PredictionResult
          result={predictionResult}
          onClose={handleClosePrediction}
        />
      )}
    </div>
  );
}

export default Dashboard;