import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://easyxpense.onrender.com';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.data?.error) {
      error.message = error.response.data.error;
    } else if (error.response?.data?.message) {
      error.message = error.response.data.message;
    } else if (!error.response) {
      error.message = 'Network Error: Cannot reach server';
    }
    return Promise.reject(error);
  }
);

export const expensesAPI = {
  getAll: () => api.get('/api/expenses'),
  create: (expenseData) => api.post('/api/expenses', expenseData),
};

export const debtsAPI = {
  getAll: () => api.get('/api/debts'),
};

export const settlementsAPI = {
  create: (settlementData) => api.post('/api/settlements', settlementData),
  getHistory: () => api.get('/api/settlements'),
};

export const friendsAPI = {
  getAll: () => api.get('/api/friends'),
  add: (friendData) => api.post('/api/friends', friendData),
};

export default api;