# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Endpoints

### 1. Search City Air Quality

Search for air quality data by city name.

**Endpoint:** `GET /search`

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| city | string | Yes | Name of the city to search (min 2 characters) |

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/search?city=London"
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "city": "London",
    "country": "GB",
    "coordinates": {
      "lat": 51.5074,
      "lon": -0.1278
    },
    "aqi": {
      "value": 3,
      "level": "Moderate",
      "description": "Members of sensitive groups may experience health effects"
    },
    "pollutants": {
      "co": {
        "value": 250.5,
        "unit": "µg/m³"
      },
      "no": {
        "value": 5.2,
        "unit": "µg/m³"
      },
      "no2": {
        "value": 12.1,
        "unit": "µg/m³",
        "who_guideline": 25,
        "exceeds_who": false,
        "percentage_of_guideline": 48.4
      },
      "o3": {
        "value": 45.2,
        "unit": "µg/m³",
        "who_guideline": 100,
        "exceeds_who": false,
        "percentage_of_guideline": 45.2
      },
      "so2": {
        "value": 3.4,
        "unit": "µg/m³",
        "who_guideline": 40,
        "exceeds_who": false,
        "percentage_of_guideline": 8.5
      },
      "pm2_5": {
        "value": 15.5,
        "unit": "µg/m³",
        "who_guideline": 15,
        "exceeds_who": true,
        "percentage_of_guideline": 103.3
      },
      "pm10": {
        "value": 22.3,
        "unit": "µg/m³",
        "who_guideline": 45,
        "exceeds_who": false,
        "percentage_of_guideline": 49.6
      },
      "nh3": {
        "value": 1.2,
        "unit": "µg/m³"
      }
    },
    "forecast": [
      {
        "timestamp": 1732468800,
        "aqi": 3,
        "pm25": 15.5,
        "pm10": 22.3
      }
      // ... up to 96 hourly forecasts
    ],
    "timestamp": 1732468980,
    "cached": false
  },
  "response_time_ms": 523.45,
  "from_cache": false
}
```

**Error Responses:**

**404 Not Found** - City not found:
```json
{
  "status": "error",
  "message": "City 'InvalidCityName' not found. Please check the spelling.",
  "code": "CITY_NOT_FOUND"
}
```

**400 Bad Request** - Invalid parameters:
```json
{
  "status": "error",
  "message": "Invalid request parameters",
  "errors": {
    "city": ["City name is required"]
  }
}
```

**500 Internal Server Error** - Server error:
```json
{
  "status": "error",
  "message": "Unable to connect to weather service. Please try again later.",
  "code": "SERVER_ERROR"
}
```

**504 Gateway Timeout** - API timeout:
```json
{
  "status": "error",
  "message": "API request timed out. Please try again.",
  "code": "REQUEST_TIMEOUT"
}
```

---

### 2. Cache Statistics

Get caching system statistics.

**Endpoint:** `GET /cache/stats`

**Query Parameters:** None

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/cache/stats"
```

**Success Response (200 OK):**
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

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| hits | integer | Number of cache hits |
| misses | integer | Number of cache misses |
| total_requests | integer | Total number of requests |
| hit_rate | float | Percentage of requests served from cache |
| cache_enabled | boolean | Whether caching is enabled |

---

### 3. Health Check

Check API health status.

**Endpoint:** `GET /health`

**Query Parameters:** None

**Example Request:**
```bash
curl "http://localhost:8000/api/v1/health"
```

**Success Response (200 OK):**
```json
{
  "status": "healthy",
  "api_key_configured": true,
  "cache_enabled": true,
  "timestamp": 1732468980
}
```

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| status | string | Health status ("healthy" or "unhealthy") |
| api_key_configured | boolean | Whether OpenWeather API key is set |
| cache_enabled | boolean | Whether caching is enabled |
| timestamp | integer | Current Unix timestamp |

---

## Data Models

### AQI (Air Quality Index)

| Value | Level | Description |
|-------|-------|-------------|
| 1 | Good | Air quality is satisfactory, and air pollution poses little or no risk |
| 2 | Fair | Air quality is acceptable for most people |
| 3 | Moderate | Members of sensitive groups may experience health effects |
| 4 | Poor | Everyone may begin to experience health effects |
| 5 | Very Poor | Health alert: everyone may experience more serious health effects |

### Pollutants

| Pollutant | Full Name | WHO Guideline (µg/m³) |
|-----------|-----------|----------------------|
| pm2_5 | Fine Particulate Matter (PM2.5) | 15 |
| pm10 | Particulate Matter (PM10) | 45 |
| no2 | Nitrogen Dioxide | 25 |
| o3 | Ozone | 100 |
| so2 | Sulfur Dioxide | 40 |
| co | Carbon Monoxide | - |
| no | Nitrogen Monoxide | - |
| nh3 | Ammonia | - |

### Coordinates

| Field | Type | Description |
|-------|------|-------------|
| lat | float | Latitude (-90 to 90) |
| lon | float | Longitude (-180 to 180) |

---

## Rate Limiting

The application uses OpenWeatherMap's free tier:
- **Limit:** 1,000,000 calls/month
- **Rate:** ~31 calls/minute on average

However, with caching enabled (30-minute TTL):
- Most requests are served from cache
- Actual API calls reduced by 80-90%
- Effective capacity: millions of user requests/month

---

## Caching Behavior

### Cache Key Format
```
aqi_city_{normalized_city_name}
```

Example: `aqi_city_new_york`

### Cache TTL (Time To Live)
- **Default:** 1800 seconds (30 minutes)
- **Configurable:** Set `CACHE_TTL` in `.env`

### Cache Indicators

The response includes cache metadata:

```json
{
  "data": {
    // ... air quality data
    "cached": true,
    "cached_at": 1732468980.123
  },
  "from_cache": true
}
```

| Field | Type | Description |
|-------|------|-------------|
| cached | boolean | Whether this data was cached |
| cached_at | float | Unix timestamp when data was cached |
| from_cache | boolean | Whether this response came from cache |

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| CITY_NOT_FOUND | 404 | City name not recognized |
| API_KEY_ERROR | 500 | Invalid or missing API key |
| REQUEST_TIMEOUT | 504 | API request timed out (10s) |
| SERVER_ERROR | 500 | General server error |

---

## Response Times

### Typical Performance

| Scenario | Response Time |
|----------|--------------|
| Cache Hit | 20-50ms |
| Cache Miss (API call) | 500-1000ms |
| Error Response | <10ms |

### Factors Affecting Performance

- **Network latency** to OpenWeatherMap servers
- **Cache status** (hit vs miss)
- **Redis availability** (local memory is slightly slower)
- **Database load** (minimal impact)

---

## Example Use Cases

### 1. Basic City Search

```javascript
// JavaScript example
const searchCity = async (cityName) => {
  const response = await fetch(
    `http://localhost:8000/api/v1/search?city=${encodeURIComponent(cityName)}`
  );
  const data = await response.json();
  
  if (data.status === 'success') {
    console.log(`AQI for ${data.data.city}: ${data.data.aqi.value}`);
    console.log(`Level: ${data.data.aqi.level}`);
  } else {
    console.error(`Error: ${data.message}`);
  }
};

await searchCity('Tokyo');
```

### 2. Checking Cache Performance

```javascript
// Python example
import requests
import time

def test_cache_performance(city):
    base_url = 'http://localhost:8000/api/v1'
    
    # First request (cache miss)
    start = time.time()
    response1 = requests.get(f'{base_url}/search', params={'city': city})
    time1 = (time.time() - start) * 1000
    
    # Second request (cache hit)
    start = time.time()
    response2 = requests.get(f'{base_url}/search', params={'city': city})
    time2 = (time.time() - start) * 1000
    
    print(f'First request (cold): {time1:.2f}ms')
    print(f'Second request (cached): {time2:.2f}ms')
    print(f'Speedup: {time1/time2:.1f}x faster')

test_cache_performance('Paris')
```

### 3. Monitoring Cache Statistics

```bash
# Bash script
#!/bin/bash

while true; do
  curl -s "http://localhost:8000/api/v1/cache/stats" | jq '.data'
  sleep 5
done
```

---

## Best Practices

### For Developers

1. **Always handle errors gracefully**
   - Check `status` field in response
   - Display user-friendly error messages

2. **Implement debouncing for search inputs**
   - Wait 300-500ms before API call
   - Prevents excessive requests

3. **Show loading states**
   - Indicate to users that data is loading
   - Disable inputs during fetch

4. **Display cache indicators**
   - Show users when data is from cache
   - Include timestamp for freshness

5. **Monitor performance**
   - Track response times
   - Log cache hit rates
   - Alert on high API usage

### For Production

1. **Use environment variables**
   - Never commit API keys
   - Use `.env` files

2. **Enable Redis**
   - Better performance than local memory
   - Survives server restarts

3. **Set appropriate cache TTL**
   - Balance freshness vs API usage
   - 30 minutes is recommended

4. **Monitor API quota**
   - Track monthly usage
   - Set up alerts near limits

5. **Implement retry logic**
   - Handle transient failures
   - Exponential backoff

---

## Testing the API

### Using cURL

```bash
# Search for London
curl "http://localhost:8000/api/v1/search?city=London"

# With pretty printing
curl "http://localhost:8000/api/v1/search?city=London" | jq

# Check cache stats
curl "http://localhost:8000/api/v1/cache/stats" | jq

# Health check
curl "http://localhost:8000/api/v1/health" | jq
```

### Using Python Requests

```python
import requests

# Search
response = requests.get(
    'http://localhost:8000/api/v1/search',
    params={'city': 'New York'}
)
data = response.json()
print(data)

# Cache stats
stats = requests.get('http://localhost:8000/api/v1/cache/stats').json()
print(f"Hit rate: {stats['data']['hit_rate']}%")
```

### Using Postman

1. Import collection:
   - Method: GET
   - URL: `http://localhost:8000/api/v1/search`
   - Params: `city = London`

2. Send request and inspect response

---

## Changelog

### Version 1.0.0 (November 2024)
- Initial release
- City search with caching
- 8+ pollutants
- 4-day forecast
- WHO guideline comparison
- Cache statistics
- Health check endpoint

---

## Support

For API-related questions:
1. Check this documentation
2. Review the README.md
3. Test with provided examples
4. Open an issue on GitHub

---

**Last Updated:** November 2024
