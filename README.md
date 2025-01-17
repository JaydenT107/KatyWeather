# KatyWeather

This Python script predicts weather conditions for the next 5 days and provides a historical view of the past 12 hours. It leverages WeatherAPI for real-time weather data, AWS Lambda for serverless execution, and Make.com for automating workflows. The script pulls data from WeatherAPI, stores it in an S3 bucket, and imported it into a Google Sheet, which is used for visualization on a Google Site: https://sites.google.com/view/katyweather/home.

Additionally, AI is incorporated to provide descriptive insights into the forecast for the next 5 days, helping users understand weather patterns beyond raw data.

---

# Weather Prediction and History Tracker

This is my first-ever project! It uses AWS Lambda to automate the process of fetching weather data from [WeatherAPI](https://weatherapi.com), forecasting the next 5 days, and tracking weather conditions for the past 12 hours. The weather data is stored in an S3 bucket, and the S3 URL is used to import the data into a Google Sheet. Make.com is used to automatically update the data every 12 hours, ensuring that the visualized data on a Google Site stays up to date. Additionally, an AI API is used to generate descriptions of the forecasted weather for the next 5 days, which automatically updates based on the provided data.

## Overview

This project includes the following features:
1. **Fetch Weather Data**: The script fetches weather data for the past 12 hours and the 5-day forecast using the WeatherAPI.
2. **Store Data in S3**: The pulled data is stored in an S3 bucket, and the URL to the stored data is used for further processing.
3. **AI-Generated Descriptions**: An AI API is used to automatically generate natural language descriptions for the forecasted weather for the next 5 days based on the provided data.
4. **Automated Data Collection with AWS Lambda**: The Lambda function is triggered every hour to update weather data and every 12 hours to update the forecast, all scheduled via AWS EventBridge.
5. **Import Data into Google Sheets**: The weather data is imported into a Google Sheet, which is used for visualization on a Google Site.
6. **Automatic Data Updates**: Make.com ensures the Google Sheet is updated every 12 hours, ensuring the visualized data is current.

## Architecture

- **AWS Lambda**: Executes the script to fetch, process, and store weather data in S3.
- **AWS EventBridge**: Triggers the Lambda function on an hourly schedule for weather data updates and every 12 hours for forecast updates.
- **WeatherAPI**: Provides real-time weather data for the last 12 hours and forecasts for the next 5 days.
- **Amazon S3**: Stores the weather data pulled from WeatherAPI.
- **Make.com**: Fetches the S3 URL and imports the data into a Google Sheet, ensuring the sheet is updated every 12 hours.
- **AI API**: Generates natural language descriptions of the forecasted weather for the next 5 days.

## Skills Used

This project utilizes the following skills:
- **AWS Lambda**: For automating the execution of the script to fetch and store weather data.
- **Amazon S3**: To store the weather data fetched from WeatherAPI.
- **Python**: The programming language used to write the Lambda function and process the weather data.
- **Make.com**: For automating the import of data into a Google Sheet and ensuring the sheet is updated every 12 hours.
- **WeatherAPI**: Provides the weather data used in this project.
- **AI API**: Generates descriptions of the forecasted weather data.

## Setup

### 1. **AWS Lambda & EventBridge**
- Create an AWS Lambda function with permissions to fetch weather data from WeatherAPI and store it in an S3 bucket.
- Set up an EventBridge rule to trigger the Lambda function every hour for weather updates and every 12 hours for forecast data.

### 2. **WeatherAPI Integration**
- Sign up at https://openweathermap.org/ and obtain an API key.
- In your Lambda function, fetch the weather data for the last 12 hours and the 5-day forecast, then store it in an S3 bucket.

### 3. **Amazon S3**
- Set up an S3 bucket to store the weather data fetched from Openweathermap.
- Configure the Lambda function to store the weather data in the S3 bucket.

### 4. **Make.com Integration**
- Set up a Make.com scenario to fetch the weather data from the S3 URL and import it into a Google Sheet.
- Configure the Make.com scenario to run every 12 hours to update the visualized data in the Google Sheet.

### 5. **AI API Integration**
- Integrate an AI API that can process the weather forecast data and generate natural language descriptions for the next 5 days.
- Ensure the AI API automatically updates the descriptions based on the forecast data provided.

## Usage

Once set up, the Lambda function will run on an hourly schedule to update weather data and every 12 hours to fetch forecast data. The weather data is stored in S3, and Make.com will automatically insert this data into the Google Sheet, which is used for visualization on a Google Site. The AI API will update the weather descriptions for the 5-day forecast automatically.

## Google Site Link

https://sites.google.com/view/katyweather/home

## Contributions

Since this is my first project, feel free to submit any issues, suggestions, or improvements.
