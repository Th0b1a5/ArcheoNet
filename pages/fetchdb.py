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
import folium
from streamlit_folium import st_folium
from PIL import Image, ImageOps
import io
import psycopg2
from psycopg2.extras import RealDictCursor

import modules.get_ip as get_ip
import modules.location as location
import modules.styles as styles


if 'length' not in st.session_state:
    st.session_state.length = 1
    
if "page" not in st.session_state:
    st.session_state.page = "fetchdb"

if st.session_state.page != "fetchdb":
    st.session_state.length = 3

st.session_state.page = Path(__file__).name.replace('.py', '')
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")

try:
	userID = (st.session_state['userID'])
	username = (st.session_state['username'])
except:
	st.switch_page(r"login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")
 
st.set_page_config(
    page_title="ArcheoNet DEV VERSION (alpaha) Login",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

styles.apply()

# ======= Database stuff =======
def fetch_db():
    conn = psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        port=st.secrets["postgres"]["port"],
        dbname=st.secrets["postgres"]["dbname"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"]
    )

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    # DB and displaying posts
    cursor.execute("SELECT * FROM map_posts WHERE latitude IS NOT NULL ORDER BY timestamp DESC LIMIT %s", (st.session_state.length,))
    posts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    if not posts:
        st.write("No posts found in the database.")
        return
    
    for post in posts:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.header(f"{post['name']}")
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
        st.session_state.length = st.session_state.length + 2
        st.rerun()
    

fetch_db()
