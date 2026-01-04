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

conn = sqlite3.connect(r"database\users.db")
cursor = conn.cursor()
try:
    cursor.execute("""CREATE TABLE users    (
                    username TEXT PRIMARY KEY,
                    password TEXT
        )""")
    conn.commit()
except sqlite3.OperationalError:
    print("Table already exists")

allowed_char = r"a-zA-Z0-9\-_.#@ěščřžýáíéúůťňďóĚŠČŘŽÝÁÍÉÚŮŤŇĎÓ"
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

def verify_google():
    user_data = st.experimental_user
    if user_data["is_logged_in"] == False:
        pass
    elif user_data["is_logged_in"] == True:
        st.session_state['userID'] = user_data["sub"]
        st.session_state['username'] = user_data["name"]
        st.switch_page("pages/app.py")

verify_google()

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

if st.button("Log in with google"):
    st.login("google")

verify_google()
# Keep in ming we might migrate to postgres if we win the FLL championships, so dont go crazy with SQLite

# streamlit run login.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
