from functools import lru_cache
import pandas as pd
from datetime import datetime, timedelta

class DataCache:
    def __init__(self):
        self._cache = {}
        self._cache_time = {}
        self.CACHE_DURATION = timedelta(minutes=5)

    def get(self, key):
        if key in self._cache:
            if datetime.now() - self._cache_time[key] < self.CACHE_DURATION:
                return self._cache[key]
            else:
                del self._cache[key]
                del self._cache_time[key]
        return None

    def set(self, key, value):
        self._cache[key] = value
        self._cache_time[key] = datetime.now()

cache = DataCache()

@lru_cache(maxsize=32)
def cache_data_processing(func):
    def wrapper(*args, **kwargs):
        cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
        result = cache.get(cache_key)
        if result is None:
            result = func(*args, **kwargs)
            cache.set(cache_key, result)
        return result
    return wrapper