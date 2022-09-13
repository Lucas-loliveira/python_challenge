
import re


class Parser:

    def extract_ips_from_file(self, file_path: str) -> dict:
        ip_list=[]
        content = self.open_file_from_path(file_path)
        if not content:
            return {"success": False, "error":"file_not_found"}

        for line in content:
            ip_list.extend(self.extract_ips(line))

        return {"success": True, "data":ip_list}


    def open_file_from_path(self, file_path:str) -> list:
        try:
            with open(file_path) as f:
                return f.readlines()
        except FileNotFoundError as e:
            return []


    def extract_ips(self, data:str) -> list:
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        return pattern.findall(data)
