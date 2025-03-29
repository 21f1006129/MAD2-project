from flask_caching import Cache

config = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_URL": "redis://localhost:6379/2",
    "CACHE_DEFAULT_TIMEOUT": 60
}


cache = Cache(config=config)