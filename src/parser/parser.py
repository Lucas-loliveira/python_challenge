from typing import List
import re


class Parcer:

    def extract_ips_from_file(self, file_path: str) -> List:
        ip_list=[]
        content = self.open_file_from_path(file_path)

        for line in content:
            ip_list.extend(self.extract_ips(line))

        return ip_list


    def open_file_from_path(self, file_path:str) -> List:
        try:
            with open(file_path) as f:
                return f.readlines()
        except FileNotFoundError as e:
            raise e


    def extract_ips(self, data:str) -> List:
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        return pattern.findall(data)
