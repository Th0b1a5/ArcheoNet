import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import pandas as pd
import numpy as np
from streamlit.runtime import get_instance
from datetime import datetime
import pydeck as pdk
import sqlite3
import time
import socket
import re





# ===== SETUP =====
st.set_page_config(
    page_title="ArcheoNet DEV VERSION (alpaha) Login",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "option" not in st.session_state:
    st.session_state.option = None

if "userID" not in st.session_state:
    st.session_state['userID'] = None

conn = sqlite3.connect("users.db")
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



# ======= Title =======
st.title("ArcheoNet DEV DEMO VERSION Login")


# ======= Login =======
def login_page():
    st.caption("Login")

    with st.form(key="login"):
        username = st.text_input("Username")

        password = st.text_input("Password", type="password")

        if st.form_submit_button():
            result = verify_user(username, password)

            if result == True:
                st.session_state['userID'] = username
                st.success(result)
                st.switch_page("pages/app.py")

            else:
                st.error(result)

def register_page():
    st.caption("Register")

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


if st.session_state.option == "Register":
    register_page()

elif st.session_state.option == "Login":
    login_page()

else:
    st.caption("Please chose one of the options below:")



if st.session_state.option == "Register":
    if st.button("Login"):
        st.session_state.option = "Login"
        st.rerun()

elif st.session_state.option == "Login":
    if st.button("Register"):
        st.session_state.option = "Register"
        st.rerun()

else:
    if st.button("Login"):
        st.session_state.option = "Login"
        st.rerun()

    if st.button("Register"):
        st.session_state.option = "Register"
        st.rerun()


# streamlit run login.py --server.sslCertFile=keys/cert.pem --server.sslKeyFile=keys/key.pem
