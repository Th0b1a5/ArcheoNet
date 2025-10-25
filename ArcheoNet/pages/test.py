import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
  <style>
    html, body, #map {{
      margin: 0;
      padding: 0;
      height: 100vh;
      width: 100vw;
    }}
  </style>
  <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
</head>
<body>
  <div id="map"></div>
  <script>
    var map = L.map('map').setView([37.7749, -122.4194], 11);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 19,
    }}).addTo(map);
  </script>
</body>
</html>
"""

html(html_code, height=800, width=1200)  # Adjust width/height - try big values or window-resize trick
