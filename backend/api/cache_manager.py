# Cache Manager for Air Quality Data
# Handles caching with TTL and LRU eviction

from django.core.cache import cache
from django.conf import settings
import time
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    # Cache statistics
    _stats = {
        'hits': 0,
        'misses': 0,
        'total_requests': 0,
    }
    
    @staticmethod
    def _normalize_key(city_name):
        # Normalize city name for cache keys
        return f"city_{city_name.lower().strip().replace(' ', '_')}"
    
    @classmethod
    def get(cls, city_name):
        # Get cached data for a city
        cls._stats['total_requests'] += 1
        cache_key = cls._normalize_key(city_name)
        
        try:
            data = cache.get(cache_key)
            if data is not None:
                cls._stats['hits'] += 1
                logger.info(f"Cache HIT for city: {city_name}")
                return data
            else:
                cls._stats['misses'] += 1
                logger.info(f"Cache MISS for city: {city_name}")
                return None
        except Exception as e:
            logger.error(f"Cache retrieval error: {str(e)}")
            cls._stats['misses'] += 1
            return None
    
    @classmethod
    def set(cls, city_name, data, timeout=None):
        # Store data in cache
        cache_key = cls._normalize_key(city_name)
        
        if timeout is None:
            timeout = settings.CACHES['default']['TIMEOUT']
        
        try:
            data['cached_at'] = time.time()
            cache.set(cache_key, data, timeout)
            logger.info(f"Cached data for city: {city_name} (TTL: {timeout}s)")
        except Exception as e:
            logger.error(f"Cache storage error: {str(e)}")
    
    @classmethod
    def delete(cls, city_name):
        # Delete cached data for a city
        cache_key = cls._normalize_key(city_name)
        try:
            cache.delete(cache_key)
            logger.info(f"Deleted cache for city: {city_name}")
        except Exception as e:
            logger.error(f"Cache deletion error: {str(e)}")
    
    @classmethod
    def clear_all(cls):
        # Clear all cache
        try:
            cache.clear()
            cls._stats = {'hits': 0, 'misses': 0, 'total_requests': 0}
            logger.info("All cache cleared")
        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")
    
    @classmethod
    def get_stats(cls):
        # Get cache statistics
        total = cls._stats['total_requests']
        hit_rate = (cls._stats['hits'] / total * 100) if total > 0 else 0
        
        return {
            'hits': cls._stats['hits'],
            'misses': cls._stats['misses'],
            'total_requests': total,
            'hit_rate': round(hit_rate, 2),
            'cache_enabled': True,
        }
    
    @classmethod
    def reset_stats(cls):
        # Reset statistics
        cls._stats = {'hits': 0, 'misses': 0, 'total_requests': 0}
        logger.info("Cache statistics reset")

