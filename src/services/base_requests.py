import requests_cache

from requests.exceptions import ConnectionError


class BaseClient:

    def _get_cached_session(self, token):
        session = requests_cache.CachedSession('client_cache')
        session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': token,
        })
        return session


    def _request_get(self, url, token, ttl = None):
        session = self._get_cached_session(token)

        try:
            response = session.get(url, expire_after=ttl)
            
        except ConnectionError:
            return False

        return response
