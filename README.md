# Air Quality Index Search Engine

A full-stack web application for searching and displaying real-time air quality data worldwide. Built with Django REST API backend and React frontend.

## Features

### Backend (Django REST API)
- RESTful API endpoints for air quality data
- Caching system with Redis (fallback to local memory)
  - 30-minute TTL (configurable)
  - LRU eviction policy
  - Max 1000 cache entries (configurable)
  - Cache hit/miss statistics
- Integration with OpenWeatherMap Air Pollution API
- Error handling and logging
- CORS support for frontend

### Frontend (React + Vite)
- Modern UI design with glassmorphism effects
- Real-time city search with debouncing
- Color-coded AQI levels (Good to Very Poor)
- Detailed pollutant information with WHO guideline comparison
- 4-day hourly forecast visualization
- Cache indicators and response time display
- Fully responsive design
- Smooth animations

##  Data Provided

- Overall Air Quality Index (AQI): 1-5 scale with interpretation
- 8+ Pollutants: PM2.5, PM10, CO, NO, NO2, O3, SO2, NH3
- WHO Guideline Comparison: Shows if pollutants exceed safe limits
- 4-Day Forecast: Hourly predictions for next 96 hours
- Historical Context: Cache timestamps and response times

## API Selection: OpenWeatherMap

I chose OpenWeatherMap over AQICN for the following reasons:

| Feature | OpenWeatherMap | AQICN |
|---------|----------------|-------|
| Free Tier Limit | 1,000,000 calls/month | Limited |
| Pollutants | 8+ types | 6 types |
| Forecast | 4-day hourly | None |
| Historical | Since Nov 2020 | Limited |
| Global Coverage | Excellent | Good |
| Documentation | Comprehensive | Good |

## Technology Stack

### Backend
- Python 3.12+
- Django 4.2.7 - Web framework
- Django REST Framework 3.14 - API framework
- Redis 5.0 - Caching (with fallback to local memory)
- Requests 2.31 - HTTP client

### Frontend
- React 18 - UI framework
- Vite 7.2 - Build tool
- Axios - HTTP client
- Modern CSS - Responsive design with gradients & animations

## Prerequisites

Before running this project, make sure you have:

- Python 3.10+ installed
- Node.js 20.12+ and npm installed
- OpenWeatherMap API Key (free tier) - Get it from https://openweathermap.org/api
- (Optional) Redis Server - For better caching performance

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/air-quality.git
cd air-quality
```

### 2. Backend Setup

#### Navigate to backend directory
```bash
cd backend
```

#### Create and activate virtual environment

Windows:
```bash
python -m venv venv
.\\venv\\Scripts\\activate
```

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Configure environment variables

Create a `.env` file in the `backend` directory:

```env
# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY=your_api_key_here

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/1

# Cache Settings (TTL in seconds)
CACHE_TTL=1800
MAX_CACHE_ENTRIES=1000

# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

Note: Get your free API key from https://openweathermap.org/api

#### Run migrations
```bash
python manage.py migrate
```

#### Start the Django development server
```bash
python manage.py runserver
```

Backend will be running at http://localhost:8000

### 3. Frontend Setup

#### Open a new terminal and navigate to frontend directory
```bash
cd frontend
```

#### Install dependencies
```bash
npm install
```

#### Start the development server
```bash
npm run dev
```

Frontend will be running at http://localhost:5173

### 4. Open the Application

Open your browser and navigate to:
```
http://localhost:5173
```

## API Endpoints

Base URL: http://localhost:8000/api/v1/

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| GET | /search | Search city air quality | ?city=<city_name> |
| GET | /cache/stats | Get cache statistics | None |
| GET | /health | Health check | None |

### Example Requests

#### Search for a City
```bash
curl "http://localhost:8000/api/v1/search?city=London"
```

Response:
```json
{
 "status": "success",
  "data": {
    "city": "London",
    "country": "GB",
    "coordinates": {"lat": 51.5074, "lon": -0.1278},
    "aqi": {
      "value": 3,
      "level": "Moderate",
      "description": "Members of sensitive groups may experience health effects"
    },
    "pollutants": {
      "pm2_5": {
        "value": 15.5,
        "unit": "µg/m³",
        "who_guideline": 15,
        "exceeds_who": true,
        "percentage_of_guideline": 103.3
      }
      // ... more pollutants
    },
    "forecast": [...],
    "timestamp": 1732468980,
    "cached": false
  },
  "response_time_ms": 523.45,
  "from_cache": false
}
```

#### Get Cache Statistics
```bash
curl "http://localhost:8000/api/v1/cache/stats"
```

Response:
```json
{
  "status": "success",
  "data": {
    "hits": 45,
    "misses": 12,
    "total_requests": 57,
    "hit_rate": 78.95,
    "cache_enabled": true
  }
}
```

## UI Design

The application features:
- Glassmorphism: Frosted glass effect with backdrop blur
- Color-Coded AQI: Visual feedback based on air quality level
  - Good (1): Green
  - Fair (2): Yellow
  - Moderate (3): Orange
  - Poor (4): Red
  - Very Poor (5): Purple
- WHO Guidelines: Shows compliance with World Health Organization standards
- Dark Theme: Dark background with vibrant accents
- Responsive: Works on desktop, tablet, and mobile
- Smooth Animations: Fade-ins, slides, and hover effects

## Caching Strategy

### How It Works

1. First Request (Cache Miss):
   - User searches for "London"
   - Backend checks cache - Not found
   - Fetches from OpenWeather API (~500-1000ms)
   - Stores in cache with 30-minute TTL
   - Returns data to user

2. Subsequent Requests (Cache Hit):
   - User searches for "London" again
   - Backend checks cache - Found
   - Returns cached data instantly (<50ms)
   - Around 10-20x faster than API call

3. Cache Expiry:
   - After 30 minutes, cache entry expires
   - Next request fetches fresh data from API
   - Cycle repeats

4. Max Entries (LRU Eviction):
   - When cache reaches 1000 entries
   - Least Recently Used entry is removed
   - Ensures memory efficiency

### Performance

- Cache Hit: ~20-50ms response time
- Cache Miss: ~500-1000ms (API call)
- Improvement: Up to 20x faster for repeated queries
- Hit Rate: Typically 70-90% in production

## Testing

### Test the Backend API

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Search for New York
curl "http://localhost:8000/api/v1/search?city=New%20York"

# Get cache statistics
curl http://localhost:8000/api/v1/cache/stats
```

### Test Cache Behavior

1. Search for a city (e.g., "Tokyo")
2. Note the response time in the UI
3. Search for the same city again
4. Response time should be <50ms with "Cached Data" indicator

## Production Deployment

### Backend

1. Set DEBUG=False in .env
2. Use a production-grade WSGI server (e.g., Gunicorn)
3. Setup Redis for distributed caching
4. Configure proper SECRET_KEY
5. Use environment-based settings

### Frontend

```bash
cd frontend
npm run build
```

Serve the dist folder with a web server (Nginx, Apache, etc.)

## Project Structure

```
air-quality/
├── backend/
│   ├── api/
│   │   ├── cache_manager.py      # Cache logic with TTL & LRU
│   │   ├── services.py           # OpenWeather API integration
│   │   ├── serializers.py        # Data validation
│   │   ├── views.py              # API endpoints
│   │   └── urls.py               # Route configuration
│   ├── config/
│   │   ├── settings.py           # Django settings
│   │   └── urls.py               # Main URL config
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── services/
│   │   │   └── apiClient.js      # Axios API client
│   │   ├── utils/
│   │   │   └── helpers.js        # Utility functions
│   │   ├── App.jsx               # Main App component
│   │   └── index.css             # Styles
│   ├── package.json
│   └── vite.config.js
├── .gitignore
├── .env.example
└── README.md
```

## Implementation Details

### Backend

Cache Manager (api/cache_manager.py):
- Normalized cache keys for consistent lookups
- Statistics tracking (hits/misses/hit rate)
- Automatic TTL management
- Error handling with graceful fallback

OpenWeather Service (api/services.py):
- Geocoding for city name to coordinates conversion
- Air pollution data fetching
- 4-day forecast retrieval
- WHO guideline comparison logic
- Error handling

API Views (api/views.py):
- Input validation with serializers
- Cache-first approach
- Response time tracking
- Proper HTTP status codes

### Frontend

Debounced Search:
- 500ms delay before API call
- Prevents excessive requests while typing

Color Gradients:
- Dynamic backgrounds based on AQI value
- Smooth transitions between states

Responsive Grid:
- CSS Grid for pollutant cards
- Auto-fit layout for different screen sizes

## Redis (Optional)

If Redis is not installed, the application automatically falls back to Django's local memory cache. Redis is recommended for:
- Multi-server deployments
- Persistent caching across restarts
- Better performance under high load

To install Redis:

Windows:
Download from https://github.com/microsoftarchive/redis/releases

Mac:
```bash
brew install redis
brew services start redis
```

Linux:
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

## Troubleshooting

### "City not found" error
- Check spelling
- Try major cities first (e.g., "London", "Paris", "Tokyo")
- Ensure API key is valid

### "Invalid API key" error
- Verify .env file has correct OPENWEATHER_API_KEY
- Ensure API key is activated (can take 10-15 minutes after registration)

### Backend not starting
- Check Python version (3.10+)
- Ensure virtual environment is activated
- Run pip install -r requirements.txt again

### Frontend not connecting to backend
- Verify backend is running on http://localhost:8000
- Check browser console for CORS errors
- Ensure CORS is configured in Django settings

## License

This project is open source and available under the MIT License.

## Acknowledgments

- OpenWeatherMap for providing the Air Quality API
- World Health Organization for air quality guidelines
- Django and React communities for documentation

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub

---

Built using Django and React

Last Updated: November 2024
