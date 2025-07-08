import requests
import datetime
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Get API key from environment variables or use a placeholder for demo
API_KEY = os.getenv("OPENWEATHER_API_KEY", "demo_key")

@st.cache_data(ttl=1800)  # Cache data for 30 minutes
def get_weather_data(location):
    """
    Get current weather data for a location using OpenWeatherMap API
    """
    # For demo purposes, if API key is not available, return mock data
    if API_KEY == "demo_key":
        return get_mock_weather_data(location)
        
    try:
        # Make API call to OpenWeatherMap
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=imperial"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}")
            
        data = response.json()
        
        # Extract relevant weather information
        weather_data = {
            'temp': round(data['main']['temp']),
            'humidity': data['main']['humidity'],
            'conditions': data['weather'][0]['main'],
            'wind_speed': data['wind']['speed'],
            'location': f"{data['name']}, {data.get('sys', {}).get('country', '')}",
            'timestamp': datetime.datetime.now()
        }
        
        # Try to get rainfall data if available
        if 'rain' in data:
            weather_data['rainfall_24h'] = data['rain'].get('1h', 0) * 24  # Estimate based on current rainfall
        else:
            weather_data['rainfall_24h'] = 0
            
        return weather_data
        
    except Exception as e:
        st.error(f"Error getting weather data: {str(e)}")
        return get_mock_weather_data(location)

@st.cache_data(ttl=3600)  # Cache data for 60 minutes
def get_forecast(location, days=5):
    """
    Get 5-day forecast for a location using OpenWeatherMap API
    """
    # For demo purposes, if API key is not available, return mock data
    if API_KEY == "demo_key":
        return get_mock_forecast(location, days)
        
    try:
        # Make API call to OpenWeatherMap forecast endpoint
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=imperial"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}")
            
        data = response.json()
        
        # Process and organize forecast data by day
        forecast_data = []
        today = datetime.datetime.now().date()
        
        # Group by date
        forecasts_by_date = {}
        
        for item in data['list']:
            dt = datetime.datetime.fromtimestamp(item['dt'])
            date_str = dt.date()
            
            if date_str not in forecasts_by_date:
                forecasts_by_date[date_str] = []
                
            forecasts_by_date[date_str].append({
                'temp': item['main']['temp'],
                'conditions': item['weather'][0]['main'],
                'humidity': item['main']['humidity'],
                'rainfall': item.get('rain', {}).get('3h', 0),
                'time': dt.time()
            })
        
        # Create daily summaries for the next 'days' days
        for i in range(1, days + 1):
            forecast_date = today + datetime.timedelta(days=i)
            
            if forecast_date in forecasts_by_date:
                day_forecasts = forecasts_by_date[forecast_date]
                
                # Calculate daily stats
                temps = [f['temp'] for f in day_forecasts]
                rainfall = sum(f.get('rainfall', 0) for f in day_forecasts)
                conditions = max(set(f['conditions'] for f in day_forecasts), 
                                key=[f['conditions'] for f in day_forecasts].count)
                
                forecast_data.append({
                    'date': forecast_date,
                    'temp_high': round(max(temps)),
                    'temp_low': round(min(temps)),
                    'temp_avg': round(sum(temps) / len(temps)),
                    'conditions': conditions,
                    'rainfall': round(rainfall, 2),
                    'humidity': round(sum(f['humidity'] for f in day_forecasts) / len(day_forecasts))
                })
        
        return forecast_data
        
    except Exception as e:
        st.error(f"Error getting forecast data: {str(e)}")
        return get_mock_forecast(location, days)

def get_mock_weather_data(location):
    """
    Generate mock weather data for demo purposes
    """
    return {
        'temp': 72,
        'humidity': 65,
        'conditions': 'Partly Cloudy',
        'wind_speed': 5.2,
        'location': location,
        'timestamp': datetime.datetime.now(),
        'rainfall_24h': 0.1
    }

def get_mock_forecast(location, days=5):
    """
    Generate mock forecast data for demo purposes
    """
    forecast_data = []
    today = datetime.datetime.now().date()
    
    conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Sunny']
    temps_high = [75, 78, 72, 68, 76]
    temps_low = [60, 62, 58, 55, 59]
    rainfall = [0, 0, 0, 0.35, 0]
    
    for i in range(1, days + 1):
        forecast_date = today + datetime.timedelta(days=i)
        forecast_data.append({
            'date': forecast_date,
            'temp_high': temps_high[i-1] if i <= len(temps_high) else 75,
            'temp_low': temps_low[i-1] if i <= len(temps_low) else 60,
            'temp_avg': (temps_high[i-1] + temps_low[i-1]) / 2 if i <= len(temps_high) else 68,
            'conditions': conditions[i-1] if i <= len(conditions) else 'Sunny',
            'rainfall': rainfall[i-1] if i <= len(rainfall) else 0,
            'humidity': 65
        })
    
    return forecast_data
