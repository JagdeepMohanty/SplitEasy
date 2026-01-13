import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../contexts/AuthContext';
import './CreateExpense.css';

const CreateExpense = () => {
  const { user, token } = useContext(AuthContext);
  const navigate = useNavigate();
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [friends, setFriends] = useState([]);
  const [selectedFriends, setSelectedFriends] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchFriends = async () => {
      try {
        const response = await axios.get('/api/friends');
        setFriends(response.data);
      } catch (err) {
        setError('Failed to load friends');
      }
    };
    fetchFriends();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    // Validation
    if (!description.trim()) {
      setError('Description is required');
      return;
    }
    
    const amountValue = parseFloat(amount);
    if (!amount || amountValue <= 0) {
      setError('Please enter a valid amount in INR');
      return;
    }
    
    if (selectedFriends.length === 0) {
      setError('Please select at least one friend');
      return;
    }

    setLoading(true);
    try {
      const participants = [...selectedFriends, user._id];
      await axios.post('/api/expenses', {
        description: description.trim(),
        amount: amountValue,
        participants
      });
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.msg || 'Failed to create expense');
    } finally {
      setLoading(false);
    }
  };

  const formatAmount = (value) => {
    // Remove non-numeric characters except decimal point
    return value.replace(/[^0-9.]/g, '');
  };

  return (
    <div className="expense-form">
      <h2>Add New Expense</h2>
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <input
            type="text"
            placeholder="Description (e.g., Dinner at restaurant)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
          />
        </div>
        
        <div className="form-group">
          <div className="amount-input">
            <span className="currency-symbol">₹</span>
            <input
              type="number"
              placeholder="0.00"
              value={amount}
              onChange={(e) => setAmount(formatAmount(e.target.value))}
              min="0.01"
              step="0.01"
              required
            />
          </div>
        </div>
        
        <div className="form-group">
          <label>Split with friends:</label>
          <select
            multiple
            value={selectedFriends}
            onChange={(e) => {
              const selected = Array.from(e.target.selectedOptions, option => option.value);
              setSelectedFriends(selected);
            }}
            required
          >
            {friends.map((friend) => (
              <option key={friend._id} value={friend._id}>
                {friend.name}
              </option>
            ))}
          </select>
          <small>Hold Ctrl/Cmd to select multiple friends</small>
        </div>
        
        <button type="submit" disabled={loading}>
          {loading ? 'Creating...' : 'Add Expense'}
        </button>
      </form>
    </div>
  );
};

export default CreateExpense;