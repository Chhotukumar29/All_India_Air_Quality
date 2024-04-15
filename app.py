import streamlit as st
import joblib 
import pandas as pd
import numpy as np 

# # Loading model
# model = joblib.load('src/Notebook/model_joblib')

# # Function to make predictions with expanded features
# def predict_air_quality(features):
#     prediction = model.predict(features)
#     return prediction[0]

# # Air quality categorization function
# def air_quality(aqi_value):
#     if aqi_value <= 50:
#         return "Good"
#     elif 51 <= aqi_value <= 100:
#         return "Moderate"
#     elif 101 <= aqi_value <= 200:
#         return "Poor"
#     elif 201 <= aqi_value <= 300:
#         return "Unhealthy"
#     elif 301 <= aqi_value <= 400:
#         return "Very Unhealthy"
#     else:
#         return "Hazardous"

# # title of the app
# st.title('Air Quality Prediction App')

# # Geographical and weather inputs
# lat = st.number_input('Latitude', format="%.5f")
# lon = st.number_input('Longitude', format="%.5f")
# elevation = st.number_input('Elevation (in meters)', format="%.2f")
# co_ppb = st.number_input('CO (ppb)')
# no2_ppb = st.number_input('NO2 (ppb)')
# o3_ppb = st.number_input('O3 (ppb)')
# pm10 = st.number_input('PM10 (ug/m3)')
# pm25 = st.number_input('PM2.5 (ug/m3)')
# so2_ppb = st.number_input('SO2 (ppb)')
# t_C = st.number_input('Temperature (°C)')
# p_mb = st.number_input('Pressure (mb)')
# dew_C = st.number_input('Dew Point (°C)')
# humidity = st.number_input('Humidity (%)')
# wind_speed = st.number_input('Wind Speed (km/h)')
# wind_direction = st.number_input('Wind Direction (°)')

# if st.button('Predict Air Quality (AQI)'):
#     features = np.array([[lat, lon, elevation, co_ppb, no2_ppb, o3_ppb, pm10, pm25, so2_ppb, t_C, p_mb, dew_C, humidity, wind_speed, wind_direction]])
#     aqi = predict_air_quality(features)
#     aqi_category = air_quality(aqi)
#     st.write(f'Predicted Air Quality (AQI): {aqi:.2f}')
#     st.write(f'Air Quality Category: {aqi_category}')
    
    

# -------------------------------------------------------------------------------------------

from src.pipeline.predict_pipeline import predict_pipeline 
from sklearn.impute import SimpleImputer
import streamlit as st
import joblib
import numpy as np 

# Load the model
try:
    model = joblib.load('src/Notebook/model_joblib')
except Exception as e:
    st.error(f"Error loading the model: {e}")
    st.stop()

# Function to preprocess input data and predict AQI
def predict_aqi(lat, lon):
    try: 
        # Concatenate latitude, longitude, and other features
        input_features = predict_pipeline(lat,lon)
        
        # Make prediction
        aqi = model.predict(input_features)
        return aqi[0]  # Return the predicted AQI
    except Exception as e: 
        st.error(f"Error predicting AQI: {e}")
        return None

# Function to determine air quality category based on AQI value
def air_quality(aqi_value):
    if aqi_value <= 50:
        return "Good"
    elif 51 <= aqi_value <= 100:
        return "Moderate"
    elif 101 <= aqi_value <= 200:
        return "Poor"
    elif 201 <= aqi_value <= 300:
        return "Unhealthy"
    elif 301 <= aqi_value <= 400:
        return "Very Unhealthy"
    else:
        return "Hazardous"

# Streamlit app
def main():
    st.title("Air Quality Prediction System")

    # User input for latitude and longitude
    lat = st.number_input("Enter Latitude:", value=0.0, step=0.0001, format="%.4f")  
    lon = st.number_input("Enter Longitude:", value=0.0, step=0.0001, format="%.4f")  

    # Predict AQI when user clicks the button
    if st.button("Predict AQI"):
        # Call prediction function
        aqi = predict_aqi(lat, lon)
        if aqi is not None:
            aqi_rounded = round(aqi, 0)
            st.write(f"Predicted AQI: {aqi_rounded}")
            # Call air quality function
            quality = air_quality(aqi_rounded)
            st.write(f"AQI Status: {quality}")

if __name__ == "__main__":
    main()

