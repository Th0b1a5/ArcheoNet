import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import pandas as pd
import numpy as np
from streamlit.runtime import get_instance
from datetime import datetime
import pydeck as pdk
import time
import socket



# ===== SCRIPTS =====
ip = """
async function getClientIP() {
  try {
    const response = await fetch('https://api.ipify.org?format=json');
    const data = await response.json();
    return data.ip;
  } catch (error) {
    return 'IP not available';
  }
}
getClientIP();
"""

ip = streamlit_js_eval(js_expressions=ip)
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {ip}")
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
      latitude: 0.00,
      longitude: 0.00,
      accuracy: 0.00,
      error: err.message
    })
  );
});
"""

loc = streamlit_js_eval(js_expressions=getgeolocation, key="getgeolocation")

#print(loc["latitude"])

try:
    latitude = loc["latitude"]
    longitude = loc["longitude"]

    st.write(loc)
    st.write(f"Latitude: {latitude}")
    st.write(f"Longitude: {longitude}")
except:
    latitude = 0.00
    longitude = 0.00
    st.write("Location data is not available.")




map_point = pd.DataFrame({
    "latitude": [latitude],
    "longitude": [longitude]
    
    
})

st.map(map_point)



# Launch app: streamlit run app.py --server.sslCertFile=cert.pem --server.sslKeyFile=key.pem
# streamlit run app.py --server.sslCertFile=cert.pem --server.sslKeyFile=key.pem
