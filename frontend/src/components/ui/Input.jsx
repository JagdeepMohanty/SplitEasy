import React from 'react';

const Input = ({ 
  label,
  error,
  success,
  helper,
  floating = false,
  className = '',
  ...props 
}) => {
  const inputClasses = [
    'form-input',
    error ? 'form-error' : '',
    success ? 'form-success' : '',
    className
  ].filter(Boolean).join(' ');

  if (floating) {
    return (
      <div className="form-group">
        <div className="form-floating">
          <input 
            className={inputClasses}
            placeholder=" "
            {...props}
          />
          {label && <label className="form-label">{label}</label>}
        </div>
        {error && <div className="form-error-message">⚠️ {error}</div>}
        {success && <div className="form-success-message">✓ {success}</div>}
        {helper && <div className="form-helper">{helper}</div>}
      </div>
    );
  }

  return (
    <div className="form-group">
      {label && <label className="form-label">{label}</label>}
      <input className={inputClasses} {...props} />
      {error && <div className="form-error-message">⚠️ {error}</div>}
      {success && <div className="form-success-message">✓ {success}</div>}
      {helper && <div className="form-helper">{helper}</div>}
    </div>
  );
};

export default Input;