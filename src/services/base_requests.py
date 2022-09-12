import requests_cache
import json

from .constants import *
from requests.exceptions import ConnectionError
from requests.models import Response


class BaseClient:

    def _get_cached_session(self, token:str)->requests_cache.CachedSession:
        backend = requests_cache.RedisCache(host=REDIS_HOST, port=REDIS_PORT,password=REDIS_PASSWORD)
        session = requests_cache.CachedSession('client_cache',backend, allowable_methods=('GET', 'HEAD', 'POST'))
        session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': token,
        })
        return session


    def request_get(self, url:str, token:str=None, ttl:int = TLL_DEFAULT) -> Response:
        session = self._get_cached_session(token)

        try:
            return session.get(url, expire_after=ttl)
            
        except ConnectionError:
            response = Response()
            response.error_type = "connection error"
            response.status_code = 500
            response._content = b'{ "error" : "connection error" }'
            return response


    def request_post_with_cache(self, url:str,token:str=None, data:dict=None,  ttl:int = TLL_DEFAULT) -> Response:
        session = self._get_cached_session(token)

        try:
            return session.post(url, data = json.dumps(data), expire_after=ttl)
        except ConnectionError:
            response = Response()
            response.error_type = "connection error"
            response.status_code = 500
            response._content = b'{ "error" : "connection error" }'
            return response
