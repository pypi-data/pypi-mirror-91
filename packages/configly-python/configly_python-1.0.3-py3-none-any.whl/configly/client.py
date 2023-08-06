import time
from urllib.parse import urljoin

import requests

from .errors import ConfiglyConnectionError
from .errors import ConfiglyRequestError
from .errors import InvalidApiKeyError
from .version import VERSION

GET_API_PATH = '/api/v1/value'
GET_KEY_IDENTIFIER = 'keys[]'
GET_HEADERS = {
    'Accept': 'application/json',
    'X-Lib-Version': f'configly-python/{VERSION}',
}


class Client():
    """ Create a new Configly client."""

    def __init__(self, api_key=None, host='https://api.config.ly/', timeout=3, enable_cache=True):
        """ API Key is required. All others become instance defaults and are optional. """

        self.api_key = api_key
        self.host = host
        self.timeout = timeout
        self.enable_cache = enable_cache

        self.cache = {}
        self.cache_ttl = {}
        self.session = requests.session()

    def get(self, key, options={}):
        """
            Fetch a Config with the key. May make call Configly's backend servers if a value
            is not cached (or caching is disabled). Options is an optional dict that only applies
            to this call. Options are:
            - enable_cache - boolean
            - timeout - float for seconds before timing out
        """

        enable_cache = self.enable_cache
        if 'enable_cache' in options:
            enable_cache = bool(options['enable_cache'])

        # Returned cached value if appropriate (caching enabled, data is fresh).
        if enable_cache and key in self.cache and time.time() < self.cache_ttl[key]:
            return self.cache[key]

        timeout = options.get('timeout', self.timeout) or 3
        try:
            response = self.session.get(
                urljoin(self.host, GET_API_PATH),
                timeout=timeout,
                auth=(self.api_key, None),
                params={
                    GET_KEY_IDENTIFIER: key,
                },
                headers=GET_HEADERS,
            )
        except requests.exceptions.Timeout as error:
            if key in self.cache:  # Prefer a stale value over error
                return self.cache[key]
            raise ConfiglyConnectionError('Timeout', error)
        except requests.exceptions.ConnectionError as error:
            if key in self.cache:  # Prefer a stale value over error
                return self.cache[key]
            raise ConfiglyConnectionError(
                'Connection Error - Internet connection disrupted?', error,
            )

        if response.status_code == 401:
            raise InvalidApiKeyError(response.text)
        if response.status_code != 200:
            raise ConfiglyRequestError(response)

        json_response = response.json()
        data = json_response['data']
        if key not in data:
            return None

        ttl = data[key].get('ttl', 60)
        value = data[key]['value']

        # Store cached data if caching is enabled.
        if enable_cache:
            self.cache[key] = value
            self.cache_ttl[key] = time.time() + ttl

        return value
