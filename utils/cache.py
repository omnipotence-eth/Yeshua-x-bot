import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SimpleCache:
    """Simple file-based cache to reduce API calls"""
    
    def __init__(self, cache_dir=".cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        logger.info(f"Cache initialized at {self.cache_dir}")
    
    def _get_cache_file(self, key):
        """Get cache file path for a key"""
        safe_key = "".join(c if c.isalnum() or c in ['_', '-'] else '_' for c in key)
        return self.cache_dir / f"{safe_key}.json"
    
    def get(self, key, max_age_minutes=10):
        """Get cached value if it exists and is not expired"""
        cache_file = self._get_cache_file(key)
        
        if not cache_file.exists():
            logger.debug(f"Cache miss: {key}")
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # Check if cache is expired
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            age = datetime.now() - cached_time
            
            if age > timedelta(minutes=max_age_minutes):
                logger.debug(f"Cache expired: {key} (age: {age})")
                return None
            
            logger.info(f"Cache hit: {key} (age: {age.seconds}s)")
            return cached_data['value']
        
        except Exception as e:
            logger.error(f"Cache read error for {key}: {e}")
            return None
    
    def set(self, key, value):
        """Store value in cache"""
        cache_file = self._get_cache_file(key)
        
        try:
            cached_data = {
                'timestamp': datetime.now().isoformat(),
                'value': value
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cached_data, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"Cache set: {key}")
        
        except Exception as e:
            logger.error(f"Cache write error for {key}: {e}")
    
    def clear(self):
        """Clear all cached data"""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            logger.info("Cache cleared")
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
    
    def clear_old(self, max_age_hours=24):
        """Remove cache files older than specified hours"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            count = 0
            
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                    
                    cached_time = datetime.fromisoformat(cached_data['timestamp'])
                    
                    if cached_time < cutoff_time:
                        cache_file.unlink()
                        count += 1
                
                except Exception:
                    # If we can't read it, delete it
                    cache_file.unlink()
                    count += 1
            
            if count > 0:
                logger.info(f"Cleared {count} old cache files")
        
        except Exception as e:
            logger.error(f"Error clearing old cache: {e}")

# Global cache instance
cache = SimpleCache()

