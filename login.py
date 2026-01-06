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

import modules.get_ip as get_ip
import modules.location as location
import modules.styles as styles

# ===== SETUP =====
st.set_page_config(
    page_title="ArcheoNet DEV VERSION (alpaha) Login",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.session_state.page = Path(__file__).name.replace('.py', '')
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")


if "option" not in st.session_state:
    st.session_state.option = None

if "userID" not in st.session_state:
    st.session_state['userID'] = None

if "username" not in st.session_state:
    st.session_state['username'] = None

SEZNAM_CONFIG = st.secrets["auth"]["seznam"]


conn = sqlite3.connect(r"database/users.db")
cursor = conn.cursor()
try:
    cursor.execute("""CREATE TABLE users    (
                    username TEXT PRIMARY KEY,
                    password TEXT
        )""")
    conn.commit()
except sqlite3.OperationalError:
    print("Table already exists")

allowed_char = r"a-zA-Z0-9/-_.#@ěščřžýáíéúůťňďóĚŠČŘŽÝÁÍÉÚŮŤŇĎÓ"
pattern_char = rf"^[{allowed_char}]+$"

# ======= Styles =======
styles.apply()

# ======= Functions =======
def register_user(username, password):
    if username == None or password == None or username == "" or password == "":
        return "Please insert a value"
    
    elif not re.match(pattern_char, username):
        return f"Username contains unwanted characters. Allowed characters: {allowed_char}"

    else:
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
        
        except sqlite3.IntegrityError:
            return "User already exists"
        
        except sqlite3.DatabaseError:
            return "Database error, please refresh this page"

def verify_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    print(result)

    if result:
        conn.close()
        return True
    else:
        return "User not found or password incorrect"


# ======= Title =======
#st.title("ArcheoNet DEV DEMO VERSION Login")

# ======= Login =======
def login_page():
    st.title("Login")

    with st.form(key="login"):
        username = st.text_input("Username")

        password = st.text_input("Password", type="password")

        if st.form_submit_button():
            result = verify_user(username, password)

            if result == True:
                st.session_state["userID"] = username
                st.session_state["username"] = username
                st.success(result)
                st.switch_page("pages/app.py")

            else:
                st.error(result)

def register_page():
    st.title("Register")

    with st.form(key="register"):
        reg_username = st.text_input("Enter username")

        reg_password = st.text_input("Enter password", type="password")

        if st.form_submit_button():
            result = register_user(reg_username, reg_password)
            
            if result == True:
                st.session_state.option = "Login"
                st.rerun()
            else:
                st.error(result)
  
def login_google():
    if st.button("Log in with google"):
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
    if st.button("Login with Seznam"):
        redirect(auth_url)

def process_google_token():
    user_data = st.experimental_user
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
            st.rerun()
            
        except requests.exceptions.HTTPError as e:
            st.error(f"Seznam Token Error: {e}")
            st.write(response.text) # Print exact error from Seznam for debugging
            
    if "seznam_token" in st.session_state:
        st.session_state["userID"] = st.session_state["seznam_token"].get("oauth_user_id")
        name, data = get_seznam_username(st.session_state["seznam_token"]["access_token"])
        st.session_state["username"] = name
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
    
    return full_name, data

process_google_token()
process_seznam_token()

if st.session_state.option == "Register":
    register_page()
    if st.button("Login"):
        st.session_state.option = "Login"
        st.rerun()

elif st.session_state.option == "Login":
    login_page()
    if st.button("Register"):
        st.session_state.option = "Register"
        st.rerun()

else:
    st.title("ArcheoNet")
    st.caption("Please chose one of the options below:")
    if st.button("Login"):
        st.session_state.option = "Login"
        st.rerun()

    if st.button("Register"):
        st.session_state.option = "Register"
        st.rerun()

login_google()
login_seznam()
# Keep in ming we might migrate to postgres if we win the FLL championships, so dont go crazy with SQLite

# streamlit run login.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
