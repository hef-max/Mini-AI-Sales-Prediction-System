import React, { useState } from 'react';
import { authAPI, setToken } from '../utils/api';
import '../styles/LoginPage.css';

/**
 * Login Page Component
 * 
 * Features:
 * - Username/password form
 * - Error handling
 * - Loading state
 * - Dummy users info
 */

function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('password123');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const response = await authAPI.login(username, password);
      
      // Save token dan username
      setToken(response.access_token);
      localStorage.setItem('username', username);
      
      // Callback ke parent component
      onLoginSuccess(username);
      
    } catch (err) {
      setError(err.detail || 'Login gagal. Username atau password salah.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>AI Sales Prediction</h1>
          <p>Login untuk akses dashboard</p>
        </div>

        {error && (
          <div className="alert alert-danger" role="alert">
            <strong>Error:</strong> {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              className="form-control"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Masukkan username"
              disabled={loading}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="password-input-group">
              <input
                type={showPassword ? 'text' : 'password'}
                className="form-control"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Masukkan password"
                disabled={loading}
                required
              />
              <button
                type="button"
                className="btn-toggle-password"
                onClick={() => setShowPassword(!showPassword)}
                tabIndex="-1"
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-block w-100"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="login-info">
          <p className="info-title">Dummy Users (untuk testing):</p>
          <ul className="dummy-users">
            <li><code>admin</code> : <code>password123</code></li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;