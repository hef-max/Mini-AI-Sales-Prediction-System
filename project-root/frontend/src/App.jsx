import React, { useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import { isAuthenticated, authAPI } from './utils/api';
import './styles/App.css';

/**
 * Main App Component
 * 
 * Handles:
 * - Routing between Login dan Dashboard
 * - Authentication state
 * - User session management
 */

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [appLoading, setAppLoading] = useState(true);

  // Check if user is already logged in on mount
  useEffect(() => {
    if (isAuthenticated()) {
      const storedUsername = localStorage.getItem('username');
      setUsername(storedUsername || '');
      setIsLoggedIn(true);
    }
    setAppLoading(false);
  }, []);

  const handleLoginSuccess = (loggedInUsername) => {
    setUsername(loggedInUsername);
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    authAPI.logout();
    setIsLoggedIn(false);
    setUsername('');
  };

  if (appLoading) {
    return (
      <div className="app-loading">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p>Loading application...</p>
      </div>
    );
  }

  return (
    <div className="app">
      {isLoggedIn ? (
        <Dashboard username={username} onLogout={handleLogout} />
      ) : (
        <LoginPage onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}

export default App;