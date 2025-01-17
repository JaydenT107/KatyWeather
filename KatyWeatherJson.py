
import requests
import boto3
import json
import csv
import io
import os

def get_data():
    api_key = os.getenv('weather_api_key')
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = { 'q' : 'katy,tx,us', 'appid' : api_key}
    
    try:
        response = requests.get(base_url,params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('Error: ', response.status_code)
            return None
    except requests.RequestException as r:
        print('Error: ', r)
        return None


import datetime
from datetime import timedelta
def data():
    data = get_data()
    data2 = {}
    data2['Date'] = (datetime.datetime.today() - timedelta(hours=6)).strftime("%D")
    data2['Time'] = (datetime.datetime.now() - timedelta(hours=6)).strftime("%H:%M")
    data2['Coordinate'] = f"{list(data['coord'].values())[1]} - {list(data['coord'].values())[0]}"
    data2['Location'] = [data['name'],data['sys']['country']]
    weather_list = [data['weather'][0]['main'],data['weather'][0]['description']]
    data2['Weather'] = weather_list
    data2['Temperature (°C)'] = data['main']['temp']
    data2['Wind (m/s)'] = data['wind']['speed']
    
    return data2


def clean_data(data):   
    
    edict = data
    if edict['Temperature (°C)'] > 100:
        edict['Temperature (°C)'] = round(edict['Temperature (°C)']-273.15,2)
        
    if type(edict['Location']) == list :
        edict['Location'] = ", ".join(edict['Location'])    
    
    if type(edict['Weather']) == list :
        edict['Weather'] = ": ".join(edict['Weather'])
    return edict
    
def upload_json_s3():
    s3 = boto3.client('s3')
    my_bucket = os.getenv('Json_bucket')
    try: 
        response = s3.get_object(Bucket=my_bucket, Key='Weather/weatherkaty.json')
        elist = list(json.loads(response['Body'].read().decode('utf-8')))
        elist.append(clean_data(data()))
        s3.put_object(Bucket=my_bucket, Key='Weather/weatherkaty.json', Body=json.dumps(elist, indent = 4))
    except s3.exceptions.NoSuchKey:
        elist = []
        elist.append(clean_data(data()))
        s3.put_object(Bucket=my_bucket, Key='Weather/weatherkaty.json', Body=json.dumps(elist, indent = 4))



def lambda_handler(event, context):
    upload_json_s3()
