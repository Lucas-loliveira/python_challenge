from .api_rdap_client import RDAPApiClient


class RADP:
    def __init__(self, ip_list:list) -> None:
        self.ip_list = ip_list
        self.rdap_client = RDAPApiClient()


    def process_rdap(self, result_file:str)-> dict:

        for index,ip in enumerate(self.ip_list):
            print(f"rdap: processing {index+1}/{len(self.ip_list)} ip")
            response = self.rdap_client.get_rdap_from_ip(ip)
            write_result = self.write_result_file(result_file, response)
            if not write_result["success"]:
                return write_result
        return {"success": True, "data":result_file}


    def write_result_file(self, file_path:str, data:str) -> None:
        try:
            with open(file_path, 'a') as file:  
                file.write(str(data))
                file.write('\n')
            file.close()
            return {"success": True}
        except FileNotFoundError as e:
            return {"success": False, "error": f"result_file not found"}


