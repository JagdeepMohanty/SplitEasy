import React, { useContext } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Friends from './pages/Friends';
import CreateExpense from './pages/CreateExpense';
import Settle from './pages/Settle';
import DebtTracker from './pages/DebtTracker';
import './App.css';

// Loading component
const LoadingSpinner = () => (
  <div className="loading-container">
    <div className="loading-spinner"></div>
    <p>Loading SplitEasy...</p>
  </div>
);

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useContext(AuthContext);
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

// Public Route Component (redirect to dashboard if authenticated)
const PublicRoute = ({ children }) => {
  const { isAuthenticated } = useContext(AuthContext);
  return !isAuthenticated ? children : <Navigate to="/" replace />;
};

const AppRoutes = () => {
  const { isAuthenticated, loading } = useContext(AuthContext);
  
  if (loading) {
    return <LoadingSpinner />;
  }
  
  return (
    <div className="app-container">
      {isAuthenticated && <Navbar />}
      <Routes>
        <Route path="/login" element={
          <PublicRoute><Login /></PublicRoute>
        } />
        <Route path="/register" element={
          <PublicRoute><Register /></PublicRoute>
        } />
        <Route path="/" element={
          <ProtectedRoute><Dashboard /></ProtectedRoute>
        } />
        <Route path="/friends" element={
          <ProtectedRoute><Friends /></ProtectedRoute>
        } />
        <Route path="/create-expense" element={
          <ProtectedRoute><CreateExpense /></ProtectedRoute>
        } />
        <Route path="/settle" element={
          <ProtectedRoute><Settle /></ProtectedRoute>
        } />
        <Route path="/debts" element={
          <ProtectedRoute><DebtTracker /></ProtectedRoute>
        } />
        <Route path="*" element={
          isAuthenticated ? <Navigate to="/" replace /> : <Navigate to="/login" replace />
        } />
      </Routes>
    </div>
  );
};

const App = () => (
  <AuthProvider>
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  </AuthProvider>
);

export default App;