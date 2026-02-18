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
import psycopg2
from psycopg2.extras import RealDictCursor
import html

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
	name = st.text_input("Pojmenujte váš nález", key="post_name")
	description = st.text_area("Popište co jste našli", key="post_description")
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	post_type = st.selectbox(
		"Vyberter materiál nálezu",
		["Keramika", "Kov", "Kámen", "Kost", "Jiné", "Neznámé"]
	)

	uploaded_file = st.file_uploader("Vyfoťte to")
	image = None
	if uploaded_file:
		try:
			image = Image.open(uploaded_file)
			image = ImageOps.exif_transpose(image)
			image = image.convert('RGB')
			image.thumbnail((1920, 1920))
			st.image(image)

			img_byte_arr = io.BytesIO()
			image.save(img_byte_arr, format='JPEG', quality=40, optimize=True)
			image = img_byte_arr.getvalue()
		except:
			st.error("Nepodařilo se načíst obrázek, zkuste to prosím znovu.")
			image = None
  
	# ======= User location =======

	latitude, longitude = get_geolocation()
	st.header("Vaše pozice")
	if latitude == None or latitude == "":
		st.error("GPS není dostupná, prosím zkontrolujte že máte polohové služby zapnuté a povolené oprávnění")
	else:

		user_pos = pd.DataFrame({
			"latitude": [latitude],
			"longitude": [longitude]
		})

		st.map(user_pos, height=200)


	# ======= Submit post handling =======
	if st.button("Zveřejnit", use_container_width=True):
		if name == None or name == "":
			st.session_state["last_state"] = "Vyplňte název"
			st.rerun()

		elif description == None or description == "":
			st.session_state["last_state"] = "Vyplňte popisek"
			st.rerun()	

		elif latitude == None or longitude == None:
			pass

		elif image == None or image == "":
			st.session_state["last_state"] = "Obrázek je vyžadován aby jste mohli pokračovat"		
			st.rerun()

		elif timestamp == None or timestamp == "":
			st.session_state["last_state"] = "Chyba generace času, server error. Prosím kontaktujte ArcheoNet tým přes email."
			st.rerun()

		else:
			id = generate_id(latitude, longitude, name, userID) # Move to the end!
			
			if id == None or id == "":
				st.session_state["last_state"] = "Chyba generování ID, zkuste to prosím později."
				st.error("Chyba generování ID, zkuste to prosím později.")

			else:
				try:
					conn = psycopg2.connect(
						host=st.secrets["postgres"]["host"],
						port=st.secrets["postgres"]["port"],
						dbname=st.secrets["postgres"]["dbname"],
						user=st.secrets["postgres"]["user"],
						password=st.secrets["postgres"]["password"],
						sslmode="require"
					)
					cursor = conn.cursor(cursor_factory=RealDictCursor)
     
					try:
						cursor.execute("""CREATE TABLE IF NOT EXISTS map_posts    (
										latitude REAL,
										longitude REAL,
										name TEXT,
										description TEXT,
										owner TEXT,
										image BYTEA,
										timestamp TEXT,
										type TEXT,
										id TEXT PRIMARY KEY,
										userID TEXT,
					 					position INTEGER
							)""")
						conn.commit()
					except psycopg2.DatabaseError:
						print("Error in creating or accessing the database")
						st.session_state["last_state"] = "Chyba přístupu k databázi, zkuste to prosím později."
						cursor.close()
						conn.close()
						st.rerun()
        
					cursor.execute("""
						INSERT INTO map_posts (latitude, longitude, name, description, owner, image, timestamp, type, id, userID)
						VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
					""", (latitude, longitude, html.escape(name), html.escape(description), username, image, timestamp, html.escape(post_type), html.escape(id), userID))
					conn.commit()
     
					cursor.close()
					conn.close()
     
					st.switch_page("pages/post_success.py")
     
				except psycopg2.IntegrityError:
					st.session_state["last_state"] = "Chyba, zkuste to prosím později: Duplicate ID generated."	
					st.error("Chyba, zkuste to prosím později: Duplicate ID generated.")
					cursor.close()
					conn.close()
					st.rerun()	
     
				except Exception as e:
					st.session_state["last_state"] = "Chyba, zkuste to prosím později"
					print(e)
					st.error("Chyba, zkuste to prosím později")
					st.rerun()	

def display_warnings(warning):
	if warning != None and warning != "":
		st.warning(warning)
		st.toast(warning, icon="⚠️")
		st.session_state["last_state"] = None
	
# ======= Page =======
st.title("Vytvořte příspěvek")

display_warnings(st.session_state["last_state"])
map_post()


# Keep in ming we might migrate to postgres if we win the FLL championships, so dont go crazy with SQLite