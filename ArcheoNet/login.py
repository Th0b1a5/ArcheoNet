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



# ===== SCRIPTS =====
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
try:
    cursor.execute("""CREATE TABLE users    (
                    email TEXT PRIMARY KEY,
                    password TEXT
        )""")
    conn.commit()
except sqlite3.OperationalError:
    print("Table already exists")

def register_user(email, password):
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return "User already exists"
    except sqlite3.DatabaseError:
        return "Database error, please refresh this page"


def verify_user(email, password):

    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    result = cursor.fetchone()
    print(result)
    if result:
        conn.close()
        return True
    else:
        return "User not found or password incorrect"

if "option" not in st.session_state:
    st.session_state.option = None

st.markdown("""
<style>
div.stButton > button {
    width: 90vw;
    max-width: 400px;
    margin: 10px auto;
    display: block;
    font-size: 1.2em;
    padding: 1em 0.5em;
}
</style>
""", unsafe_allow_html=True)

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
# ===== BASIC PAGE SETUP =====
st.set_page_config(
    page_title="ArcheoNet DEV VERSION (alpaha) Login",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======= Title =======
st.title("ArcheoNet DEV DEMO VERSION Login")

# ======= Login =======
def login_page():
    st.caption("Login")

    with st.form(key="login"):
        email = st.text_input("E-mail")

        password = st.text_input("Password", type="password")

        if st.form_submit_button():
            result = verify_user(email, password)
            st.write(result)


def register_page():
    st.caption("Register")

    with st.form(key="register"):
        reg_email = st.text_input("Enter e-mail")

        reg_password = st.text_input("Enter password", type="password")

        if st.form_submit_button():
            result = register_user(reg_email, reg_password)
            st.write(result)


if st.session_state.option == "Register":
    register_page()
elif st.session_state.option == "Login":
    login_page()
else:
    st.caption("Please chose one of the options below:")


# Vertical, centered buttons
if st.button("Login"):
    st.session_state.option = "Login"
    st.rerun()

if st.button("Register"):
    st.session_state.option = "Register"
    st.rerun()

# streamlit run login.py --server.sslCertFile=cert.pem --server.sslKeyFile=key.pem