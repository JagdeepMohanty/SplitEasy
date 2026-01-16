import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { expensesAPI, debtsAPI } from '../services/api';
import { formatCurrency } from '../utils/currency';

const Dashboard = () => {
  const [expenses, setExpenses] = useState([]);
  const [debts, setDebts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError('');
      
      const [expensesRes, debtsRes] = await Promise.all([
        expensesAPI.getAll(),
        debtsAPI.getAll()
      ]);
      
      setExpenses(expensesRes.data.slice(0, 5)); // Show only recent 5
      
      // Handle both optimized and legacy debt response formats
      const debtsData = debtsRes.data.debts || debtsRes.data;
      setDebts(Array.isArray(debtsData) ? debtsData : []);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard">
        <div className="error">{error}</div>
      </div>
    );
  }

  const totalOwed = debts
    .reduce((sum, debt) => sum + (debt.amount || 0), 0);

  const totalExpenses = expenses.reduce((sum, exp) => sum + (exp.amount || 0), 0);

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <Link to="/add-expense" className="btn btn-primary">
          Add New Expense
        </Link>
      </div>

      <div className="dashboard-stats">
        <div className="stat-card">
          <h3>Total Expenses</h3>
          <p className="amount">{formatCurrency(totalExpenses)}</p>
        </div>
        <div className="stat-card">
          <h3>Pending Settlements</h3>
          <p className="amount">{debts.length}</p>
        </div>
        <div className="stat-card">
          <h3>Net Balance</h3>
          <p className="amount">{formatCurrency(totalOwed)}</p>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="recent-expenses">
          <div className="section-header">
            <h2>Recent Expenses</h2>
            <Link to="/history" className="view-all">View All</Link>
          </div>
          {expenses.length === 0 ? (
            <p className="empty-state">No expenses yet. <Link to="/add-expense">Add your first expense</Link></p>
          ) : (
            <div className="expense-list">
              {expenses.map((expense) => (
                <div key={expense._id} className="expense-item">
                  <div className="expense-info">
                    <h4>{expense.description}</h4>
                    <p>Paid by: {expense.payer}</p>
                  </div>
                  <div className="expense-amount">
                    {formatCurrency(expense.amount)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="debt-summary">
          <div className="section-header">
            <h2>Pending Settlements</h2>
            <Link to="/debts" className="view-all">View All</Link>
          </div>
          {debts.length === 0 ? (
            <p className="empty-state">All settled up!</p>
          ) : (
            <div className="debt-list">
              {debts.slice(0, 5).map((debt, index) => (
                <div key={index} className="debt-item">
                  <div className="debt-info">
                    <h4>{debt.debtor} → {debt.creditor}</h4>
                  </div>
                  <div className="debt-amount">
                    {formatCurrency(debt.amount)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;