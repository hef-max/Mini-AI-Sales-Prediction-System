import React, { useState } from 'react';
import { predictAPI } from '../utils/api';

/**
 * Prediction Form Component
 * 
 * Features:
 * - Input form (jumlah_penjualan, harga, diskon)
 * - Form validation
 * - Loading state
 * - Error handling
 * - Calls parent callback dengan hasil prediksi
 */

function PredictionForm({ onPredictionResult }) {
  const [formData, setFormData] = useState({
    jumlah_penjualan: '',
    harga: '',
    diskon: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(null);
  };

  const validateForm = () => {
    if (!formData.jumlah_penjualan || !formData.harga || formData.diskon === '') {
      setError('Semua field harus diisi');
      return false;
    }

    const qty = Number(formData.jumlah_penjualan);
    const price = Number(formData.harga);
    const discount = Number(formData.diskon);

    if (qty < 0 || price < 0 || discount < 0 || discount > 100) {
      setError('Input tidak valid. Cek range nilai yang benar.');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setLoading(true);
    setError(null);

    try {
      const result = await predictAPI.predict(
        formData.jumlah_penjualan,
        formData.harga,
        formData.diskon
      );

      // Clear form
      setFormData({
        jumlah_penjualan: '',
        harga: '',
        diskon: ''
      });

      // Pass result ke parent
      onPredictionResult(result);

    } catch (err) {
      setError(err.detail || 'Prediksi gagal. Coba lagi.');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <h5 className="mb-0">🔮 Prediksi Status Produk</h5>
      </div>

      <div className="card-body">
        {error && (
          <div className="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Error:</strong> {error}
            <button
              type="button"
              className="btn-close"
              onClick={() => setError(null)}
            ></button>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="row">
            <div className="col-md-4">
              <div className="form-group mb-3">
                <label htmlFor="jumlah_penjualan" className="form-label">
                  Jumlah Penjualan (unit)
                </label>
                <input
                  type="number"
                  className="form-control"
                  id="jumlah_penjualan"
                  name="jumlah_penjualan"
                  value={formData.jumlah_penjualan}
                  onChange={handleChange}
                  placeholder="Contoh: 150"
                  min="0"
                  disabled={loading}
                  required
                />
                <small className="form-text text-muted">
                  Jumlah unit yang terjual
                </small>
              </div>
            </div>

            <div className="col-md-4">
              <div className="form-group mb-3">
                <label htmlFor="harga" className="form-label">
                  Harga (Rp)
                </label>
                <input
                  type="number"
                  className="form-control"
                  id="harga"
                  name="harga"
                  value={formData.harga}
                  onChange={handleChange}
                  placeholder="Contoh: 5000000"
                  min="0"
                  disabled={loading}
                  required
                />
                <small className="form-text text-muted">
                  Harga satuan produk
                </small>
              </div>
            </div>

            <div className="col-md-4">
              <div className="form-group mb-3">
                <label htmlFor="diskon" className="form-label">
                  Diskon (%)
                </label>
                <input
                  type="number"
                  className="form-control"
                  id="diskon"
                  name="diskon"
                  value={formData.diskon}
                  onChange={handleChange}
                  placeholder="Contoh: 10"
                  min="0"
                  max="100"
                  disabled={loading}
                  required
                />
                <small className="form-text text-muted">
                  Diskon dalam persen (0-100)
                </small>
              </div>
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary w-100"
            disabled={loading}
          >
            {loading ? (
              <>
                <span
                  className="spinner-border spinner-border-sm me-2"
                  role="status"
                  aria-hidden="true"
                ></span>
                Prediksi sedang diproses...
              </>
            ) : (
              'Lakukan Prediksi'
            )}
          </button>
        </form>

        <div className="mt-3 p-3 bg-light rounded">
          <p className="mb-0">
            <small className="text-muted">
              💡 Masukkan data produk untuk mendapatkan prediksi status
              penjualan (Laris atau Tidak Laris) berdasarkan model ML.
            </small>
          </p>
        </div>
      </div>
    </div>
  );
}

export default PredictionForm;