import streamlit as st
import folium
from streamlit_folium import st_folium
import pydeck as pdk
import pandas as pd

# Make wide layout
st.set_page_config(layout="wide")

# Remove margins and make container full screen via CSS
st.markdown(
    """
    <style>
    /* Remove all padding and margin from main container and page */
    .css-18e3th9, .css-1d391kg, .block-container, .main {
        overflow: hidden !important;
        height: 100vh !important;
        width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    /* Remove Streamlit default header space */
    header, .css-1vencpc {
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        display: none !important;  /* hides the top header bar */
    }
    /* Also remove the default footer if you want */
    footer {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

data = pd.DataFrame({
    'lat': [37.7749, 40.7128],
    'lon': [-122.4194, -74.006],
    'name': ['San Francisco', 'New York']
})

# Define layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position='[lon, lat]',
    get_color='[200, 30, 0, 160]',
    get_radius=10000,
    pickable=True,
)

# Define view
view_state = pdk.ViewState(
    latitude=37.7749,
    longitude=-122.4194,
    zoom=4,
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{name}"},
)

selected = st.pydeck_chart(r, height=1000)

# You can extend to detect clicks and display info below using Streamlit widgets and state
