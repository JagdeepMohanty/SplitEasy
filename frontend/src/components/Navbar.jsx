
import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-left">
          <Link to="/" className="navbar-brand">
            <span className="brand-icon">💰</span>
            SplitEase
          </Link>
        </div>
        <div className="navbar-right">
          {user ? (
            <div className="user-nav">
              <Link to="/" className="nav-link">Dashboard</Link>
              <Link to="/friends" className="nav-link">Friends</Link>
              <Link to="/create-expense" className="nav-link">Add Expense</Link>
              <Link to="/settle" className="nav-link">Settle</Link>
              <Link to="/debts" className="nav-link">Debts</Link>
              <button onClick={handleLogout} className="logout-btn">
                Logout
              </button>
            </div>
          ) : (
            <div className="auth-nav">
              <Link to="/login" className="auth-btn login-btn">Login</Link>
              <Link to="/register" className="auth-btn register-btn">Register</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;