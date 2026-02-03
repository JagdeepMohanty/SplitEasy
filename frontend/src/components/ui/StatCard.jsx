import React from 'react';

const StatCard = ({ 
  title, 
  value, 
  icon, 
  change, 
  changeType = 'neutral',
  className = '',
  ...props 
}) => {
  const changeClasses = {
    positive: 'stat-card-change positive',
    negative: 'stat-card-change negative',
    neutral: 'stat-card-change'
  };

  return (
    <div className={`stat-card ${className}`} {...props}>
      {icon && <div className="stat-card-icon">{icon}</div>}
      <div className="stat-card-title">{title}</div>
      <div className="stat-card-value">{value}</div>
      {change && (
        <div className={changeClasses[changeType]}>
          {changeType === 'positive' && '↗️'}
          {changeType === 'negative' && '↘️'}
          {change}
        </div>
      )}
    </div>
  );
};

export default StatCard;