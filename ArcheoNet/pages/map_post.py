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
import io
import re
import time
import socket
import secrets

# ======= Setun and scripts =======
st.set_page_config(
	page_title="ArcheoNet DEV VERSION (alpaha)",
	page_icon="📚",
	layout="wide",
	initial_sidebar_state="collapsed"
)

try:
	username = (st.session_state['userID'])
except:
	st.switch_page("login.py")

if st.session_state["userID"] == None:
	st.switch_page("login.py")

   
conn = sqlite3.connect("map_posts.db")
cursor = conn.cursor()
try:
	cursor.execute("""CREATE TABLE IF NOT EXISTS map_posts    (
					latitude REAL,
					longitude REAL,
					owner TEXT,
					timestamp TEXT,
					description TEXT,
					image BLOB,
					id TEXT PRIMARY KEY
		)""")
	conn.commit()
except sqlite3.OperationalError:
	print("Error in creating or accessing the database")

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

st.markdown("""
<style>
div.stButton > button {
    width: 87vw;
    margin: 10px auto;
    display: block;
    font-size: 1.2em;
    padding: 1em 0.5em;
}
</style>
""", unsafe_allow_html=True)

def generate_id(lat, lon, name, username):
	chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	timestamp = datetime.now().strftime("%d.%m.%y..%H.%M.%S")
	name = re.sub(r"[^a-zA-Z0-9]+", "", name)
	username = re.sub(r"[^a-zA-Z0-9]+", "", username)

	id = str(lat) + ":" + str(lon) + ":" + str(name) + ":" + str(username) + ":" + str(timestamp) + ":" + ''.join(secrets.choice(chars) for _ in range(6))
	return id

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
	latitude, longitude = get_geolocation()

	uploaded_file = st.file_uploader("Take a picture!", type=["jpg", "jpeg", "png"])
	if uploaded_file:
		image = Image.open(uploaded_file)
		image = ImageOps.exif_transpose(image)  # Auto-rotate based on EXIF tag
		st.image(image)
		# Convert image to bytes
		img_byte_arr = io.BytesIO()
		image.save(img_byte_arr, format='PNG')  # or use uploaded_file.type.split('/')[-1].upper() for format
		image = img_byte_arr.getvalue()

  
	# ======= User location =======
	st.header("Your location")

	user_pos = pd.DataFrame({
		"latitude": [latitude],
		"longitude": [longitude]
	})

	st.map(user_pos)

	if st.button("Post", use_container_width=True):
		id = generate_id(latitude, longitude, name, username) # Move to the end!
		st.write(id)
		cursor.execute("""
			INSERT INTO map_posts (latitude, longitude, owner, timestamp, description, image, id)
			VALUES (?, ?, ?, ?, ?, ?, ?)
		""", (latitude, longitude, username, timestamp, description, image, id))
		conn.commit()


	
# ======= Page =======

map_post()
