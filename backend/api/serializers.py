"""
API Serializers for Air Quality Data
"""

from rest_framework import serializers


class CoordinatesSerializer(serializers.Serializer):
    """Serializer for geographic coordinates"""
    lat = serializers.FloatField()
    lon = serializers.FloatField()


class AQISerializer(serializers.Serializer):
    """Serializer for Air Quality Index information"""
    value = serializers.IntegerField()
    level = serializers.CharField()
    description = serializers.CharField()


class PollutantSerializer(serializers.Serializer):
    """Serializer for individual pollutant data"""
    value = serializers.FloatField()
    unit = serializers.CharField()
    who_guideline = serializers.FloatField(required=False)
    exceeds_who = serializers.BooleanField(required=False)
    percentage_of_guideline = serializers.FloatField(required=False)


class ForecastItemSerializer(serializers.Serializer):
    """Serializer for forecast data item"""
    timestamp = serializers.IntegerField()
    aqi = serializers.IntegerField()
    pm25 = serializers.FloatField()
    pm10 = serializers.FloatField()


class AirQualityDataSerializer(serializers.Serializer):
    """Serializer for complete air quality response"""
    city = serializers.CharField()
    country = serializers.CharField()
    coordinates = CoordinatesSerializer()
    aqi = AQISerializer()
    pollutants = serializers.DictField(child=PollutantSerializer())
    forecast = ForecastItemSerializer(many=True)
    timestamp = serializers.IntegerField()
    cached = serializers.BooleanField(default=False)
    cached_at = serializers.FloatField(required=False)


class ErrorSerializer(serializers.Serializer):
    """Serializer for error responses"""
    status = serializers.CharField(default='error')
    message = serializers.CharField()
    code = serializers.CharField(required=False)


class CacheStatsSerializer(serializers.Serializer):
    """Serializer for cache statistics"""
    hits = serializers.IntegerField()
    misses = serializers.IntegerField()
    total_requests = serializers.IntegerField()
    hit_rate = serializers.FloatField()
    cache_enabled = serializers.BooleanField()


class CitySearchSerializer(serializers.Serializer):
    """Serializer for city search input validation"""
    city = serializers.CharField(
        max_length=100,
        required=True,
        error_messages={
            'required': 'City name is required',
            'blank': 'City name cannot be empty',
            'max_length': 'City name is too long'
        }
    )
    
    def validate_city(self, value):
        """Validate and clean city name"""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("City name cannot be empty")
        if len(value) < 2:
            raise serializers.ValidationError("City name must be at least 2 characters")
        return value
