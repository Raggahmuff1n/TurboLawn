import datetime
from datetime import timedelta

def get_watering_recommendation(weather_data, forecast_data, lawn_type):
    """
    Generate watering recommendations based on weather data and forecast
    
    Args:
        weather_data: Current weather conditions
        forecast_data: 5-day forecast
        lawn_type: Type of grass (Cool Season, Warm Season, Mixed)
        
    Returns:
        Dictionary with watering recommendation details
    """
    today = datetime.datetime.now().date()
    current_temp = weather_data['temp']
    current_humidity = weather_data['humidity']
    recent_rainfall = weather_data.get('rainfall_24h', 0)
    
    # Check if it rained recently or will rain soon
    rain_coming = any(day['rainfall'] > 0.25 for day in forecast_data[:2])
    
    # Base water needs on grass type (inches per week)
    if lawn_type == "Cool Season Grass":
        weekly_water_need = 1.0  # 1 inch per week
        ideal_temp_range = (60, 75)
    elif lawn_type == "Warm Season Grass":
        weekly_water_need = 0.75  # 0.75 inches per week
        ideal_temp_range = (80, 95)
    else:  # Mixed
        weekly_water_need = 0.85  # 0.85 inches per week
        ideal_temp_range = (65, 85)
    
    # Adjust for temperature and humidity
    if current_temp > ideal_temp_range[1] + 10:
        weekly_water_need *= 1.3  # Increase water needs in very hot weather
    elif current_temp < ideal_temp_range[0] - 10:
        weekly_water_need *= 0.7  # Decrease water needs in cool weather
        
    if current_humidity < 40:
        weekly_water_need *= 1.2  # More water needed in dry conditions
    elif current_humidity > 80:
        weekly_water_need *= 0.8  # Less water needed in humid conditions
    
    # Calculate daily water need
    daily_water_need = weekly_water_need / 3  # Typically water 3 times per week
    
    # Determine recommendation
    recommendation = {}
    
    if recent_rainfall > daily_water_need:
        recommendation['message'] = f"Skip watering today. Recent rainfall of {recent_rainfall} inches is sufficient."
        recommendation['should_water'] = False
        recommendation['next_water_date'] = today + timedelta(days=2)  # Check again in 2 days
        
    elif rain_coming:
        recommendation['message'] = "Hold off on watering as rain is forecasted within the next 48 hours."
        recommendation['should_water'] = False
        
        # Find the day after rain
        for i, day in enumerate(forecast_data):
            if day['rainfall'] > 0:
                recommendation['next_water_date'] = day['date'] + timedelta(days=1)
                break
        else:
            recommendation['next_water_date'] = today + timedelta(days=1)
            
    else:
        # Determine if watering is needed based on temperature and time of day
        current_hour = datetime.datetime.now().hour
        
        if current_hour < 10 or current_hour > 16:  # Early morning or evening is ideal
            recommendation['message'] = f"Water your lawn today with {daily_water_need:.2f} inches of water (about {int(daily_water_need * 60)} minutes with sprinkler)."
            recommendation['should_water'] = True
            recommendation['water_amount'] = daily_water_need
            recommendation['next_water_date'] = today + timedelta(days=2)  # Water again in 2 days
        else:
            recommendation['message'] = f"Water your lawn this evening or early tomorrow morning with {daily_water_need:.2f} inches of water."
            recommendation['should_water'] = True
            recommendation['water_amount'] = daily_water_need
            recommendation['next_water_date'] = today
            
    return recommendation

def get_mowing_recommendation(weather_data, forecast_data, lawn_type):
    """
    Generate mowing recommendations based on weather data and forecast
    
    Args:
        weather_data: Current weather conditions
        forecast_data: 5-day forecast
        lawn_type: Type of grass (Cool Season, Warm Season, Mixed)
        
    Returns:
        Dictionary with mowing recommendation details
    """
    today = datetime.datetime.now().date()
    current_temp = weather_data['temp']
    conditions = weather_data['conditions']
    
    # Check upcoming weather
    rain_today = "rain" in conditions.lower()
    rain_tomorrow = any("rain" in day['conditions'].lower() for day in forecast_data[:1])
    
    # Determine ideal mowing day based on forecast
    ideal_mowing_days = []
    
    for i, day in enumerate(forecast_data):
        day_quality = 100  # Start with perfect score
        
        # Penalize for rain
        if "rain" in day['conditions'].lower():
            day_quality -= 80
            
        # Penalize for extreme temperatures
        if day['temp_high'] > 95:
            day_quality -= 40
        elif day['temp_high'] > 90:
            day_quality -= 20
            
        if day['temp_high'] < 50:
            day_quality -= 30
            
        # Add day and quality score
        ideal_mowing_days.append((day['date'], day_quality))
    
    # Sort by quality
    ideal_mowing_days.sort(key=lambda x: x[1], reverse=True)
    
    # Generate recommendation
    recommendation = {}
    
    if rain_today:
        recommendation['message'] = "Avoid mowing today as the lawn is wet. Wait for it to dry completely."
        recommendation['should_mow'] = False
        recommendation['next_mow_date'] = today + timedelta(days=1)
    elif rain_tomorrow:
        recommendation['message'] = "Consider mowing today as rain is expected tomorrow."
        recommendation['should_mow'] = True
        recommendation['next_mow_date'] = today
    else:
        # Recommend the best day in the next 5 days
        best_day, best_score = ideal_mowing_days[0]
        
        if best_day == today + timedelta(days=1):
            recommendation['message'] = f"Tomorrow will be an ideal day for mowing your lawn."
            recommendation['should_mow'] = False
            recommendation['next_mow_date'] = best_day
        elif best_day == today:
            recommendation['message'] = "Today is an ideal day for mowing your lawn."
            recommendation['should_mow'] = True
            recommendation['next_mow_date'] = today
        else:
            days_away = (best_day - today).days
            recommendation['message'] = f"Plan to mow your lawn on {best_day.strftime('%A')}, which will be the best day in the coming {days_away} days."
            recommendation['should_mow'] = False
            recommendation['next_mow_date'] = best_day
            
    # Add lawn-type specific advice
    if lawn_type == "Cool Season Grass":
        recommendation['message'] += " For cool season grass, maintain a height of 2.5-3.5 inches."
    elif lawn_type == "Warm Season Grass":
        recommendation['message'] += " For warm season grass, maintain a height of 1.5-2.5 inches."
    else:
        recommendation['message'] += " For mixed grass, maintain a height of 2-3 inches."
        
    return recommendation
