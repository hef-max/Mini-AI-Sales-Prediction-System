import React from 'react';
import '../styles/PredictionResult.css';

/**
 * Prediction Result Component
 * 
 * Displays:
 * - Prediction result (Laris / Tidak Laris)
 * - Confidence score dengan progress bar
 * - Input data yang digunakan
 * - Visual indication dengan warna
 */

function PredictionResult({ result, onClose }) {
  if (!result) return null;

  const prediction = result.prediction;
  const confidence = result.confidence;
  const inputData = result.input_data;

  // Determine badge color dan icon
  const isLaris = prediction === 'Laris';
  const badgeClass = isLaris ? 'bg-success' : 'bg-danger';
  const iconEmoji = isLaris ? '📈' : '📉';
  const confidencePercent = Math.round(confidence * 100);

  return (
    <div className="prediction-result-overlay">
      <div className="prediction-result-card">
        <div className="result-header">
          <h5>Hasil Prediksi</h5>
          <button
            className="btn-close"
            aria-label="Close"
            onClick={onClose}
          ></button>
        </div>

        <div className="result-body">
          {/* Prediction Result */}
          <div className="prediction-display">
            <span className={`badge ${badgeClass} badge-lg`}>
              {iconEmoji} {prediction}
            </span>
          </div>

          {/* Confidence Score */}
          <div className="confidence-section">
            <div className="d-flex justify-content-between align-items-center mb-2">
              <label className="form-label mb-0">
                Confidence Score
              </label>
              <span className="badge bg-info">{confidencePercent}%</span>
            </div>
            <div className="progress" style={{ height: '25px' }}>
              <div
                className={`progress-bar ${
                  confidence >= 0.8
                    ? 'bg-success'
                    : confidence >= 0.6
                    ? 'bg-warning'
                    : 'bg-danger'
                }`}
                role="progressbar"
                style={{ width: `${confidencePercent}%` }}
                aria-valuenow={confidencePercent}
                aria-valuemin="0"
                aria-valuemax="100"
              >
                {confidencePercent}%
              </div>
            </div>
            <small className="text-muted">
              {confidence >= 0.8
                ? 'Prediksi sangat yakin'
                : confidence >= 0.6
                ? 'Prediksi cukup yakin'
                : 'Prediksi kurang yakin'}
            </small>
          </div>

          {/* Input Data Used */}
          <div className="input-data-section">
            <h6>Data Input:</h6>
            <div className="input-data-grid">
              <div className="input-item">
                <small className="text-muted">Jumlah Penjualan</small>
                <p className="value">{inputData.jumlah_penjualan} unit</p>
              </div>
              <div className="input-item">
                <small className="text-muted">Harga</small>
                <p className="value">Rp {inputData.harga.toLocaleString('id-ID')}</p>
              </div>
              <div className="input-item">
                <small className="text-muted">Diskon</small>
                <p className="value">{inputData.diskon}%</p>
              </div>
            </div>
          </div>

          {/* Interpretation */}
          <div className="interpretation">
            <p className="mb-0">
              <strong>Interpretasi:</strong> Berdasarkan fitur input, produk
              diprediksi akan{' '}
              <strong className={isLaris ? 'text-success' : 'text-danger'}>
                {isLaris ? 'LARIS' : 'TIDAK LARIS'}
              </strong>{' '}
              dengan tingkat kepercayaan {confidencePercent}%.
            </p>
          </div>
        </div>

        <div className="result-footer">
          <button
            className="btn btn-outline-secondary w-100"
            onClick={onClose}
          >
            Tutup Hasil
          </button>
        </div>
      </div>
    </div>
  );
}

export default PredictionResult;