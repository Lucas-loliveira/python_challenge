import asyncio

from parser.parser_service import Parcer
from geoip.geoip_service import GeoIP
from rdap.rdap_service import RADP


def main():
    p = Parcer()
    result_parcer = p.extract_ips_from_file("raw_data/list_of_ips.txt")

    if result_parcer["success"]:
            
        geoip = GeoIP(result_parcer["data"])
        print(geoip.process_geoip(result_file="result_data/result_geoip_example.txt"))


        rdap = RADP(result_parcer["data"])
        print(rdap.process_rdap(result_file="result_data/result_rdap_example.txt"))
    else:
        print(result_parcer)
