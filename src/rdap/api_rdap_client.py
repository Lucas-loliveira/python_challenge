from services.base_requests import BaseClient

from .constants import *

class RDAPApiClient:
    def __init__(self) -> None:
        self.base_client = BaseClient()
        self.url = RDAP_API_URL

    def get_rdap_from_ip(self, ip):
        response = self.base_client.request_get(url=self.url+ip,ttl=RDAP_API_CACHE_TTL)
        print({
            "service": "rdap",
            "status": response.status_code,
            "response_cache_hit": response.from_cache,
            "query": ip
	    })
        if response.status_code != 200:
            return {"success": False, "status_code": response.status_code, "query": ip}
        result = response.json()
        result["success"] = True
        return result
