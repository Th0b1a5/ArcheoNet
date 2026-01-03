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
import base64

import modules.get_ip as get_ip
import modules.location as location
import modules.styles as styles
from pages.floating_button import toggle_slide_up

# ======= SETUP AND SCRIPTS =======
st.set_page_config(
	page_title="ArcheoNet DEV VERSION (alpaha)",
	page_icon="📚",
	layout="wide",
	initial_sidebar_state="collapsed"
)

st.session_state.page = Path(__file__).name.replace('.py', '')
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")

try:
	userID = (st.session_state['userID'])
	username = (st.session_state['username'])
except:
	st.switch_page(r"login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")
	
# Initialize session state for toggle
if "display_window" not in st.session_state:
    st.session_state.display_window = False

def toggle_display_window():
    st.session_state.display_window = not st.session_state.display_window



# ------- PAGE CONTENT -------
st.title("Slide Up Window Example")

# Button to toggle sliding div
st.button("Toggle Window", on_click=toggle_display_window)

# CSS styles for sliding div
display_window_css = """
<style>
#display_window {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 65vh; 
  background-color: var(--primary-color);
  border-top: 3px solid #666;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
  overflow: auto;
  transition: transform 0.4s ease-in-out;
  transform: translateY(100%);
  z-index: 9999;
  padding: 30px;
}
#display_window.open {
  transform: translateY(0);
}
button.inner-btn {
  margin: 5px;
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
}
button.inner-btn:hover {
  background-color: #0056b3;
  cursor: pointer;
}
div.stButton > button[kind="primary"] {
  position: fixed;
  bottom: 58vh;
  right: 25px;
  z-index: 10000;
  width: 40px;
  height: 40px;

}
</style>
"""

# Embed the CSS
st.markdown(display_window_css, unsafe_allow_html=True)


  
print(st.session_state.display_window)

display_window_html = f"""
<div id="display_window" class="{ 'open' if st.session_state.display_window else '' }">

  <h2>Display Window Content</h2>
</div>

"""
st.markdown(display_window_html, unsafe_allow_html=True)

if st.session_state.display_window:
  time.sleep(0.32)  # Wait for the slide-up animation to complete
  st.button("✖", on_click=toggle_display_window, type="primary")
  #✖