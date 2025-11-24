"""
API URL Configuration
"""

from django.urls import path
from .views import SearchCityAPIView, CacheStatsAPIView, HealthCheckAPIView

urlpatterns = [
    path('search', SearchCityAPIView.as_view(), name='search-city'),
    path('cache/stats', CacheStatsAPIView.as_view(), name='cache-stats'),
    path('health', HealthCheckAPIView.as_view(), name='health-check'),
]
