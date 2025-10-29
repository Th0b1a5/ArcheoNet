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

# ======= Setup and scripts =======
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
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")

conn = sqlite3.connect("map_posts.db")
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

st.markdown(
    """
    <style>
        div.block-container {
            padding-top: 0rem;      /* Adjust to taste */
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ======= Functions =======
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
		print("Location data is unavatible")

	return latitude, longitude


st.map()


