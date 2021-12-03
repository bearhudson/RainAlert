#!/usr/bin/python

import requests
import os
import datetime as datetime
import json
import time
from email_message import email_message

API_KEY = os.environ.get("OPENWEATHER_API_KEY")
ZIPCODE = os.environ.get("ZIPCODE")
HOURS = int(os.environ.get("HOURS"))
SLEEP = 3600

# load cond list
with open("condition_codes.json", mode='r') as file:
    cond_json = json.load(file)

# load lat/lon from zip
payload = {
    'zip': ZIPCODE,
    'appid': API_KEY
}
zip_request = requests.get(url='http://api.openweathermap.org/geo/1.0/zip', params=payload)
zip_request.raise_for_status()
zip_json = zip_request.json()

in_processing = True
while in_processing:
    payload = {
        "lat": zip_json['lat'],
        "lon": zip_json['lon'],
        "appid": API_KEY,
        "exclude": "daily,current,minutely,alerts",
    }
    request_api = requests.get(url=f'https://api.openweathermap.org/data/2.5/onecall', params=payload)
    request_api.raise_for_status()
    api_response_json = request_api.json()
    now = time.time()
    now_formatted = datetime.datetime.fromtimestamp(now).strftime('%H:%M--%y/%m/%d')
    cond_sum = 0
    cur_fc_txt = ""
    print(f"\nT: {now_formatted}")
    weather_slice = api_response_json['hourly'][:HOURS]
    for hour_weather in weather_slice:
        cur_fc_time = hour_weather['dt']
        cur_fc = hour_weather['weather'][0]['id']
        time_converted = datetime.datetime.fromtimestamp(cur_fc_time).strftime('%H')
        cond_sum += cur_fc
        for cond in cond_json:
            if cur_fc == cond['code']:
                cur_fc_txt = cond['description']
        print(f"{time_converted} o'clock forecast: {cur_fc_txt}")
        if cur_fc <= 622:
            email_message(f"Possible Precipitation soon!\n{time_converted} o'clock"
                          f" forecast: {cur_fc_txt}\nT: {now_formatted}")

    cur_cond = "Error"
    if cond_sum <= 232 * HOURS:
        cur_cond = "Thunderstorms"
    elif cond_sum <= 321 * HOURS:
        cur_cond = "Drizzle"
    elif cond_sum <= 531 * HOURS:
        cur_cond = "Rain"
    elif cond_sum <= 622 * HOURS:
        cur_cond = "Snow"
    elif cond_sum <= 781 * HOURS:
        cur_cond = "Extreme Event!"
    elif cond_sum <= 804 * HOURS:
        cur_cond = "None Forecasted"
    print(f"Overall Precipitation: {cur_cond}")
    time.sleep(SLEEP)
