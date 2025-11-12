import streamlit as st
import pydeck as pdk
import pandas as pd

# Example data: list of places with lat, lon, and info
data = [
    {"name": "Place A", "lat": 40.7128, "lon": -74.0060, "info": "Info about Place A"},
    {"name": "Place B", "lat": 34.0522, "lon": -118.2437, "info": "Info about Place B"},
    {"name": "Place C", "lat": 37.7749, "lon": -122.4194, "info": "Info about Place C"},
]

df = pd.DataFrame(data)

# Define a layer to show scatterplot (markers)
layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    get_position='[lon, lat]',
    get_fill_color='[200, 30, 0, 160]',
    get_radius=30000,
    pickable=True,  # Enable picking (click detection)
)

# Set the view state (center and zoom)
view_state = pdk.ViewState(
    latitude=df['lat'].mean(),
    longitude=df['lon'].mean(),
    zoom=4,
    pitch=0,
)

# Create the deck.gl map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{name}\n{info}"},
)

# Render the map in Streamlit
selected = st.pydeck_chart(r)

# selected contains info about clicked object (if any)
if selected is not None and "picked_object" in selected:
    picked = selected["picked_object"]
    if picked is not None:
        st.write(f"You clicked on {picked['name']}")
        st.write(picked['info'])
