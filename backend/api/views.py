# API Views for Air Quality Search Engine

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import time
import logging

from .services import OpenWeatherService
from .cache_manager import CacheManager
from .serializers import (
    CitySearchSerializer,
    AirQualityDataSerializer,
    ErrorSerializer,
    CacheStatsSerializer
)

logger = logging.getLogger(__name__)


class SearchCityAPIView(APIView):
    # API endpoint for searching city air quality data
    # GET /api/v1/search?city=<city_name>
    
    def get(self, request):
        # Handle GET request for city air quality search
        
        start_time = time.time()
        
        # Validate input
        search_serializer = CitySearchSerializer(data=request.query_params)
        if not search_serializer.is_valid():
            error_data = {
                'status': 'error',
                'message': 'Invalid request parameters',
                'errors': search_serializer.errors
            }
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
        
        city_name = search_serializer.validated_data['city']
        
        try:
            # Check cache first
            cached_data = CacheManager.get(city_name)
            
            if cached_data:
                # Return cached data
                cached_data['cached'] = True
                response_time = round((time.time() - start_time) * 1000, 2)  # ms
                
                logger.info(f"Returned cached data for '{city_name}' in {response_time}ms")
                
                return Response({
                    'status': 'success',
                    'data': cached_data,
                    'response_time_ms': response_time,
                    'from_cache': True
                }, status=status.HTTP_200_OK)
            
            # Cache miss - fetch from API
            weather_service = OpenWeatherService()
            air_quality_data = weather_service.get_air_quality_by_city(city_name)
            
            # Store in cache
            CacheManager.set(city_name, air_quality_data)
            
            # Add cache indicator
            air_quality_data['cached'] = False
            
            response_time = round((time.time() - start_time) * 1000, 2)  # ms
            
            logger.info(f"Fetched fresh data for '{city_name}' in {response_time}ms")
            
            return Response({
                'status': 'success',
                'data': air_quality_data,
                'response_time_ms': response_time,
                'from_cache': False
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            error_message = str(e)
            logger.error(f"Error searching for city '{city_name}': {error_message}")
            
            # Determine appropriate status code
            if 'not found' in error_message.lower():
                status_code = status.HTTP_404_NOT_FOUND
                error_code = 'CITY_NOT_FOUND'
            elif 'api key' in error_message.lower():
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                error_code = 'API_KEY_ERROR'
            elif 'timeout' in error_message.lower():
                status_code = status.HTTP_504_GATEWAY_TIMEOUT
                error_code = 'REQUEST_TIMEOUT'
            else:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                error_code = 'SERVER_ERROR'
            
            error_data = {
                'status': 'error',
                'message': error_message,
                'code': error_code
            }
            
            return Response(error_data, status=status_code)


class CacheStatsAPIView(APIView):
    # API endpoint for cache statistics
    # GET /api/v1/cache/stats
    
    def get(self, request):
        # Handle GET request for cache statistics
        
        if not settings.CACHE_STATS_ENABLED:
            return Response({
                'status': 'error',
                'message': 'Cache statistics are disabled'
            }, status=status.HTTP_403_FORBIDDEN)
        
        stats = CacheManager.get_stats()
        
        serializer = CacheStatsSerializer(stats)
        
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def delete(self, request):
        # Reset cache statistics
        
        CacheManager.reset_stats()
        
        return Response({
            'status': 'success',
            'message': 'Cache statistics reset successfully'
        }, status=status.HTTP_200_OK)


class HealthCheckAPIView(APIView):
    # Health check endpoint
    # GET /api/v1/health
    
    def get(self, request):
        # Handle GET request for health check
        
        # Check if API key is configured
        api_key_configured = bool(settings.OPENWEATHER_API_KEY)
        
        health_data = {
            'status': 'healthy',
            'api_key_configured': api_key_configured,
            'cache_enabled': True,
            'timestamp': int(time.time())
        }
        
        return Response(health_data, status=status.HTTP_200_OK)
