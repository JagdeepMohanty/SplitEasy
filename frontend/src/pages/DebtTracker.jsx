import React, { useState, useEffect } from 'react';
import { debtsAPI, settlementsAPI } from '../services/api';
import { formatCurrency } from '../utils/currency';

const DebtTracker = () => {
  const [debts, setDebts] = useState([]);
  const [balances, setBalances] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [settlingDebt, setSettlingDebt] = useState(null);
  const [settlementAmount, setSettlementAmount] = useState('');

  useEffect(() => {
    fetchDebts();
  }, []);

  const fetchDebts = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await debtsAPI.getAll();
      
      // Handle optimized response format
      if (response.data.debts) {
        setDebts(response.data.debts);
        setBalances(response.data.balances || {});
      } else {
        // Legacy format
        setDebts(Array.isArray(response.data) ? response.data : []);
      }
    } catch (err) {
      setError(err.message || 'Failed to load debts');
      console.error('Debts error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSettleDebt = async (debt) => {
    const amount = parseFloat(settlementAmount);
    if (!amount || amount <= 0) {
      alert('Please enter a valid amount');
      return;
    }

    try {
      await settlementsAPI.create({
        fromUser: debt.debtor,
        toUser: debt.creditor,
        amount: amount
      });

      setSettlingDebt(null);
      setSettlementAmount('');
      fetchDebts();
    } catch (err) {
      alert(err.message || 'Failed to settle debt');
      console.error('Settlement error:', err);
    }
  };

  if (loading) {
    return (
      <div className="debt-tracker">
        <div className="loading">Loading debts...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="debt-tracker">
        <div className="error">{error}</div>
      </div>
    );
  }

  const activeDebts = debts.filter(debt => debt.amount > 0.01);
  const totalAmount = debts.reduce((sum, debt) => sum + (debt.amount || 0), 0);

  return (
    <div className="debt-tracker">
      <div className="page-header">
        <h1>Debt Tracker</h1>
      </div>

      <div className="debt-summary">
        <div className="summary-cards">
          <div className="summary-card">
            <h3>Pending Settlements</h3>
            <p className="amount">{activeDebts.length}</p>
          </div>
          <div className="summary-card">
            <h3>Total Amount</h3>
            <p className="amount">{formatCurrency(totalAmount)}</p>
          </div>
        </div>
      </div>

      <div className="debts-section">
        <h2>Active Debts</h2>
        {activeDebts.length === 0 ? (
          <div className="empty-state">
            <p>🎉 All settled up! No outstanding debts.</p>
          </div>
        ) : (
          <div className="debts-list">
            {activeDebts.map((debt, index) => (
              <div key={index} className="debt-card">
                <div className="debt-info">
                  <div className="friend-avatar">
                    {debt.debtor.charAt(0).toUpperCase()}
                  </div>
                  <div className="debt-details">
                    <h3>{debt.debtor} → {debt.creditor}</h3>
                    <p className="debt-amount">
                      <strong>{formatCurrency(debt.amount)}</strong>
                    </p>
                  </div>
                </div>
                <div className="debt-actions">
                  {settlingDebt === index ? (
                    <div className="settle-form">
                      <input
                        type="number"
                        value={settlementAmount}
                        onChange={(e) => setSettlementAmount(e.target.value)}
                        placeholder="Amount"
                        min="0.01"
                        step="0.01"
                        className="settle-input"
                      />
                      <button
                        onClick={() => handleSettleDebt(debt)}
                        className="btn btn-primary btn-sm"
                      >
                        Confirm
                      </button>
                      <button
                        onClick={() => {
                          setSettlingDebt(null);
                          setSettlementAmount('');
                        }}
                        className="btn btn-secondary btn-sm"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <button
                      onClick={() => {
                        setSettlingDebt(index);
                        setSettlementAmount(debt.amount.toString());
                      }}
                      className="btn btn-primary btn-sm"
                    >
                      Settle Up
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DebtTracker;