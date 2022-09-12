from time import sleep
from services.base_requests import BaseClient
from .constants import *


class IpApiClient:

    def __init__(self) -> None:
        self.base_client = BaseClient()
        self.batch_url = IP_API_URL
        self.time_out = 0
    
    def get_geoip_batch(self, ip_list:list) -> dict:
        if len(ip_list) > IP_API_LIMIT_SIZE:
            return {"success": False, "error": f"ip list needs to have less than {IP_API_LIMIT_SIZE} elements"}

        if not self.take_time_out():
            return {"success": False, "error": "ip api unavailable"}

        response = self.base_client.request_post_with_cache(url=self.batch_url,data=ip_list, ttl=IP_API_CACHE_TTL)

        if response.status_code != 200:
            return {"success": False, "error": f"{response.status_code} status code"}

        if(int(response.headers.get('X-Rl',1)) == 0 and not response.from_cache):
            self.time_out = int(response.headers.get('X-Ttl',1)) + 1

        return {"success": True, "data": response.json()}
            
    def take_time_out(self) -> bool:
        if self.time_out > IP_API_TIMEOUT_LIMIT:
            return False

        if self.time_out > 0:
            sleep(self.time_out)
            self.time_out = 0
        return True

