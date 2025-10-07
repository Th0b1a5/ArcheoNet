import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import pandas as pd
import numpy as np
from datetime import datetime
import time

# ===== SCRIPTS =====
print(f"Device connected! {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
# ===== BASIC PAGE SETUP =====
st.set_page_config(
    page_title="ArcheoNet DEV VERSION (alpaha)",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======= Title =======
st.title("ArcheoNet DEV DEMO VERSION")


# ======= MAP DEMO =======
st.header("Map Demo")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

df = pd.DataFrame({
    'latitude': [37.7749551, 34.0522, 40.7128],
    'longitude': [-122.41941465, -118.2437, -74.0060]
})
st.map(df)


# ===== REQUEST USER LOCATION OLD =====
st.title("Request User Location in Streamlit - Old")

location = streamlit_geolocation()

if location["longitude"] != None and location["latitude"] != None:
    latitude = location["latitude"]
    longitude = location["longitude"]
    st.write(f"Latitude: {location["latitude"]}, Longitude: {location["longitude"]}")

    current_pos = pd.DataFrame({
        'latitude': [latitude],
        'longitude': [longitude],
    })

else:
    current_pos = pd.DataFrame({
        'latitude': [0.0],
        'longitude': [0.0],
    })

st.map(current_pos, color="#008000", size=10)


# ======= USER LOCATION - NEW =======
st.title("Request User Location in Streamlit - New")

if st.checkbox("Check my location"):
    loc = get_geolocation()
    st.write(f"Your coordinates are {loc}")

# ======= CUSTOM COMPONENT =======
st.title("Request User Location in Streamlit - Custom Component")

getgeolocation = """
new Promise((resolve, reject) => {
  navigator.geolocation.getCurrentPosition(
    pos => resolve({
      latitude: pos.coords.latitude,
      longitude: pos.coords.longitude,
      accuracy: pos.coords.accuracy,
      error: null
    }),
    err => resolve({
      latitude: null,
      longitude: null,
      accuracy: null,
      error: err.message
    })
  );
});
"""

loc = streamlit_js_eval(js_expressions=getgeolocation, key="getgeolocation")

if loc is not None:
    st.write(loc)
    st.write(f"Latitude: {loc["latitude"]}")
    st.write(f"Longitude: {loc["longitude"]}")
else:
    st.write("Location data is not available.")




# Launch app: streamlit run app.py --server.sslCertFile=cert.pem --server.sslKeyFile=key.pem
# streamlit run app.py --server.sslCertFile=cert.pem --server.sslKeyFile=key.pem
