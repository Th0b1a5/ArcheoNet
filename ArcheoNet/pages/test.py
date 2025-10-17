import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime
import sqlite3
import time
from streamlit_folium import st_folium
import folium
import plotly.express as px
import pandas as pd


st.title("HTML Camera input Test")


import streamlit as st

st.markdown("""
<style>
[data-testid="stFileUploader"] button {
    padding: 0.4em 2em;
    border-radius: 0.5em;
    background-color: #0099ff;
    color: white;
    font-weight: 600;
    border: none;
    cursor: pointer;
    width: 100%;
    height: 50px;
}
</style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Select image or camera photo")

if uploaded_file is not None:
    st.image(uploaded_file)
    
    


m = folium.Map(location=[49.8, 18.2], zoom_start=10, tiles='CartoDB positron')
folium.Marker([49.9, 18.3], popup='Example Location').add_to(m)
st_folium(m)

df = pd.DataFrame({
    'lat': [49.8, 49.9],
    'lon': [18.2, 18.3]
})

fig = px.scatter_map(df, lat="lat", lon="lon", zoom=10, mapbox_style="carto-positron")
st.plotly_chart(fig)