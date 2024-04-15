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

