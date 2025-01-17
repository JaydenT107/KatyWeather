import json
import boto3
import csv
import io
import os
def upload_csv_s3():
    my_bucket1 = os.getenv('WK_bucket')
    my_bucket2 = os.getenv('KWCSV_bucket')
    s3 = boto3.client('s3')
    try:
        csv_content = io.StringIO()
        response = s3.get_object(Bucket= my_bucket1 , Key='Weather/weatherkaty.json')
        json_data = json.loads(response['Body'].read().decode('utf-8'))
        writer = csv.DictWriter(csv_content, fieldnames = json_data[0].keys())
        writer.writeheader()
        writer.writerows(json_data[len(json_data)-12::])
        s3.put_object(Bucket = my_bucket2 , Key = 'Weather/weatherkatycsv.csv', Body = csv_content.getvalue())

    except s3.exceptions.NoSuchKey:
        print('Error! File is not exist')



import requests

def get_data_forecast():
    api_key = os.getenv('weather_api_key')
    base_url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = { 'q' : 'katy,tx,us', 'appid' : api_key}
    
    try:
        response = requests.get(base_url,params)
        if response.status_code == 200:
            data = response.json()
            return data
    except requests.RequestException as r:
        print('Error: ' , r)
        return None


import datetime
def data_forecast():
    data = get_data_forecast()
    datacity = data['city']
    dataweather = data['list']
    elist = []   
    for i in dataweather:
        data3 = {}
        data3['Date'] = datetime.datetime.fromtimestamp(i['dt']).strftime('%D')
        data3['Time'] = datetime.datetime.fromtimestamp(i['dt']).strftime('%H:%M')
        data3['Location'] = [datacity['name'],datacity['country']]
        weather_list = [i['weather'][0]['main'],i['weather'][0]['description']]
        data3['Weather'] = weather_list
        data3['Temperature (°C)'] = i['main']['temp']
        data3['Wind (m/s)'] = i['wind']['speed']
        data3['Humidity (%)'] = i['main']['humidity']
        data3['Cloudiness (%)'] = list(i['clouds'].values())[0]                     
        elist.append(data3)
    return elist
    

def clean_data(data): 
    elist = []
    
    for i in data:
        edict = i
        if edict['Temperature (°C)'] > 100:
            edict['Temperature (°C)'] = round(edict['Temperature (°C)']-273.15,2)

        if type(edict['Location']) == list :
            edict['Location'] = ", ".join(edict['Location'])    

        if type(edict['Weather']) == list :
            edict['Weather'] = ": ".join(edict['Weather'])
        
        elist.append(edict)
            
    return elist
    
def description_forecast(data_forecast = data_forecast()):
    data2 = clean_data(data_forecast)
    
    wlist = [i['Weather'] for i in data2]
    
    dlist = sorted(set([i['Date'] for i in data2]))
    todaylist = [i for i in data2 if i['Date'] == dlist[0]]
    tmrlist = [i for i in data2 if i['Date'] == dlist[1]]
    n4list = [i for i in data2 if i['Date'] == dlist[4]]
    
    general_count = sorted(list({i : wlist.count(i) for i in set(wlist)}.items()),key = lambda x: x[1], reverse=True)
    
    
    
    weather_conditions = [i.split(':')[0] if 'Clear' not in i else 'clear sky' for i in set(wlist)]
    
    #general_description

    general_string = ", ".join(list(set(weather_conditions))[-1::-1]).lower()
    general_weather = (f'The upcoming five days are expected to generally feature: {general_string}, with varying conditions throughout the week, mostly {general_count[0][0].lower()}')
    
    #day_by_day
    #today
    tlisttoday = [i['Temperature (°C)'] for i in todaylist]
    hlisttoday = [i['Humidity (%)'] for i in todaylist]
    cloudlisttoday = [i['Cloudiness (%)'] for i in todaylist]
    windspeedtoday = [i['Wind (m/s)'] for i in todaylist]
    avg_temp_today = round(sum(tlisttoday)/len(tlisttoday),2)
    avg_humi_today = round(sum(hlisttoday)/len(hlisttoday),2)
    avg_sp_today = round(sum(windspeedtoday)/len(windspeedtoday),2)
    avg_cloud_today = round(sum(cloudlisttoday)/len(cloudlisttoday),2)
    #tomorrow

    clist = [i['Weather'].split(":")[1] for i in tmrlist]
    cdict = sorted(list({i : clist.count(i) for i in set(clist)}.items()),key= lambda x: x[1], reverse=True)
    tlist = [i['Temperature (°C)'] for i in tmrlist]
    hlist = [i['Humidity (%)'] for i in tmrlist]
    cloudlist = [i['Cloudiness (%)'] for i in tmrlist]
    windspeed = [i['Wind (m/s)'] for i in tmrlist]
    avg_temp = round(sum(tlist)/len(tlist),2)
    avg_humi = round(sum(hlist)/len(hlist),2)
    avg_cloud = round(sum(cloudlist)/len(cloudlist),2)
    avg_sp = round(sum(windspeed)/len(windspeed),2)
    
    next_day_weather = (f'On {dlist[1]}, expect{cdict[0][0].lower()} with temperatures between {tlist[0]}°C and {tlist[-1]}°C')
    if len(cdict) > 1:
        next_day_weather+= f', {cdict[1][0].lower()} is expected'

    def check_status(percentage):
        if percentage <= 33:
            return 'lightly'
        elif 33 < percentage <= 66:
            return 'moderately'
        elif percentage > 66:
            return 'highly'

    #next_4_days
    tlist4 = [i['Temperature (°C)'] for i in n4list]
    hlist4 = [i['Humidity (%)'] for i in n4list]
    cloudlist4 = [i['Cloudiness (%)'] for i in n4list]
    windspeed4 = [i['Wind (m/s)'] for i in n4list]
    avg_humi4 = round(sum(hlist4)/len(hlist4),2)
    avg_cloud4 = round(sum(cloudlist4)/len(cloudlist4),2)
    avg_sp4 = round(sum(windspeed4)/len(windspeed4),2)
    avg_temp4 = round(sum(tlist4)/len(tlist4),2)


    def percentage(data1,data4):
       return round(abs(data1-data4)/data1*100,2)  

    humi4 = f"Average Humidity Over Five Days: from {avg_humi_today} to {avg_humi4} ({round(abs(avg_humi_today - avg_humi4),2)}% change)"
    wind4 = f"Average Wind Speed Over Five Days: from {avg_sp_today} to {avg_sp4} ({percentage(avg_sp_today, avg_sp4)}% change)"
    cloud4 = f"Average Cloudiness Over Five Days: from {avg_cloud_today} to {avg_cloud4} ({round(abs(avg_cloud4 - avg_cloud_today),2)}% change)"  
    temp4 = f"Average Temperature Over Five Days: from {avg_temp_today} to {avg_temp4} ({percentage(avg_temp_today, avg_temp4)}% change)"

    WandH = f'Average wind speed is {avg_sp} m/s, with humidity levels hovering around {avg_humi}%, creating a {check_status(avg_humi)} humid feel.'

    result = [general_weather,humi4,wind4,cloud4,temp4,next_day_weather,WandH]

    return result
    
        


def export_to_forecast_csv():
    import json
    import csv
    import boto3
    import io

    s3 = boto3.client('s3')
    csv_content = io.StringIO()

    data = clean_data(data_forecast())
    
    writer = csv.DictWriter(csv_content, fieldnames=list(data[0].keys()))
    writer.writeheader()
    writer.writerows(data)
    
    s3.put_object(Bucket = 'katyweathercsv', Key = 'Weather/forecastweatherkatycsv.csv', Body = csv_content.getvalue())

from openai import OpenAI
def AI_commentary(data=description_forecast()):
    AI_apikey = os.getenv('AI_api_key')
    AI_base_url = "https://api.deepseek.com"
    client = OpenAI(api_key = AI_apikey, base_url = AI_base_url)
    
    response = client.chat.completions.create(
        model = "deepseek-chat",
        messages = [
            { "role" : "system" , "content" : "You are a witty weather forecaster. Your job is to provide a short, natural comment (1-2 sentences) based on the provided weather data. Keep your response professional, accurate. Do not provide a full weather report—just a clever remark."},
            { "role" : "user" , "content" : ", ".join(data[5::])},    
        ],
         stream = False,
         max_tokens = 50)

    response2 = client.chat.completions.create(
        model = "deepseek-chat",
        messages = [
            { "role" : "system" , "content" : "You are a professional weather forecaster. Your job is to provide a short, natural comment (3-4 sentences) based on the provided weather data for the next 5 days. Keep your response professional, accurate, and analytical."},
            { "role" : "user" , "content" : ", ".join(data[1:5:])},    
        ],
         stream = False,
         max_tokens = 150)
    output = [response.choices[0].message.content, response2.choices[0].message.content]
    return(output)

def export_to_forecast_txt():
    import boto3
    my_bucket = os.getenv('KWCSV_bucket')
    s3 = boto3.client('s3')
    data = description_forecast()
    AI_desc = AI_commentary()
    general_content = data[0]
    tomorrow_content = ", ".join(data[5::])
    humid_content = data[1]
    wind_content = data[2]
    cloud_content = data[3]
    temp_content = data[4]

    s3.put_object(Bucket = my_bucket, Key = 'Weather/forecastweatherkatygeneral.txt', Body = general_content)
    s3.put_object(Bucket = my_bucket, Key = 'Weather/forecastweatherkatytmr.txt', Body = tomorrow_content)
    s3.put_object(Bucket = my_bucket, Key = 'Weather/forecastweatherkatyhumid.txt', Body = humid_content)
    s3.put_object(Bucket = my_bucket, Key = 'Weather/forecastweatherkatywind.txt', Body = wind_content)
    s3.put_object(Bucket = my_bucket, Key = 'Weather/forecastweatherkatycloud.txt', Body = cloud_content)
    s3.put_object(Bucket = my_bucket, Key = 'Weather/forecastweatherkatytemp.txt', Body = temp_content)
    s3.put_object(Bucket = my_bucket, Key = 'Weather/forecastweatherkatyAItmr.txt', Body = AI_desc[0])
    s3.put_object(Bucket = my_bucket, Key = 'Weather/forecastweatherkatyAInum.txt', Body = AI_desc[1])

def lambda_handler(event, context):
    upload_csv_s3()
    export_to_forecast_csv()
    export_to_forecast_txt()
