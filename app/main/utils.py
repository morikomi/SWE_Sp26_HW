from flask import current_app
from sgp4.api import Satrec, jday
from datetime import datetime

def build_query(satellite_id):
    api_url="https://tle.ivanstanojevic.me/api/tle/"
    query = api_url + satellite_id
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    return (query, headers)

def parse_response(response):
    result={"msg":"", "satellite_id": "", "satellite_name": "", "line1":"", "line2":""}
    if response.status_code == 200:
        response_json = response.json()
        result["satellite_id"] = response_json["satelliteId"]
        result["satellite_name"] = response_json["name"]
        result["line1"] = response_json["line1"]
        result["line2"] = response_json["line2"]
        result["msg"] = "OK"
    else:
        result = None
    return result

def parse_satellite(tle_dict, input_date_time):
    # Convert TLE lines into a satellite object
    satellite = Satrec.twoline2rv(tle_dict["line1"], tle_dict["line2"])
    # Choose the target date/time in UTC (e.g., June 1, 2026 at 12:00:00 UTC)
    jd, fr = jday(input_date_time.year, input_date_time.month, input_date_time.day, input_date_time.hour, input_date_time.minute, input_date_time.second)
    # Calculate position (r) and velocity (v)
    error, r, v = satellite.sgp4(jd, fr)
    return (error, r, v)