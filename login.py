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
import urllib.parse
import requests
from streamlit_redirect import redirect
from streamlit_extras.exception_handler import set_global_exception_handler

import modules.get_ip as get_ip
import modules.location as location
import modules.styles as styles
import modules.exception_handler as excHandler

#set_global_exception_handler(excHandler.handler)
# ===== SETUP =====
st.set_page_config(
    page_title="ArcheoNet DEV VERSION (alpaha) Login",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    h1 {
        font-size: 16vw !important;  
        text-align: center !important;
        margin-bottom: 18px !important;
    }

    .st-key-google button {
        background-color: white !important;
        color: #31333F !important;
        border: 1px solid #d3d3d3 !important; 
            
        background-image: url('https://www.gstatic.com/marketing-cms/assets/images/d5/dc/cfe9ce8b4425b410b49b7f2dd3f3/g.webp=s96-fcrop64=1,00000000ffffffff-rw');
        background-repeat: no-repeat;
        background-position: 15px center; /* Pozice: 15px zleva, uprostřed výšky */
        background-size: 24px;
    }
    
    .st-key-seznam button {
        background-color: white !important;
        color: #31333F !important;
        border: 1px solid #d3d3d3 !important; 
            
        background-image: url('https://www.seznam.cz/favicon.ico');
        background-repeat: no-repeat;
        background-position: 15px center; /* Pozice: 15px zleva, uprostřed výšky */
        background-size: 24px;
    }
            
    .st-key-google button:hover, .st-key-seznam button:hover {
        background-color: #f0f2f6 !important;
        border-color: #ff4b4b !important;
    }
</style>
""", unsafe_allow_html=True)

st.session_state.page = Path(__file__).name.replace('.py', '')
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")


if "option" not in st.session_state:
    st.session_state.option = None

if "userID" not in st.session_state:
    st.session_state['userID'] = None

if "username" not in st.session_state:
    st.session_state['username'] = None
    
if "seznam_token" not in st.session_state:
    st.session_state["seznam_token"] = None    

SEZNAM_CONFIG = st.secrets["auth"]["seznam"]
# ======= Styles =======
styles.apply()

# ======= Authentication Logic =======
def login_google():
    if st.button("Přihlásit přes Google", key="google"):
        st.login("google")
        
def login_seznam():  
    # 2. Build the URL (Same logic as before)
    params = {
        "client_id": SEZNAM_CONFIG["client_id"],
        "scope": SEZNAM_CONFIG["scope"],
        "response_type": "code",
        "redirect_uri": SEZNAM_CONFIG["redirect_uri"],
        "state": "seznam_manual_flow" 
    }
    auth_url = f"{SEZNAM_CONFIG['authorize_url']}?{urllib.parse.urlencode(params)}"

    # 3. THE TRICK: Use JavaScript to navigate in the CURRENT tab
    # This prevents opening a new tab and solves your UX issue.
    if st.button("Přihlásit přes Seznam", key="seznam"):
        redirect(auth_url)

def process_google_token():
    user_data = st.user
    if user_data["is_logged_in"] == False:
        pass
    elif user_data["is_logged_in"] == True:
        st.session_state['userID'] = user_data["sub"]
        st.session_state['username'] = user_data["name"]
        st.switch_page("pages/app.py")

def process_seznam_token():
    """Exchanges the code for a token manually."""
    query_params = st.query_params
    code = query_params.get("code")
    state = query_params.get("state")

    # Only process if we see a code AND it matches our Seznam state
    if code and state == "seznam_manual_flow":
        try:
            # THIS IS THE KEY FIX: Sending secrets in the 'data' (Body), not headers
            token_data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": SEZNAM_CONFIG["redirect_uri"],
                "client_id": SEZNAM_CONFIG["client_id"],
                "client_secret": SEZNAM_CONFIG["client_secret"] 
            }
            
            # Manual POST request
            response = requests.post(SEZNAM_CONFIG["token_url"], data=token_data)
            response.raise_for_status() # This will catch the 400 error if it persists
            
            # If successful, parse token
            tokens = response.json()
            st.session_state["seznam_token"] = tokens
            
            # Clear URL params to clean up
            st.query_params.clear()
            #st.rerun()
            
        except requests.exceptions.HTTPError as e:
            st.error(f"Seznam Token Error: {e}")
            st.write(response.text) # Print exact error from Seznam for debugging
            
    if "seznam_token" in st.session_state:
        try:
            st.session_state["userID"] = st.session_state["seznam_token"].get("oauth_user_id")
            print("Getting Seznam user info...")
        except:
            return
        
        print("Success, redirecting")
        name, data = get_seznam_username(st.session_state["seznam_token"]["access_token"])
        st.session_state["username"] = name
        st.session_state["userID"] = data["oauth_user_id"]
        st.switch_page("pages/app.py")


def get_seznam_username(access_token):
    user_info_url = "https://login.szn.cz/api/v1/user"

    # 2. Set the headers with your new Access Token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # 3. Make the request
    response = requests.get(user_info_url, headers=headers)
    data = response.json()

    # 4. Extract the name safely
    # Seznam usually provides 'account_name' (display name), but sometimes only 'username'.
    # We try 'account_name' first, then fall back to 'username'.
    full_name = data.get("firstname") + " " + data.get("lastname") or data.get("account_name")
    print(data)
    return full_name, data


if len(st.query_params) > 0:
    process_seznam_token()

process_google_token()

st.title("Vítejte v ArcheoNetu!")
login_google()
login_seznam()

if st.button("Legacy login"):
    st.switch_page("pages/intercept_legacy_login.py")

# Logo at: https://drive.google.com/thumbnail?id=1GAt9nJyJ5kiRtvl0KGIPDqALTaGOaMGE&sz=w1000

# streamlit run login.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
