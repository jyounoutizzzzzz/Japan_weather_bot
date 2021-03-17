from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
    MessageEvent,
    TextMessage,
    FlexSendMessage,
    TextSendMessage 
)
import os
from linebot.models.send_messages import TextSendMessage
import requests
from datetime import datetime
import re
import json
from django.template.loader import render_to_string


def keys():
    YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
    YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
    line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(YOUR_CHANNEL_SECRET)
    API_KEY = os.environ["API_KEY"]
    return line_bot_api, handler, API_KEY

handler = keys()[1]




@csrf_exempt
def callback(request):
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        HttpResponseForbidden()
    return HttpResponse('OK', status=200)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    line_bot_api = keys()[0]
    if result(event):
        city_name = result(event).group(1)
        geo_data = geometry_data(city_name)
        try:
            city_title, city_lon, city_lat = city_lat_lon(geo_data, city_name)
        except UnboundLocalError:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="キーワード\"{}\"に該当する地名のデータを取得することが出来ませんでした".format(city_name)))
        temp, feels_like, temp_min, temp_max, humidity, wind_speed, wind_deg, sunrise, sunset, text, rain, snow, hourly_time, hourly_text, hourly_temp, daily_day, daily_text, daily_max, daily_min, daily_morn, daily_eve, daily_night, daily_humidity, daily_deg, daily_speed, daily_rain, daily_snow= extract_data(data(city_lat,city_lon))

        main = render_to_string("weather.json", {"text": text, "city_title": city_title, "sunrise": utc_to_jp(sunrise), "sunset": utc_to_jp(sunset), "temp": temp, "feels_like": feels_like, "temp_max": temp_max, "temp_min": temp_min, "humidity": humidity, "wind_deg": degree(wind_deg), "wind_speed": wind_speed, "rain": rain, "snow": snow, "city_title": city_title, "city_lat": city_lat, "city_lon": city_lon})
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="main", contents=json.loads(main)))


        hourly = render_to_string("hourly_weather.json", {"1_": hourly_time[0], "2_": hourly_time[1], "3_": hourly_time[2], "4_": hourly_time[3], "5_": hourly_time[4], "6_": hourly_time[5], "7_": hourly_time[6], "8_": hourly_time[7], "9_": hourly_time[8], "10_": hourly_time[9], "11_": hourly_time[10], "12_": hourly_time[11], 
                                        "1_text": hourly_text[0], "2_text": hourly_text[1], "3_text": hourly_text[2], "4_text": hourly_text[3], "5_text": hourly_text[4], "6_text": hourly_text[5], "7_text": hourly_text[6], "8_text": hourly_text[7], "9_text": hourly_text[8], "10_text": hourly_text[9], "11_text": hourly_text[10], "12_text": hourly_text[11], 
                                                "1_temp": hourly_temp[0], "2_temp": hourly_temp[1], "3_temp": hourly_temp[2], "4_temp": hourly_temp[3], "5_temp": hourly_temp[4], "6_temp": hourly_temp[5], "7_temp": hourly_temp[6], "8_temp": hourly_temp[7],"9_temp": hourly_temp[8], "10_temp": hourly_temp[9], "11_temp": hourly_temp[10],"12_temp": hourly_temp[11],})
        line_bot_api.push_message(event.source.user_id, FlexSendMessage(alt_text="hourly", contents=json.loads(hourly)))


        weekly = render_to_string("weekly_weather.json", {"day_1": daily_day[0],"text_1": daily_text[0],"max_1": daily_max[0],"min_1": daily_min[0],"moring_1": daily_morn[0],"eve_1": daily_eve[0],"night_1": daily_night[0],"humidity_1": daily_humidity[0],"deg_1": daily_deg[0],"speed_1": daily_speed[0],"rain_1": daily_rain[0],"snow_1": daily_snow[0],
                                                                    "day_2": daily_day[1],"text_2": daily_text[1],"max_2": daily_max[1],"min_2": daily_min[1],"moring_2": daily_morn[1],"eve_2": daily_eve[1],"night_2": daily_night[1],"humidity_2": daily_humidity[1],"deg_2": daily_deg[1],"speed_2": daily_speed[1],"rain_2": daily_rain[1],"snow_2": daily_snow[1],
                                                                            "day_3": daily_day[2],"text_3": daily_text[2],"max_3": daily_max[2],"min_3": daily_min[2],"moring_3": daily_morn[2],"eve_3": daily_eve[2],"night_3": daily_night[2],"humidity_3": daily_humidity[2],"deg_3": daily_deg[2],"speed_3": daily_speed[2],"rain_3": daily_rain[2],"snow_3": daily_snow[2],
                                                                                    "day_4": daily_day[3],"text_4": daily_text[3],"max_4": daily_max[3],"min_4": daily_min[3],"moring_4": daily_morn[3],"eve_4": daily_eve[3],"night_4": daily_night[3],"humidity_4": daily_humidity[3],"deg_4": daily_deg[3],"speed_4": daily_speed[3],"rain_4": daily_rain[3],"snow_4": daily_snow[3],
                                                                                            "day_5": daily_day[4],"text_5": daily_text[4],"max_5": daily_max[4],"min_5": daily_min[4],"moring_5": daily_morn[4],"eve_5": daily_eve[4],"night_5": daily_night[4],"humidity_5": daily_humidity[4],"deg_5": daily_deg[4],"speed_5": daily_speed[4],"rain_5": daily_rain[4],"snow_5": daily_snow[4],
                                                                                                    "day_6": daily_day[5],"text_6": daily_text[5],"max_6": daily_max[5],"min_6": daily_min[5],"moring_6": daily_morn[5],"eve_6": daily_eve[5],"night_6": daily_night[5],"humidity_6": daily_humidity[5],"deg_6": daily_deg[5],"speed_6": daily_speed[5],"rain_6": daily_rain[5],"snow_6": daily_snow[5],
                                                                                                            "day_7": daily_day[6],"text_7": daily_text[6],"max_7": daily_max[6],"min_7": daily_min[6],"moring_7": daily_morn[6],"eve_7": daily_eve[6],"night_7": daily_night[6],"humidity_7": daily_humidity[6],"deg_7": daily_deg[6],"speed_7": daily_speed[6],"rain_7": daily_rain[6],"snow_7": daily_snow[6],})
        line_bot_api.push_message(event.source.user_id, FlexSendMessage(alt_text="hourly", contents=json.loads(weekly)))



def result(event):
    match_pattern = r'(.+)の天気$'
    return re.search(match_pattern,event.message.text)

def degree(weather_wind_deg):
    wind_deg = ("北","北北東","北東", "東北東", "東", "東南東", "南東", "南南東", "南", "南南西", "南西", "西南西", "西", "西北西", "北西", "北北西",)
    each_deg = 360.0 / len(wind_deg)
    degree = round(weather_wind_deg / each_deg) % len(wind_deg)
    return wind_deg[degree]

def geometry_data(city_name):
    url_geometry = "https://msearch.gsi.go.jp/address-search/AddressSearch?q={city}"
    format = url_geometry.format(city = city_name,)
    response = requests.get(format)
    data = response.json()
    return data

def city_lat_lon(geo_data, city_name):
    for i in range(len(geo_data)) :
        if re.search(city_name ,geo_data[i]["properties"]["title"]):
            city_geometry = geo_data[i]["geometry"]["coordinates"]
            city_title = geo_data[i]["properties"]["title"]
            city_lon = city_geometry[0]
            city_lat = city_geometry[1]
            break
    return city_title, city_lon, city_lat

def amount(type,data):
    weather_amount = 0
    for i in range(24):
        try:
            weather_amount += data["hourly"][i][type]["1h"]
        except KeyError:
                continue
    return weather_amount

def data(lat,lon):
    api_key = keys()[2]
    url_weather = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=alerts&appid={key}&units=metric&lang=ja"
    format = url_weather.format(lat = lat, lon = lon, key = api_key,)
    response = requests.get(format)
    data = response.json()
    return data

def extract_data(data):
    current = data["current"]
    daily = data["daily"]
    hourly = data["hourly"]

    temp = current["temp"]
    feels_like = current["feels_like"]
    humidity = current["humidity"]
    wind_speed = current["wind_speed"]
    wind_deg = current["wind_deg"]
    sunrise = current["sunrise"]
    sunset = current["sunset"]
    text = current["weather"][0]["description"]

    temp_min = daily[0]["temp"]["min"]
    temp_max = daily[0]["temp"]["max"]

    rain = amount("rain", data)
    snow = amount("snow", data)

    hourly_time = tuple([utc_to_jp_hourly(hourly[i]["dt"]) for i in range(1,25,2)])
    hourly_text = tuple([hourly[i]["weather"][0]["description"] for i in range(1,25,2)])
    hourly_temp = tuple([hourly[i]["temp"] for i in range(1,25,2)])

    daily_day = tuple([utc_to_jp_weekly(daily[i]["dt"]) for i in range(7)])
    daily_text = tuple([daily[i]["weather"][0]["description"] for i in range(7)])
    daily_max = tuple([daily[i]["temp"]["max"] for i in range(7)])
    daily_min = tuple([daily[i]["temp"]["min"] for i in range(7)])
    daily_morn = tuple([daily[i]["temp"]["morn"] for i in range(7)])
    daily_eve =  tuple([daily[i]["temp"]["eve"] for i in range(7)])
    daily_night = tuple([daily[i]["temp"]["night"] for i in range(7)])
    daily_humidity = tuple([daily[i]["humidity"] for i in range(7)])
    daily_deg = tuple([degree(daily[i]["wind_deg"]) for i in range(7)])
    daily_speed = tuple([daily[i]["wind_speed"] for i in range(7)])
    daily_rain = amount_daily(daily,"rain")
    daily_snow = amount_daily(daily,"snow")
 
    return temp, feels_like, temp_min, temp_max, humidity, wind_speed, wind_deg, sunrise, sunset, text, rain, snow, hourly_time, hourly_text, hourly_temp, daily_day, daily_text, daily_max, daily_min, daily_morn, daily_eve, daily_night, daily_humidity, daily_deg, daily_speed, daily_rain, daily_snow

def utc_to_jp(time):
    return datetime.fromtimestamp(time).strftime('%H:%M:%S')

def utc_to_jp_hourly(time):
    return datetime.fromtimestamp(time).strftime('%H:%M')

def utc_to_jp_weekly(time):
    result = datetime.fromtimestamp(time).strftime('%w,%m月%d日')
    week = ("月曜日","火曜日","水曜日","木曜日","金曜日","土曜日","日曜日")
    w = result[0]
    return result.replace(w,week[int(w)],1)

def amount_daily(daily,type):
    weather_amount = []
    for i in range(7):
        try:
            weather_amount.append(daily[i][type])
        except KeyError:
            weather_amount.append(0)
    return tuple(weather_amount)