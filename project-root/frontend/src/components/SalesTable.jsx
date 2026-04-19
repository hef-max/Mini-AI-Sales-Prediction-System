import React, { useEffect, useState } from 'react';
import { salesAPI } from '../utils/api';

/**
 * Sales Table Component
 * 
 * Displays:
 * - All sales data dari backend
 * - Product info, sales qty, price, discount, status
 * - Loading state
 * - Error handling
 * - Refresh button
 */

function SalesTable() {
  const [sales, setSales] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [summary, setSummary] = useState(null);

  const fetchSalesData = async () => {
    setLoading(true);
    setError(null);

    try {
      const [salesData, summaryData] = await Promise.all([
        salesAPI.getAllSales(),
        salesAPI.getSalesSummary()
      ]);

      setSales(salesData.data || []);
      setSummary(summaryData);
    } catch (err) {
      setError(err.detail || 'Gagal mengambil data penjualan');
      console.error('Error fetching sales:', err);
    } finally {
      setLoading(false);
    }
  };

  // Fetch data on component mount
  useEffect(() => {
    fetchSalesData();
  }, []);

  if (loading) {
    return (
      <div className="card">
        <div className="card-body text-center">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-2">Loading sales data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card">
        <div className="card-body">
          <div className="alert alert-danger" role="alert">
            <strong>Error:</strong> {error}
          </div>
          <button
            className="btn btn-sm btn-outline-primary"
            onClick={fetchSalesData}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="card-header d-flex justify-content-between align-items-center">
        <h5 className="mb-0">📊 Daftar Produk Penjualan</h5>
        <button
          className="btn btn-sm btn-outline-secondary"
          onClick={fetchSalesData}
        >
          🔄 Refresh
        </button>
      </div>

      {summary && (
        <div className="card-body border-bottom bg-light">
          <div className="row">
            <div className="col-md-4">
              <small className="text-muted">Total Produk</small>
              <p className="h5">{summary.total_products}</p>
            </div>
            <div className="col-md-4">
              <small className="text-muted">Laris</small>
              <p className="h5 text-success">{summary.laris_count}</p>
            </div>
            <div className="col-md-4">
              <small className="text-muted">Tidak Laris</small>
              <p className="h5 text-danger">{summary.tidak_laris_count}</p>
            </div>
          </div>
        </div>
      )}

      <div className="table-responsive">
        <table className="table table-hover mb-0">
          <thead className="table-light">
            <tr>
              <th>ID</th>
              <th>Nama Produk</th>
              <th className="text-end">Jumlah Jual</th>
              <th className="text-end">Harga</th>
              <th className="text-end">Diskon (%)</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {sales.length > 0 ? (
              sales.map((item) => (
                <tr key={item.product_id}>
                  <td className="text-muted">{item.product_id}</td>
                  <td>{item.product_name}</td>
                  <td className="text-end">{item.jumlah_penjualan}</td>
                  <td className="text-end">
                    Rp {item.harga.toLocaleString('id-ID')}
                  </td>
                  <td className="text-end">{item.diskon}%</td>
                  <td>
                    <span
                      className={`badge ${
                        item.status === 'Laris'
                          ? 'bg-success'
                          : 'bg-danger'
                      }`}
                    >
                      {item.status}
                    </span>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="text-center text-muted">
                  Tidak ada data penjualan
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {sales.length > 0 && (
        <div className="card-footer text-muted text-center">
          Menampilkan {sales.length} dari {summary?.total_products || 0} produk
        </div>
      )}
    </div>
  );
}

export default SalesTable;