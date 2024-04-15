import warnings
warnings.filterwarnings('ignore')
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def predict_pipeline(lat, lon):
    # API RUL
    API_URL = "https://api.aqi.in/api/v1/getIndiaLocations"
    response = requests.get(API_URL)
    # checking request was successful or not
    if response.status_code == 200:
        data1 = response.json()
        print(data1)
    else:
        print("Error:", response.status_code) # printing error
        
    data = pd.json_normalize(data1, 'Locations')

    sensor_val = pd.json_normalize(data['airComponents'])
    sensor_val.shape
    sensor = pd.DataFrame()
    for col in sensor_val.columns:
        col_name = sensor_val[col][0]['sensorName'] + "_" + sensor_val[col][0]['sensorUnit']
        sensor[col_name] = sensor_val[col].apply(lambda x: x['sensorData'])


    final_data = pd.merge(data, sensor, left_index = True, right_index = True)

    # dropping those column that are not needed for the prediction purpose.
    final_data.drop(columns = ['stationname', 'locationId','formatdate' ,'dev_type', 'updated_at', 'timeStamp', 'cityName', 'stateName',
        'countryName', 'source', 'sourceUrl', 'airComponents' ], inplace = True)

    final_data.columns

    final_data['lon'] = pd.to_numeric(data['lon'])
    final_data['lat'] = pd.to_numeric(data['lat'])
    final_data['Elevation'] = pd.to_numeric(data['Elevation'])

    # It is observed that the data AQI IN is 1094 and AQI-US is 0 which does not make any sense in the data. Thus dropping the data.
    final_data.drop(index = final_data[final_data['AQI-IN_IN-AQI'] > 1000].index, inplace = True)

    import math

    def haversine(lat1, lon1, lat2, lon2, earth_radius=6371.0):
        """
        Calculates the great circle distance between two points
        on the Earth's surface using the Haversine formula.

        :param lat1: Latitude of the first point
        :param lon1: Longitude of the first point
        :param lat2: Latitude of the second point
        :param lon2: Longitude of the second point
        :param earth_radius: Radius of the Earth (default is in kilometers)
        :return: Distance between the two points in kilometers
        """
        try:
            # Convert decimal degrees to radians
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

            # Haversine formula
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.asin(math.sqrt(a))
            distance = earth_radius * c
            return distance

        except Exception as e:
            raise e
        
    # User's location
    user_lat = float(lat)  # User's latitude
    user_lon = float(lon)  # User's longitude

    # Calculate distance for each location in the dataset
    final_data['distance'] = final_data.apply(lambda row: haversine(user_lat, user_lon, row['lat'], row['lon']), axis=1)

    # list of radii
    radii = [10, 20, 30 ,40, 50,70,80, 90, 100, 150]

    # Filter and store data for each radius
    for radius in radii:
        # Filter locations within the radius
        nearby_locations = final_data[final_data['distance'] <= radius]
        print(len(nearby_locations))
        # Check if there are any locations within the radius
        if len(nearby_locations) >= 3 :
            # Append the filtered dataframe to the list
            break

    nearby_locations.reset_index(inplace = True)

    nearby_locations['weights'] = nearby_locations.apply(lambda row: 1/row['distance'], axis = 1)
    weighted_values = nearby_locations.drop(columns = ['Elevation','index', 'lat', 'lon', 'distance','AQI-IN_IN-AQI','aqi_US-AQI'])
    
    weighted_values = weighted_values.apply(lambda row: row*row['weights'], axis = 1)
    weighted_values['weights'] = nearby_locations['weights']
    
    average_values = weighted_values.sum()/ weighted_values['weights'].sum()
    values= pd.DataFrame ([average_values], columns = weighted_values.columns).drop(columns = ['weights'])

    return values


    
    
    