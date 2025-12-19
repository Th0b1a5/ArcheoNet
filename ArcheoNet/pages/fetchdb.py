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

import modules.get_ip as get_ip
import modules.location as location
import modules.styles as styles


try:
	username = (st.session_state['userID'])
except:
	st.switch_page("login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")
 
st.set_page_config(
    page_title="ArcheoNet DEV VERSION (alpaha) Login",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

styles.apply()

if 'lenght' not in st.session_state:
    st.session_state.lenght = 5

# ======= Database stuff =======
conn = sqlite3.connect('database/map_posts.db')
# Return in dictionary format
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

def filters():
    lat_values = st.slider("Latitude:", 50.0878114, 50.0978114,(50.0878114, 50.0978114), step=0.00001, format="%.7f")
    st.write(lat_values)

def fetch_db():
    cursor.execute(f"SELECT * FROM map_posts ORDER BY timestamp DESC LIMIT {st.session_state.lenght}")
    posts = cursor.fetchall()
    
    if not posts:
        st.write("No posts found in the database.")
        return
    
    for post in posts:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"Name: {post['name']}")
            st.write(f"Description: {post['description']}")
            st.write(f"Location: ({post['latitude']}, {post['longitude']})")
            st.write(f"Owner: {post['owner']}")
            st.write(f"Timestamp: {post['timestamp']}")
            st.write(f"ID: {post['id']}")
            st.write("--------------")
        with col2:
            image = post['image']
            st.image(image, width=400)

    if st.button("Fetch more"):
        st.session_state.lenght = st.session_state.lenght + 1
        st.rerun()
    

filters()

fetch_db()
