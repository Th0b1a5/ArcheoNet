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
import re
import time
import socket
import secrets

# ===== SCRIPTS =====
try:
	username = (st.session_state['userID'])
except:
	st.switch_page("login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")

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
    width: 90vw;
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

ip = """
async function getClientIP() {
  try {
	const response = await fetch('https://api.ipify.org?format=json');
	const data = await response.json();
	return data.ip;
  } catch (error) {
	return 'IP not available';
  }
}
getClientIP();
"""

ip = streamlit_js_eval(js_expressions=ip)
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {ip}")

st.set_page_config(
	page_title="ArcheoNet DEV VERSION (alpaha)",
	page_icon="📚",
	layout="wide",
	initial_sidebar_state="collapsed"
)




# ======= Page =======
st.title("ArcheoNet DEV DEMO VERSION")
st.success(f"Logged in as {username}")

st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.divider()
# ======= CREATE MAP MARKERS/POSTS =======

if st.button("Make a post"):
	st.switch_page("pages/map_post.py")

if st.button("Testpage"):
	st.switch_page("pages/test.py")


# Launch app: streamlit run app.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
# streamlit run app.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
