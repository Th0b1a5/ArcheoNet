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

st.markdown("""
<style>
.st-key-logout button {
	background-color: #e86464 !important;
	color: #31333F !important;
}
			
.st-key-logout button:hover {
	background-color: #f25050 !important;
}
			
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = ""

try:
	userID = (st.session_state['userID'])
	username = (st.session_state['username'])
except:
	st.switch_page(r"login.py")

if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")

styles.apply()

if st.session_state.page == "login":
	st.toast(f"Přihlášen jako :blue[{username}]", icon="🔑", duration="short")

st.session_state.page = Path(__file__).name.replace('.py', '')
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")


# ======= Page =======
st.title(f"Vítejte {username}!")

st.caption(f"Poslední aktualizace: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()

# ======= NAVIGATION BUTTONS =======
if st.button("Zveřejnit místo"):
	st.switch_page("pages/map_post.py")

if st.button("Mapa"):
	st.switch_page("pages/map.py")


if st.button("Extra"):
	st.switch_page("pages/pages.py")

if st.button("Odhlásit", key="logout"):
	st.session_state["seznam_token"] = None
	st.logout()
	st.session_state["userID"] = None
	st.rerun()



# Launch app: streamlit run app.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
# streamlit run app.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
