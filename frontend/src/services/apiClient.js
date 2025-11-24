/**
 * API Client for Air Quality Backend
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    if (error.response) {
      console.error(`API Error: ${error.response.status}`, error.response.data);
    } else if (error.request) {
      console.error('API Error: No response received', error.request);
    } else {
      console.error('API Error:', error.message);
    }
    return Promise.reject(error);
  }
);

/**
 * Search for air quality data by city name
 * @param {string} cityName - Name of the city
 * @returns {Promise} API response with air quality data
 */
export const searchCity = async (cityName) => {
  const response = await apiClient.get('/search', {
    params: { city: cityName },
  });
  return response.data;
};

/**
 * Get cache statistics
 * @returns {Promise} Cache statistics data
 */
export const getCacheStats = async () => {
  const response = await apiClient.get('/cache/stats');
  return response.data;
};

/**
 * Check API health
 * @returns {Promise} Health check data
 */
export const healthCheck = async () => {
  const response = await apiClient.get('/health');
  return response.data;
};

export default apiClient;
