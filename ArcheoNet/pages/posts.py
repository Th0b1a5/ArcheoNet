import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link
import pandas as pd
import numpy as np
from streamlit.runtime import get_instance
from datetime import datetime
import pydeck as pdk
import sqlite3
from io import BytesIO
from PIL import Image, ImageOps


import modules.get_ip as get_ip
import modules.location as location
import modules.styles as styles


print(f"Device connected! {datetime.now():%Y-%m-%d %H:%M:%S} - IP: {get_ip.pull_ip()} - Login")

st.map()