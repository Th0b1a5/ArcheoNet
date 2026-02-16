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
import psycopg2
from psycopg2.extras import RealDictCursor

import modules.get_ip as get_ip
import modules.location as location
import modules.styles as styles


if 'length' not in st.session_state:
    st.session_state.length = 1
    print("created")

if st.session_state.page != "latest_posts":
	st.session_state.length = 1
	print("updated")

st.session_state.page = Path(__file__).name.replace('.py', '')
print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - {st.session_state.page}")

try:
	userID = (st.session_state['userID'])
	username = (st.session_state['username'])
except:
	st.switch_page(r"login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")
 
st.set_page_config(
    page_title="ArcheoNet DEV VERSION (alpaha) Login",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

styles.apply()

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

def get_latest_by_number(pos):
    pos -= 1
    try:
        conn = psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            port=st.secrets["postgres"]["port"],
            dbname=st.secrets["postgres"]["dbname"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"],
            sslmode="require"
        )

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        print("Connection to DB successful!")
        
    except psycopg2.DatabaseError:
        print("Chyba připojení k databázi, zkuste to prosím později nebo kontaktujte ArcheoNet team.")
        st.stop()
		
    try:
        cursor.execute("SELECT name, owner, type, position id FROM map_posts ORDER BY position ASC LIMIT 1 OFFSET %s", (pos,))
        posts = cursor.fetchone()
            
        cursor.close()
        conn.close()
        
        return posts
    
    except psycopg2.DatabaseError:
        cursor.close()
        conn.close()
        print("Chyba databáze, zkuste to prosím později nebo kontaktujte ArcheoNet team.")
        st.stop()

if st.button("Další", key="btn1"):
	st.session_state.length = st.session_state.length + 1

if st.button("Předchozí", key="btn2"):
	st.session_state.length = st.session_state.length - 1

st.write(st.session_state.length)

post = get_latest_by_number(st.session_state.length)

if post == None:
    st.write("No more posts :(")
else:
    st.write(post)
    