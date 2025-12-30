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
	username = (st.session_state['userID'])
except:
	st.switch_page("login.py")
	
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")
	
# Initialize session state for toggle
if "slide_up_visible" not in st.session_state:
    st.session_state.slide_up_visible = False

def toggle_slide_up():
    st.session_state.slide_up_visible = not st.session_state.slide_up_visible



# ------- PAGE CONTENT -------
st.title("Slide Up Window Example")

# Button to toggle sliding div
st.button("Toggle Slide Up Window", on_click=toggle_slide_up)

# CSS styles for sliding div
slide_up_css = """
<style>
#slide-up-window {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 70vh; 
  background-color: var(--primary-color);
  border-top: 3px solid #666;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
  overflow: auto;
  transition: transform 0.4s ease-in-out;
  transform: translateY(100%);
  z-index: 9999;
  padding: 20px;
}
#slide-up-window.open {
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
.close {
  position: absolute;
  top: 20px;
  right: 20px;
}
</style>
"""

# Embed the CSS
st.markdown(slide_up_css, unsafe_allow_html=True)

# ------- HTML DIV FOR SLIDING WINDOW -------
current_file_dir = Path(__file__).parent  # This gets ".../Project folder/pages"
project_root = current_file_dir.parent    # This gets ".../Project folder"
image_path = project_root / "resources" / "close-light.png"

# ------- LOAD IMAGE AS BASE64 -------
img_src = ""
if image_path.exists():
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    img_src = f"data:image/png;base64,{encoded_string}"
else:
    st.error(f"Could not find image at: {image_path}")

slide_up_html = f"""
<div id="slide-up-window" class="{ 'open' if st.session_state.slide_up_visible else '' }">
  <h3>This is the sliding window content</h3>
  <p>You can put any normal text or other Streamlit elements here.</p>
  <h2>Name of creator</h2>
  <img src="{img_src}" height="20" class="close" onclick="closeOverlay()" />
</div>

"""

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
    margin: 100px auto;
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

st.markdown(slide_up_html, unsafe_allow_html=True)
