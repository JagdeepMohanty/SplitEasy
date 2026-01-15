import React, { useState } from 'react';
import { testAPI } from '../services/api';
import api from '../services/api';

const TestConnection = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const addResult = (test, success, message, data = null) => {
    setResults(prev => [...prev, { test, success, message, data, timestamp: new Date().toISOString() }]);
  };

  const runTests = async () => {
    setResults([]);
    setLoading(true);

    // Test 1: Root endpoint
    try {
      const response = await api.get('/');
      addResult('Root Endpoint', true, 'Backend is running', response.data);
    } catch (error) {
      addResult('Root Endpoint', false, error.message);
    }

    // Test 2: Health endpoint
    try {
      const response = await api.get('/health');
      addResult('Health Check', true, 'Health check passed', response.data);
    } catch (error) {
      addResult('Health Check', false, error.message);
    }

    // Test 3: Test API GET
    try {
      const response = await testAPI.ping();
      addResult('Test API GET', true, 'API connectivity verified', response.data);
    } catch (error) {
      addResult('Test API GET', false, error.message);
    }

    // Test 4: Test API POST
    try {
      const response = await testAPI.testPost({ test: 'data', timestamp: Date.now() });
      addResult('Test API POST', true, 'POST request successful', response.data);
    } catch (error) {
      addResult('Test API POST', false, error.message);
    }

    // Test 5: Get Friends
    try {
      const response = await api.get('/api/friends');
      addResult('Get Friends', true, `Retrieved ${response.data.length} friends`, { count: response.data.length });
    } catch (error) {
      addResult('Get Friends', false, error.message);
    }

    // Test 6: Get Expenses
    try {
      const response = await api.get('/api/expenses');
      addResult('Get Expenses', true, `Retrieved ${response.data.length} expenses`, { count: response.data.length });
    } catch (error) {
      addResult('Get Expenses', false, error.message);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>🔧 API Connection Test</h1>
      <p>This page tests the connection between frontend and backend.</p>
      
      <div style={{ marginBottom: '20px' }}>
        <strong>Backend URL:</strong> {process.env.REACT_APP_API_URL || 'https://easyxpense.onrender.com'}
      </div>

      <button
        onClick={runTests}
        disabled={loading}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer',
          marginBottom: '20px'
        }}
      >
        {loading ? 'Running Tests...' : 'Run Connection Tests'}
      </button>

      <div>
        {results.map((result, index) => (
          <div
            key={index}
            style={{
              padding: '15px',
              marginBottom: '10px',
              backgroundColor: result.success ? '#d4edda' : '#f8d7da',
              border: `1px solid ${result.success ? '#c3e6cb' : '#f5c6cb'}`,
              borderRadius: '4px',
              color: result.success ? '#155724' : '#721c24'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
              <span style={{ fontSize: '20px', marginRight: '10px' }}>
                {result.success ? '✅' : '❌'}
              </span>
              <strong>{result.test}</strong>
            </div>
            <div style={{ marginLeft: '30px' }}>
              <div>{result.message}</div>
              {result.data && (
                <pre style={{
                  marginTop: '10px',
                  padding: '10px',
                  backgroundColor: 'rgba(0,0,0,0.1)',
                  borderRadius: '4px',
                  fontSize: '12px',
                  overflow: 'auto'
                }}>
                  {JSON.stringify(result.data, null, 2)}
                </pre>
              )}
            </div>
          </div>
        ))}
      </div>

      {results.length > 0 && (
        <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f0f0f0', borderRadius: '4px' }}>
          <h3>Summary</h3>
          <p>
            <strong>Passed:</strong> {results.filter(r => r.success).length} / {results.length}
          </p>
          <p>
            <strong>Failed:</strong> {results.filter(r => !r.success).length} / {results.length}
          </p>
          {results.every(r => r.success) && (
            <p style={{ color: '#155724', fontWeight: 'bold' }}>
              🎉 All tests passed! Backend is fully operational.
            </p>
          )}
          {results.some(r => !r.success) && (
            <p style={{ color: '#721c24', fontWeight: 'bold' }}>
              ⚠️ Some tests failed. Check the errors above and verify backend configuration.
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default TestConnection;
