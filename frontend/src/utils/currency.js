/**
 * Format amount to Indian Rupee currency
 * @param {number} amount - The amount to format
 * @returns {string} - Formatted currency string
 */
export const formatCurrency = (amount) => {
  if (typeof amount !== 'number' || isNaN(amount)) {
    return '₹0.00';
  }
  
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
};

/**
 * Format amount to Indian Rupee without currency symbol
 * @param {number} amount - The amount to format
 * @returns {string} - Formatted number string
 */
export const formatAmount = (amount) => {
  if (typeof amount !== 'number' || isNaN(amount)) {
    return '0.00';
  }
  
  return new Intl.NumberFormat('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
};

/**
 * Parse and validate amount input
 * @param {string|number} input - The input to parse
 * @returns {number|null} - Parsed amount or null if invalid
 */
export const parseAmount = (input) => {
  if (typeof input === 'number') {
    return input > 0 ? input : null;
  }
  
  if (typeof input === 'string') {
    const cleaned = input.replace(/[^0-9.]/g, '');
    const parsed = parseFloat(cleaned);
    return !isNaN(parsed) && parsed > 0 ? parsed : null;
  }
  
  return null;
};

/**
 * Validate if amount is valid for INR
 * @param {number} amount - The amount to validate
 * @returns {boolean} - True if valid
 */
export const isValidAmount = (amount) => {
  return typeof amount === 'number' && 
         !isNaN(amount) && 
         amount > 0 && 
         amount <= 999999999.99; // Max reasonable amount
};