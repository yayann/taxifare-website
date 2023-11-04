import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
import requests

'''
# Straight To Hell Taxi Fare Prediction
'''

url = 'https://taxifare.lewagon.ai/predict'
nyc_lat, nyc_lon = 40.790021078001466, -73.95900840535145

def create_clickable_map(lat, lon, pickup_lat=None, pickup_lon=None, dropoff_lat=None, dropoff_lon=None, zoom_start=12):
    m = folium.Map(location=[lat, lon], zoom_start=zoom_start)
    folium.LatLngPopup().add_to(m)

    if pickup_lat and pickup_lon:
        folium.Marker([pickup_lat, pickup_lon], popup='Pickup', icon=folium.Icon(color='green')).add_to(m)
    if dropoff_lat and dropoff_lon:
        folium.Marker([dropoff_lat, dropoff_lon], popup='Dropoff', icon=folium.Icon(color='red')).add_to(m)

    return m


def query_api(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count):
    params = {
        "pickup_datetime": pickup_datetime,
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }
    response = requests.get(url, params=params).json()
    return round(float(response['fare']), 2)


with st.form("taxifare_input_form"):
    col_lat_from, col_lng_from = st.columns(2)

    with col_lat_from:
        pickup_lat = st.number_input('Pickup lat:', format="%.6f", value=40.8063)

    with col_lng_from:
        pickup_long = st.number_input('Pickup long:', format="%.6f", value=-73.9562)

    col_lat_to, col_lng_to = st.columns(2)

    with col_lat_to:
        dropoff_lat = st.number_input('Dropoff lat:', format="%.6f", value=40.731000)

    with col_lng_to:
        dropoff_long = st.number_input('Dropoff long:', format="%.6f", value=-73.991500)

    col1, col2, col3 = st.columns(3)

    with col1:
        date = st.date_input("Choose a date")

    with col2:
        t = st.time_input("Choose a time")

    with col3:
        passengers = st.number_input('Num passengers:', min_value=1, max_value=10, value=1, step=1)

    datetime_str = datetime.combine(date, t).strftime("%Y-%m-%d %H:%M:%S")
    predict_button = st.form_submit_button(label='Predict the fare')

if predict_button:
    m = create_clickable_map(nyc_lat, nyc_lon, pickup_lat, pickup_long, dropoff_lat, dropoff_long, zoom_start=12)
    folium_static(m)
    prediction = query_api(datetime_str, pickup_long, pickup_lat, dropoff_long, dropoff_lat, passengers)
    st.markdown(f"## Your fare would be about _${prediction}_")
else:
    m = create_clickable_map(nyc_lat, nyc_lon, zoom_start=12)
    folium_static(m)


st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), url("https://plus.unsplash.com/premium_photo-1667241634914-3d63759c0789?auto=format&fit=crop&q=80&w=3628&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-size: cover;
            background-position: center center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
