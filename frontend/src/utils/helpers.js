/**
 * Utility functions for the application
 */

/**
 * Get AQI color based on level
 * @param {number} aqiValue - AQI value (1-5)
 * @returns {string} Color class or hex code
 */
export const getAQIColor = (aqiValue) => {
  const colors = {
    1: '#10b981', // Good - Green
    2: '#fbbf24', // Fair - Yellow
    3: '#f59e0b', // Moderate - Orange
    4: '#ef4444', // Poor - Red
    5: '#9333ea', // Very Poor - Purple
  };
  return colors[aqiValue] || '#6b7280';
};

/**
 * Get AQI background gradient
 * @param {number} aqiValue - AQI value (1-5)
 * @returns {string} CSS gradient
 */
export const getAQIGradient = (aqiValue) => {
  const gradients = {
    1: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
    2: 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)',
    3: 'linear-gradient(135deg, #f59e0b 0%, #ea580c 100%)',
    4: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
    5: 'linear-gradient(135deg, #9333ea 0%, #7e22ce 100%)',
  };
  return gradients[aqiValue] || 'linear-gradient(135deg, #6b7280 0%, #4b5563 100%)';
};

/**
 * Format timestamp to human-readable string
 * @param {number} timestamp - Unix timestamp
 * @returns {string} Formatted date string
 */
export const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp * 1000);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

/**
 * Format time ago string
 * @param {number} timestamp - Unix timestamp
 * @returns {string} Time ago string
 */
export const timeAgo = (timestamp) => {
  const seconds = Math.floor(Date.now() / 1000 - timestamp);
  
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
};

/**
 * Debounce function
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

/**
 * Get pollutant display name
 * @param {string} key - Pollutant key
 * @returns {string} Display name
 */
export const getPollutantName = (key) => {
  const names = {
    co: 'Carbon Monoxide',
    no: 'Nitrogen Monoxide',
    no2: 'Nitrogen Dioxide',
    o3: 'Ozone',
    so2: 'Sulfur Dioxide',
    pm2_5: 'PM2.5',
    pm10: 'PM10',
    nh3: 'Ammonia',
  };
  return names[key] || key.toUpperCase();
};

/**
 * Truncate decimal places
 * @param {number} num - Number to truncate
 * @param {number} precision - Decimal places
 * @returns {number} Truncated number
 */
export const truncateDecimal = (num, precision = 2) => {
  return Math.round(num * Math.pow(10, precision)) / Math.pow(10, precision);
};
