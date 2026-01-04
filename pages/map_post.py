import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import pandas as pd
import numpy as np
from streamlit.runtime import get_instance
from datetime import datetime
from pathlib import Path
import pydeck as pdk
import sqlite3
import time
import socket
import secrets
import re
from PIL import Image, ImageOps
import io

import modules.get_ip as get_ip
import modules.location as location
import modules.styles as styles

# ======= Setup and scripts =======
st.set_page_config(
	page_title="ArcheoNet DEV VERSION (alpaha)",
	page_icon="📚",
	layout="wide",
	initial_sidebar_state="collapsed"
)

try:
	userID = (st.session_state['userID'])
	username = (st.session_state['username'])
except:
	st.switch_page(r"login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")

try:
	if st.session_state["last_state"] == None or st.session_state["last_state"] == "":
		st.session_state["last_state"] = ""
except:
    st.session_state["last_state"] = ""

if st.session_state.page != "map_post":
	st.session_state["last_state"] = ""

st.session_state.page = Path(__file__).name.replace('.py', '')
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")

# ======= Database setup =======
conn = sqlite3.connect(r"database/map_posts.db")
cursor = conn.cursor()
try:
	cursor.execute("""CREATE TABLE IF NOT EXISTS map_posts    (
					latitude REAL,
					longitude REAL,
					name TEXT,
					description TEXT,
					owner TEXT,
					image BLOB,
					timestamp TEXT,
					type TEXT,
					id TEXT PRIMARY KEY
		)""")
	conn.commit()
except sqlite3.OperationalError:
	print("Error in creating or accessing the database")

# ======= Styles =======
styles.apply()

# ======= Functions =======
def generate_id(lat, lon, name, username):
	try:
		chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
		timestamp = datetime.now().strftime("%d.%m.%y..%H.%M.%S")
		name = re.sub(r"[^a-zA-Z0-9]+", "", name)
		username = re.sub(r"[^a-zA-Z0-9]+", "", username)

		id = str(lat) + ":" + str(lon) + ":" + str(name) + ":" + str(username) + ":" + str(timestamp) + ":" + ''.join(secrets.choice(chars) for _ in range(6))
		return id
	except:
		return None

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
		if latitude == 0 and longitude == 0:
			latitude = None
			longitude = None
	except:
		latitude = None
		longitude = None

	return latitude, longitude


def map_post():
	# ======= Get data from user =======	
	name = st.text_input("Name your find!", key="post_name")
	description = st.text_area("Describe your find!", key="post_description")
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	post_type = st.selectbox(
		"Select post type",
		["Underground", "Building", "Location", "Small object", "Medium object", "Large object"]
     )	# ADD POST TYPES
	

	uploaded_file = st.file_uploader("Take a picture!")
	image = None
	if uploaded_file:
		image = Image.open(uploaded_file)
		image = ImageOps.exif_transpose(image)  # Auto-rotate based on EXIF tag
		st.image(image)
		# Convert image to bytes
		img_byte_arr = io.BytesIO()
		image.save(img_byte_arr, format='JPEG', quality=50)  # or use uploaded_file.type.split('/')[-1].upper() for format
		image = img_byte_arr.getvalue()

  
	# ======= User location =======
	if st.toggle("Share location", True):
		latitude, longitude = get_geolocation()
		st.header("Your location")
		if latitude == None or latitude == "":
			st.error("GPS is not enabled or unavatible. Please chaeck that you have enabled GPS in the perrmission settings on your phone.")
		else:

			user_pos = pd.DataFrame({
				"latitude": [latitude],
				"longitude": [longitude]
			})

			st.map(user_pos, height=200)
	else:
		latitude, longitude = None, None

	# ======= Submit post handling =======
	if st.button("Post", use_container_width=True):
		if name == None or name == "":
			st.session_state["last_state"] = "Fill in the name"
			st.rerun()

		elif description == None or description == "":
			st.session_state["last_state"] = "Fill in the description"
			st.rerun()	

		elif latitude == None or longitude == None:
			pass

		elif image == None or image == "":
			st.session_state["last_state"] = "An image is required for a post"		
			st.rerun()

		elif timestamp == None or timestamp == "":
			st.session_state["last_state"] = "An error has occured: Timestamp generation error."
			st.rerun()

		else:
			id = generate_id(latitude, longitude, name, userID) # Move to the end!
			
			if id == None or id == "":
				st.session_state["last_state"] = "ID generation error. Please try again later."
				st.error("An error has occured: ID generation error. Please try again later.")

			else:
				try:
					cursor.execute("""
						INSERT INTO map_posts (latitude, longitude, name, description, owner, image, timestamp, type, id)
						VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
					""", (latitude, longitude, name, description, username, image, timestamp, post_type,id))
					conn.commit()
					st.switch_page("pages/post_success.py")
     
				except sqlite3.IntegrityError:
					st.session_state["last_state"] = "An error has occured: Duplicate ID. Please try again later."	
					st.error("An error has occured: Duplicate ID. Please try again later.")
					st.rerun()		

def display_warnings(warning):
	if warning != None and warning != "":
		st.warning(warning)
		st.toast(warning, icon="⚠️")
		st.session_state["last_state"] = None
	
# ======= Page =======
st.title("Create a map post")

display_warnings(st.session_state["last_state"])
map_post()


# Keep in ming we might migrate to postgres if we win the FLL championships, so dont go crazy with SQLite