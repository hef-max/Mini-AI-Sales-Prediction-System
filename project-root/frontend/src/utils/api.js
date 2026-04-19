import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * API Service dengan token management
 * Handles:
 * - Token storage (localStorage)
 * - Request interceptors (add token ke header)
 * - Error handling
 */

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor - add token ke setiap request
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors
apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token invalid atau expired, clear local storage
      localStorage.removeItem('access_token');
      localStorage.removeItem('username');
      window.location.href = '/login'; // Redirect ke login
    }
    return Promise.reject(error.response?.data || error.message);
  }
);

// ===== AUTH ENDPOINTS =====
export const authAPI = {
  login: (username, password) => 
    apiClient.post('/auth/login', { username, password }),
  
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('username');
  }
};

// ===== SALES ENDPOINTS =====
export const salesAPI = {
  getAllSales: () => 
    apiClient.get('/sales/'),
  
  getSalesSummary: () => 
    apiClient.get('/sales/summary')
};

// ===== PREDICTION ENDPOINTS =====
export const predictAPI = {
  predict: (jumlah_penjualan, harga, diskon) => 
    apiClient.post('/predict/', {
      jumlah_penjualan: Number(jumlah_penjualan),
      harga: Number(harga),
      diskon: Number(diskon)
    }),
  
  checkHealth: () => 
    apiClient.get('/predict/health')
};

// ===== TOKEN MANAGEMENT =====
export const setToken = (token) => {
  localStorage.setItem('access_token', token);
};

export const getToken = () => {
  return localStorage.getItem('access_token');
};

export const removeToken = () => {
  localStorage.removeItem('access_token');
};

export const isAuthenticated = () => {
  return !!localStorage.getItem('access_token');
};

export default apiClient;