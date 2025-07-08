import streamlit as st
import requests
import datetime
import pandas as pd
from datetime import timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import utility modules
from utils.weather import get_weather_data, get_forecast
from utils.recommendations import get_watering_recommendation, get_mowing_recommendation

# Page configuration
st.set_page_config(
    page_title="TurboLawn - Lawn Care Assistant",
    page_icon="🌱",
    layout="wide"
)

# Initialize session state for saved locations
if 'saved_locations' not in st.session_state:
    st.session_state.saved_locations = []

if 'selected_location' not in st.session_state:
    st.session_state.selected_location = ""

if 'lawn_type' not in st.session_state:
    st.session_state.lawn_type = "Cool Season Grass"  # Default

# Function to add location to saved locations
def add_location(location):
    if location and location not in st.session_state.saved_locations:
        st.session_state.saved_locations.append(location)
        st.session_state.selected_location = location
        return True
    return False

# Header and description
st.title("🌱 TurboLawn")
st.subheader("Smart Lawn Care Assistant")

# Sidebar for navigation and settings
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Select Page", ["Dashboard", "Settings", "About"])
    
    st.header("Location")
    # Location input
    location_input = st.text_input("Enter your location (city, state)", 
                                  value=st.session_state.selected_location)
    
    if st.button("Add Location"):
        if add_location(location_input):
            st.success(f"Added {location_input} to saved locations!")
    
    # Saved locations
    if st.session_state.saved_locations:
        st.subheader("Saved Locations")
        selected_loc = st.selectbox(
            "Select a saved location",
            options=st.session_state.saved_locations,
            index=st.session_state.saved_locations.index(st.session_state.selected_location) 
                  if st.session_state.selected_location in st.session_state.saved_locations else 0
        )
        
        if selected_loc != st.session_state.selected_location:
            st.session_state.selected_location = selected_loc
            st.experimental_rerun()

# Main content based on selected page
if page == "Dashboard":
    if st.session_state.selected_location:
        try:
            # Get weather data
            weather_data = get_weather_data(st.session_state.selected_location)
            forecast_data = get_forecast(st.session_state.selected_location)
            
            # Dashboard layout with columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Current Conditions")
                st.metric("Temperature", f"{weather_data['temp']}°F")
                st.metric("Humidity", f"{weather_data['humidity']}%")
                st.metric("Conditions", weather_data['conditions'])
                
                if 'rainfall_24h' in weather_data:
                    st.metric("Rainfall (Last 24h)", f"{weather_data['rainfall_24h']} in")
            
            with col2:
                st.subheader("Lawn Care Recommendations")
                
                # Get recommendations based on weather data
                watering_rec = get_watering_recommendation(
                    weather_data, 
                    forecast_data, 
                    st.session_state.lawn_type
                )
                
                mowing_rec = get_mowing_recommendation(
                    weather_data, 
                    forecast_data, 
                    st.session_state.lawn_type
                )
                
                st.info(f"💧 **Watering Advice**: {watering_rec['message']}")
                st.info(f"🌿 **Mowing Advice**: {mowing_rec['message']}")
                
                if 'next_water_date' in watering_rec:
                    st.write(f"Next recommended watering: **{watering_rec['next_water_date'].strftime('%A, %b %d')}**")
                
                if 'next_mow_date' in mowing_rec:
                    st.write(f"Next recommended mowing: **{mowing_rec['next_mow_date'].strftime('%A, %b %d')}**")
            
            # 5-Day Forecast
            st.subheader("5-Day Forecast")
            
            forecast_df = pd.DataFrame(forecast_data)
            st.line_chart(forecast_df[['date', 'temp_high', 'temp_low']].set_index('date'))
            
            # Create columns for each forecast day
            forecast_cols = st.columns(min(5, len(forecast_data)))
            
            for i, (day, col) in enumerate(zip(forecast_data, forecast_cols)):
                with col:
                    st.write(f"**{day['date'].strftime('%a')}**")
                    st.write(f"{day['temp_high']}°F / {day['temp_low']}°F")
                    st.write(f"{day['conditions']}")
                    if 'rainfall' in day:
                        st.write(f"Rain: {day['rainfall']} in")
            
        except Exception as e:
            st.error(f"Error retrieving data: {str(e)}")
    else:
        st.info("Please enter a location in the sidebar to get started.")
        
        # Display sample dashboard when no location is selected
        st.subheader("Sample Dashboard Preview")
        st.image("https://via.placeholder.com/800x400.png?text=TurboLawn+Dashboard+Preview")
        
elif page == "Settings":
    st.header("Settings")
    
    st.subheader("Lawn Information")
    lawn_type = st.selectbox(
        "Lawn Type",
        options=["Cool Season Grass", "Warm Season Grass", "Mixed Grass"],
        index=["Cool Season Grass", "Warm Season Grass", "Mixed Grass"].index(st.session_state.lawn_type)
    )
    
    if lawn_type != st.session_state.lawn_type:
        st.session_state.lawn_type = lawn_type
    
    st.subheader("Notification Preferences")
    notify_watering = st.checkbox("Watering Reminders", value=True)
    notify_mowing = st.checkbox("Mowing Reminders", value=True)
    notify_weather = st.checkbox("Weather Alerts", value=True)
    
    st.write("Note: Notifications are simulated in the Streamlit version.")
    
    # Save settings button
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
    
elif page == "About":
    st.header("About TurboLawn")
    
    st.write("""
    TurboLawn is a smart lawn care assistant that provides personalized recommendations 
    for watering and mowing your lawn based on real-time weather data and local conditions.
    
    ### Features:
    - Real-time weather monitoring
    - Smart watering recommendations
    - Optimal mowing schedules
    - Location-based advice
    
    ### How It Works:
    TurboLawn analyzes current weather conditions, forecasts, and historical data to provide 
    tailored lawn care advice. The recommendations consider factors like temperature, rainfall, 
    humidity, and your specific grass type.
    
    ### Coming Soon:
    - Fertilization scheduling
    - Pest control recommendations
    - Lawn health tracking
    - Mobile app version
    """)

# Footer
st.markdown("---")
st.markdown("TurboLawn © 2025 | Smart Lawn Care Assistant")
