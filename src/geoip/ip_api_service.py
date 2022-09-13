from time import sleep
from services.base_requests import BaseClient
from .constants import IP_API_URL, IP_API_LIMIT_SIZE,IP_API_TIMEOUT_LIMIT,IP_API_CACHE_TTL


class IpApiClient:
    '''The batch function allows 15 requests per minute.
        that's why it was necessary to implement the take_time_out method, 
        which waits for the ttl from the request when the number of remaining requests (X-Rl)
        see more in "Usage limits" in  https://ip-api.com/docs/api:batch
         reaches zero
    '''
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
        print({
            "service": "geoip",
            "status": response.status_code,
            "self.time_out": self.time_out,
            "X-Ttl": int(response.headers.get('X-Ttl',1)),
            "X-Rl": int(response.headers.get('X-Rl',1)),
            "response_cache_hit": response.from_cache
	        })
        return {"success": True, "data": response.json()}
            
    def take_time_out(self) -> bool:
        if self.time_out > IP_API_TIMEOUT_LIMIT:
            return False

        if self.time_out > 0:
            print(f"ip request need to take a timeout of {self.time_out} seconds")
            sleep(self.time_out)
            self.time_out = 0
        return True

