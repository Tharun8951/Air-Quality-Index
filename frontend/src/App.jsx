import { useState, useCallback } from 'react';
import './index.css';
import { searchCity } from './services/apiClient';
import {
  getAQIColor,
  getAQIGradient,
  formatTimestamp,
  timeAgo,
  debounce,
  getPollutantName,
  truncateDecimal,
} from './utils/helpers';

function App() {
  const [cityName, setCityName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const handleSearch = useCallback(
    async (searchTerm) => {
      if (!searchTerm || searchTerm.trim().length < 2) {
        setError('Please enter a valid city name');
        return;
      }

      setLoading(true);
      setError(null);
      setData(null);

      try {
        const response = await searchCity(searchTerm.trim());
        setData(response);
      } catch (err) {
        const errorMessage =
          err.response?.data?.message ||
          'Failed to fetch air quality data. Please try again.';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const debouncedSearch = useCallback(debounce(handleSearch, 500), [handleSearch]);

  const handleSubmit = (e) => {
    e.preventDefault();
    handleSearch(cityName);
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <h1>Air Quality Index</h1>
        <p>Search for real-time air quality data worldwide</p>
      </header>

      {/* Search Section */}
      <section className="search-section">
        <form onSubmit={handleSubmit} className="search-container">
          <input
            type="text"
            className="search-input"
            placeholder="Enter city name (e.g., London, New York, Tokyo)..."
            value={cityName}
            onChange={(e) => setCityName(e.target.value)}
            disabled={loading}
          />
          <button type="submit" className="search-button" disabled={loading}>
            {loading ? <span className="spinner"></span> : 'Search'}
          </button>
        </form>
      </section>

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <strong>Error: </strong>
          {error}
        </div>
      )}

      {/* Air Quality Data */}
      {data && data.status === 'success' && (
        <div className="aqi-card">
          {/* Header */}
          <div className="aqi-header">
            <h2 className="aqi-city">
              {data.data.city}
              <span className="aqi-city-country"> ({data.data.country})</span>
            </h2>

            {/* AQI Badge */}
            <div
              className="aqi-badge"
              style={{
                background: getAQIGradient(data.data.aqi.value),
              }}
            >
              <div className="aqi-value">{data.data.aqi.value}</div>
              <div className="aqi-level">{data.data.aqi.level}</div>
            </div>

            <p className="aqi-description">{data.data.aqi.description}</p>

            {/* Cache & Response Time Indicators */}
            <div style={{ marginTop: '1rem' }}>
              {data.from_cache && (
                <div className="cache-indicator">
                  <svg
                    width="12"
                    height="12"
                    viewBox="0 0 12 12"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <circle cx="6" cy="6" r="5" stroke="currentColor" strokeWidth="2" />
                    <path
                      d="M6 2v4l3 3"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                  </svg>
                  <span>Cached Data</span>
                  {data.data.cached_at && (
                    <span style={{ opacity: 0.7 }}>
                      · {timeAgo(Math.floor(data.data.cached_at))}
                    </span>
                  )}
                </div>
              )}
              <p className="response-time">
                Response time: {data.response_time_ms}ms
                {' · '}
                Updated: {formatTimestamp(data.data.timestamp)}
              </p>
            </div>
          </div>

          {/* Pollutants Section */}
          <div className="pollutants-section">
            <h3 className="section-title">Pollutant Levels</h3>
            <div className="pollutants-grid">
              {Object.entries(data.data.pollutants).map(([key, pollutant]) => {
                const percentage = pollutant.who_guideline
                  ? Math.min((pollutant.value / pollutant.who_guideline) * 100, 100)
                  : (pollutant.value / 100) * 50; // fallback calculation

                return (
                  <div key={key} className="pollutant-card">
                    <div className="pollutant-name">{getPollutantName(key)}</div>
                    <div className="pollutant-value">
                      {truncateDecimal(pollutant.value, 1)}
                      <span className="pollutant-unit"> {pollutant.unit}</span>
                    </div>

                    {/* Progress Bar */}
                    <div className="pollutant-bar">
                      <div
                        className="pollutant-bar-fill"
                        style={{
                          width: `${percentage}%`,
                          background:
                            pollutant.exceeds_who
                              ? 'linear-gradient(90deg, #ef4444, #dc2626)'
                              : 'linear-gradient(90deg, #10b981, #059669)',
                        }}
                      ></div>
                    </div>

                    {/* WHO Guideline Indicator */}
                    {pollutant.who_guideline && (
                      <div className="who-indicator">
                        <span
                          className={`who-badge ${pollutant.exceeds_who ? 'exceeded' : 'safe'}`}
                        >
                          {pollutant.exceeds_who ? 'Exceeds' : 'Within'} WHO
                        </span>
                        <span>
                          {truncateDecimal(pollutant.percentage_of_guideline, 0)}% of limit
                        </span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Forecast Section */}
          {data.data.forecast && data.data.forecast.length > 0 && (
            <div className="forecast-section">
              <h3 className="section-title">4-Day Hourly Forecast</h3>
              <div className="forecast-grid">
                {data.data.forecast.slice(0, 48).map((item, index) => (
                  <div key={index} className="forecast-item">
                    <div className="forecast-time">{formatTimestamp(item.timestamp)}</div>
                    <div
                      className="forecast-aqi"
                      style={{ color: getAQIColor(item.aqi) }}
                    >
                      {item.aqi}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
                      PM2.5: {truncateDecimal(item.pm25, 1)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Footer */}
      {data && (
        <footer style={{ textAlign: 'center', marginTop: '2rem', color: '#94a3b8', fontSize: '0.875rem' }}>
          <p>
            Data provided by OpenWeatherMap API
            {' · '}
            Coordinates: {data.data.coordinates.lat.toFixed(4)}, {data.data.coordinates.lon.toFixed(4)}
          </p>
        </footer>
      )}
    </div>
  );
}

export default App;
