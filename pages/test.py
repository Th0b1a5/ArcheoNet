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
      

st.markdown("""
<style>
.st-key-btn1 button {
	position: fixed !important;
			
	bottom: 96px !important;
	right: 12px !important;
			
	z-index: 1 !important;
			
	width: 150px !important;

}
			
.st-key-btn2 button {
	position: fixed !important;
			
	bottom: 96px !important;
	left: 12px !important;
			
	z-index: 1 !important;
			
	width: 150px !important;

}
			
</style>
""", unsafe_allow_html=True)

st.button("Btn1", key="btn1")

st.button("Btn2", key="btn2")

for i in range(20):
	st.write(".............")