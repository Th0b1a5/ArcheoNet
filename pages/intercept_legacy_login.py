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
      
styles.apply()
      
st.markdown("""
<style>
.stApp {
    background-color: #fa3123; /* A light gray */
}
h1 {
	text-align: center;
	font-size: 5rem !important; /* Make it huge */
	font-family: 'Courier New', monospace; /* Change font */
	padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)
st.title("WARNING")
st.header("You are trying to log in with a DEPRECATED LEGACY method.")

st.markdown("""
<body>
	<br>
</body>
""", unsafe_allow_html=True)

st.header("We STRONGLY recommend you to use Google or Seznam login instead. Please press the return button below to return.")

if st.button("Return back to login"):
    st.switch_page("login.py")

st.write("Wait 5s to continue...")

time.sleep(5)

if st.button("Continue to legacy login"):
    st.switch_page("pages/legacy_login.py")