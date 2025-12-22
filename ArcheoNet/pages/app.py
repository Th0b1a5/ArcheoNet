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

# ===== SCRIPTS =====
st.set_page_config(
	page_title="ArcheoNet DEV VERSION (alpaha)",
	page_icon="📚",
	layout="wide",
	initial_sidebar_state="collapsed"
)

if "page" not in st.session_state:
    st.session_state.page = ""

st.session_state.page = Path(__file__).name.replace('.py', '')
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")

try:
	username = (st.session_state['userID'])
except:
	st.switch_page(r"login.py")

if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")
	
styles.apply()

# ======= Page =======
st.title("ArcheoNet DEV DEMO VERSION")
st.success(f"Logged in as {username}")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

# ======= NAVIGATION BUTTONS =======

if st.button("Actions"):
	st.switch_page("pages/pages.py")


# Launch app: streamlit run app.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
# streamlit run app.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
