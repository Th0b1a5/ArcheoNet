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

# =======INITALIZE SESSION STATE VARIABLES AND OTHER =======
styles.apply()
	
st.title("Google Login")



if st.button("Logout"):
    st.logout()

st.json(st.experimental_user)