import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
import requests

'''
# Infernal Carriage Cost Conjurer
'''

url = 'https://taxifare.lewagon.ai/predict'
nyc_lat, nyc_lon = 40.790021078001466, -73.95900840535145

def create_clickable_map(lat, lon, pickup_lat=None, pickup_lon=None, dropoff_lat=None, dropoff_lon=None, zoom_start=12):
    m = folium.Map(location=[lat, lon], zoom_start=zoom_start)
    folium.LatLngPopup().add_to(m)

    if pickup_lat and pickup_lon:
        folium.Marker([pickup_lat, pickup_lon], popup='Origin', icon=folium.Icon(color='green')).add_to(m)
    if dropoff_lat and dropoff_lon:
        folium.Marker([dropoff_lat, dropoff_lon], popup='Final Destination', icon=folium.Icon(color='red')).add_to(m)

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
        pickup_lat = st.number_input('Origin of the Damned [lat]', format="%.6f", value=40.8063)

    with col_lng_from:
        pickup_long = st.number_input('Origin of the Damned [long]', format="%.6f", value=-73.9562)

    col_lat_to, col_lng_to = st.columns(2)

    with col_lat_to:
        dropoff_lat = st.number_input('Final Stop [lat]', format="%.6f", value=40.731000)

    with col_lng_to:
        dropoff_long = st.number_input('Final Stop [long]', format="%.6f", value=-73.991500)

    col1, col2, col3 = st.columns(3)

    with col1:
        date = st.date_input("Doomsday Date")

    with col2:
        t = st.time_input("Time of Reckoning")

    with col3:
        passengers = st.number_input('Damned Souls', min_value=1, max_value=10, value=1, step=1)

    datetime_str = datetime.combine(date, t).strftime("%Y-%m-%d %H:%M:%S")
    predict_button = st.form_submit_button(label='Summon Estimate')

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
            @import url('https://fonts.googleapis.com/css2?family=Creepster&display=swap');
            /* Apply custom font and colors */
            h1, h2, h3, h4, h5, h6, label, .caption, .st-bb {{
                font-family: 'Creepster', cursive;
                color: #ff4500; /* Orangish red, similar to "hellfire" */
            }}
            /* Customize the button to a hellish theme */
            .stButton>button {{
                color: #ffffff;
                border-color: #ff4500;
                background-color: #800000; /* Maroon */
            }}
            .stButton>button:hover {{
                'background-color': #ff4500; /* Orangish red when hovered over */
            }}
            /* Customize input and select fields */
            input, select{{
                background-color: #ff4500;
                color: #ffffff;
                border-color: #800000;
            }}
            .stApp {{
                background-image: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), url("https://plus.unsplash.com/premium_photo-1667241634914-3d63759c0789?auto=format&fit=crop&q=80&w=3628&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
                background-size: cover;
                background-position: center center;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
