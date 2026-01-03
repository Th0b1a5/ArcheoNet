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

import modules.get_ip as get_ip
import modules.location as location
import modules.styles as styles

st.session_state.page = Path(__file__).name.replace('.py', '')
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")

try:
	userID = (st.session_state['userID'])
	username = (st.session_state['username'])
except:
	st.switch_page(r"login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")

# ===== SETUP =====
st.set_page_config(
    page_title="ArcheoNet DEV VERSION (alpaha) Login",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

styles.apply()

if st.button("Make a post"):
	st.switch_page("pages/map_post.py")
	
if st.button("Browse posts"):
	st.switch_page("pages/posts.py")

if st.button("Map"):
	st.switch_page("pages/map.py")
	
if st.button("Testpage"):
	st.switch_page("pages/test.py")
	
if st.button("Test 2"):
	st.switch_page("pages/test2.py")
	
if st.button("Slideup"):
	st.switch_page("pages/slideup.py")

if st.button("fetchdb"):
	st.switch_page("pages/fetchdb.py")
 
if st.button("Map tests"):
	st.switch_page("pages/map_tests.py")
 
if st.button("Imovable button"):
	st.switch_page("pages/floating_button.py")

if st.button("Back"):
	st.switch_page("pages/app.py")

