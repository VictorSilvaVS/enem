import redis
from functools import wraps
import json
from datetime import timedelta

# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def cache_data(key_prefix, expire_time=300):  # 5 minutes default
    """
    Decorator to cache function results in Redis.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Create a unique cache key based on the function arguments
            cache_key = f"{key_prefix}:{json.dumps(args)}:{json.dumps(kwargs)}"
            
            # Try to get the cached result
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # If not cached, execute the function and cache the result
            result = f(*args, **kwargs)
            redis_client.setex(cache_key, timedelta(seconds=expire_time), json.dumps(result))
            return result
        return decorated_function
    return decorator

def clear_cache(key_pattern):
    """
    Clear cache entries matching a pattern.
    """
    keys = redis_client.keys(key_pattern)
    if keys:
        redis_client.delete(*keys)

def cache_user_progress(user_id, subject, data, expire_time=3600):  # 1 hour default
    """
    Cache user study progress.
    """
    cache_key = f"user_progress:{user_id}:{subject}"
    redis_client.setex(cache_key, timedelta(seconds=expire_time), json.dumps(data))

def get_cached_user_progress(user_id, subject):
    """
    Get cached user study progress.
    """
    cache_key = f"user_progress:{user_id}:{subject}"
    data = redis_client.get(cache_key)
    return json.loads(data) if data else None
