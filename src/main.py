
from time import sleep
from parser.parser_service import Parser
from tasks import rdap_task, geoip_task, app
from random import randint

RAW_DATA_PATH = "raw_data/list_of_ips.txt"
RESULT_GEOIP_PATH = f"../result_data/result_geoip_{randint(1,99999)}.txt"
RESULT_RDAP_PATH = f"../result_data/result_rdap_{randint(1,99999)}.txt"


def main():
    parser = Parser()
    result_parcer = parser.extract_ips_from_file(RAW_DATA_PATH)

    if result_parcer["success"]:
        geoip_task.delay(result_parcer["data"], RESULT_GEOIP_PATH)
        rdap_task.delay(result_parcer["data"], RESULT_RDAP_PATH)
    else:
        print(result_parcer)

    print(f"results of geoip search can be seen in {RESULT_GEOIP_PATH}")
    print(f"results of rdap search can be seen in {RESULT_RDAP_PATH}")

if __name__ == "__main__":
    main()