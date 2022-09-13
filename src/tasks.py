from celery import Celery

from geoip.geoip_service import GeoIP
from rdap.rdap_service import RADP


app = Celery('tasks', broker='redis://cache:6379')


@app.task
def rdap_task(data, result_path):
    print("STARTING RADP PROCESS...")
    print(result_path)
    rdap = RADP(data)
    print(f"RADP RESULT: {rdap.process_rdap(result_file=result_path)}")
    print("PROCESS RADP COMPLETED.")
    return True

@app.task
def geoip_task(data,result_path):
    print("STARTING GEOIP PROCESS...")
    print(result_path)
    geoip = GeoIP(data)
    print(f"GEOIP RESULT: {geoip.process_geoip(result_file=result_path)}")
    print("PROCESS GEOIP COMPLETED.")
    return True
