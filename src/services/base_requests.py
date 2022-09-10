import requests_cache

from .constants import *
from requests.exceptions import ConnectionError
from requests.models import Response

class BaseClient:

    def _get_cached_session(self, token:str)->requests_cache.CachedSession:
        backend = requests_cache.RedisCache(host=REDIS_HOST, port=REDIS_PORT,password=REDIS_PASSWORD)
        session = requests_cache.CachedSession('client_cache',backend)
        session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': token,
        })
        return session


    def request_get(self, url:str, token:str, ttl:int = TLL_DEFAULT) -> Response:
        session = self._get_cached_session(token)

        try:
            return session.get(url, expire_after=ttl)
            
        except ConnectionError:
            return False
