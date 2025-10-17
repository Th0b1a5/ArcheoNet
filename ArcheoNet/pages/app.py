import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link
import pandas as pd
import numpy as np
from streamlit.runtime import get_instance
from datetime import datetime
import pydeck as pdk
import sqlite3
import base64
from io import BytesIO
from PIL import Image, ImageOps
import time
import socket

# ===== SCRIPTS =====
try:
	username = (st.session_state['userID'])
except:
	st.switch_page("login.py")
if st.session_state["userID"] == None:
	st.switch_page("login.py")

   
conn = sqlite3.connect("map_posts.db")
cursor = conn.cursor()
try:
	cursor.execute("""CREATE TABLE map_posts    (
					longitude REAL,
					latitude REAL,
					owner TEXT,
					timamestamp TEXT,
					description TEXT,
					image BLOB
		)""")
	conn.commit()
except sqlite3.OperationalError:
	print("Table already exists")

st.markdown("""
<style>
[data-testid="stFileUploader"] button {
    padding: 0.4em 2em;
    border-radius: 0.5em;
    background-color: #0099ff;
    color: white;
    font-weight: 600;
    border: none;
    cursor: pointer;
    width: 100%;
    height: 50px;
}
</style>
""", unsafe_allow_html=True)


def get_geolocation():

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

	loc = (streamlit_js_eval(js_expressions=getgeolocation))

	try:
		latitude = loc["latitude"]
		longitude = loc["longitude"]
	except:
		latitude = 0.00
		longitude = 0.00
		print("Location data is unavatible")

	return latitude, longitude


def map_post():
	st.title("Create a map post")
	# ======= Get data from user =======	
 
	name = st.text_input("Name your find!", key="post_name")
	description = st.text_area("Describe your find!", key="post_description")
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	uploaded_file = st.file_uploader("Take a picture!", type=["jpg", "jpeg", "png"])
	if uploaded_file:
		img = Image.open(uploaded_file)
		img = ImageOps.exif_transpose(img)  # Auto-rotate based on EXIF tag
		st.image(img)
  
	# ======= User location =======
	st.header("Your location")
	user_loc = get_geolocation()
	latitude = user_loc[0]
	longitude = user_loc[1]


	user_pos = pd.DataFrame({
		"latitude": [latitude],
		"longitude": [longitude]
	})

	st.map(user_pos)




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

st.set_page_config(
	page_title="ArcheoNet DEV VERSION (alpaha)",
	page_icon="📚",
	layout="wide",
	initial_sidebar_state="collapsed"
)










# ======= Title =======
st.title("ArcheoNet DEV DEMO VERSION")
st.success(f"Logged in as {username}")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()
# ======= CREATE MAP MARKERS/POSTS =======

map_post()

if st.button("Testpage"):
	st.switch_page("pages/test.py")





# Launch app: streamlit run app.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
# streamlit run app.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
