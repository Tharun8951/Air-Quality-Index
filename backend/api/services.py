# OpenWeatherMap API Service
# Handles all interactions with OpenWeatherMap API

import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class OpenWeatherService:
    
    # AQI Level interpretations based on index value
    AQI_LEVELS = {
        1: {'level': 'Good', 'description': 'Air quality is satisfactory, and air pollution poses little or no risk'},
        2: {'level': 'Fair', 'description': 'Air quality is acceptable for most people'},
        3: {'level': 'Moderate', 'description': 'Members of sensitive groups may experience health effects'},
        4: {'level': 'Poor', 'description': 'Everyone may begin to experience health effects'},
        5: {'level': 'Very Poor', 'description': 'Health alert: everyone may experience more serious health effects'},
    }
    
    # WHO recommended air quality guidelines (µg/m³)
    WHO_GUIDELINES = {
        'pm25': 15,
        'pm10': 45,
        'no2': 25,
        'o3': 100,
        'so2': 40,
    }
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.geo_url = settings.OPENWEATHER_GEO_URL
        self.pollution_url = settings.OPENWEATHER_POLLUTION_URL
        self.timeout = 10  # seconds
    
    def _make_request(self, url, params):
        print('inside _make_request apikey -->', self.api_key)
        # Make HTTP request to OpenWeatherMap API
        params['appid'] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout for URL: {url}")
            raise Exception("API request timed out. Please try again.")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise Exception("Invalid API key. Please check your configuration.")
            elif response.status_code == 404:
                raise Exception("City not found. Please check the city name.")
            else:
                logger.error(f"HTTP error: {e}")
                raise Exception(f"API error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            raise Exception("Unable to connect to weather service. Please try again later.")
    
    def get_coordinates(self, city_name):
        # Get coordinates for a city using Geocoding API
        url = f"{self.geo_url}/direct"
        params = {
            'q': city_name,
            'limit': 1
        }
        
        data = self._make_request(url, params)
        
        if not data or len(data) == 0:
            raise Exception(f"City '{city_name}' not found. Please check the spelling.")
        
        location = data[0]
        return (
            location['lat'],
            location['lon'],
            location.get('name', city_name),
            location.get('country', 'Unknown')
        )
    
    def get_air_pollution(self, lat, lon):
        # Get current air pollution data for coordinates
        url = f"{self.pollution_url}/air_pollution"
        params = {
            'lat': lat,
            'lon': lon
        }
        
        data = self._make_request(url, params)
        
        if not data or 'list' not in data or len(data['list']) == 0:
            raise Exception("No air quality data available for this location.")
        
        return data['list'][0]
    
    def get_air_pollution_forecast(self, lat, lon):
        # Get 4-day hourly forecast
        url = f"{self.pollution_url}/air_pollution/forecast"
        params = {
            'lat': lat,
            'lon': lon
        }
        
        data = self._make_request(url, params)
        
        if not data or 'list' not in data:
            return []
        
        return data['list']
    
    def _format_pollutant_data(self, components):
        # Format pollutant data with WHO guideline comparison
        formatted = {}
        
        for key, value in components.items():
            pollutant = {
                'value': round(value, 2),
                'unit': 'µg/m³' if key != 'no' else 'μg/m³'
            }
            
            # Add WHO guideline comparison where applicable
            if key in self.WHO_GUIDELINES:
                guideline = self.WHO_GUIDELINES[key]
                pollutant['who_guideline'] = guideline
                pollutant['exceeds_who'] = value > guideline
                pollutant['percentage_of_guideline'] = round((value / guideline) * 100, 1)
            
            formatted[key] = pollutant
        
        return formatted
    
    def get_air_quality_by_city(self, city_name):
        # Get comprehensive air quality data for a city
        # Get coordinates
        lat, lon, city, country = self.get_coordinates(city_name)
        
        # Get current air pollution
        current_data = self.get_air_pollution(lat, lon)
        
        # Get forecast data
        forecast_data = self.get_air_pollution_forecast(lat, lon)
        
        # Extract AQI information
        aqi_value = current_data['main']['aqi']
        aqi_info = self.AQI_LEVELS.get(aqi_value, {
            'level': 'Unknown',
            'description': 'Air quality index not available'
        })
        
        # Format pollutant data
        pollutants = self._format_pollutant_data(current_data['components'])
        
        # Format forecast (take hourly data for next 96 hours - 4 days)
        forecast = []
        for item in forecast_data[:96]:  # Limit to 96 hours
            forecast.append({
                'timestamp': item['dt'],
                'aqi': item['main']['aqi'],
                'pm25': item['components'].get('pm2_5', 0),
                'pm10': item['components'].get('pm10', 0),
            })
        
        return {
            'city': city,
            'country': country,
            'coordinates': {
                'lat': lat,
                'lon': lon
            },
            'aqi': {
                'value': aqi_value,
                'level': aqi_info['level'],
                'description': aqi_info['description']
            },
            'pollutants': pollutants,
            'forecast': forecast,
            'timestamp': current_data['dt']
        }
