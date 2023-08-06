from .client import Client

# Global options
api_key = None
timeout = 3
enable_cache = True
host = 'https://api.config.ly/'

default_client = None


def get(key, options={}):
    """
        Fetch a Config with the key. May make call Configly's backend servers if a value
        is not cached (or caching is disabled). Options is an optional dict that only applies
        to this call. Options are:
        - enable_cache - boolean
        - timeout - float for seconds before timing out
    """
    global default_client, api_key
    if not default_client:
        default_client = Client(
            api_key=api_key, host=host, timeout=timeout, enable_cache=enable_cache,
        )
    return default_client.get(key, options)
