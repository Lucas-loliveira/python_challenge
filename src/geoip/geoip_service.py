
from .ip_api_service import IpApiClient

from .constants import BATCH_SIZE

class GeoIP:
    def __init__(self, ip_list:list) -> None:
        self.ip_list = ip_list
        self.len_ip_list = len(ip_list)
        self.ip_client = IpApiClient()

    def process_geoip(self, result_file:str)-> dict:
        for batch in self.get_batch_from_ip_list(BATCH_SIZE):
            result = self.ip_client.get_geoip_batch(batch)
            if not result["success"]:
                return {"success": False, "error":f"ip api return {result['error']}"}
            write_result = self.write_result_file(result_file, result["data"])
            if not write_result["success"]:
                return write_result

        return {"success": True, "data":result_file}
    
    def get_batch_from_ip_list(self, batch_size:int=1)-> list:
        for ndx in range(0, self.len_ip_list, batch_size):
            yield self.ip_list[ndx:min(ndx + batch_size, self.len_ip_list)]
    
    def write_result_file(self, file_path:str, data:str) -> dict:
        try:
            with open(file_path, 'a') as file:  
                file.write(str(data))
                file.write('\n')
            file.close()
            return {"success": True}
        except FileNotFoundError as e:
            return {"success": False, "error": f"result_file not found"}

