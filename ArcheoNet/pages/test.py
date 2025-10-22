import streamlit as st
import streamlit.components.v1 as components

# Initialize toggle state
if "show_map_overlay" not in st.session_state:
    st.session_state.show_map_overlay = False

def toggle_overlay():
    st.session_state.show_map_overlay = not st.session_state.show_map_overlay

# Toggle button
st.button("Toggle Fullscreen Map Overlay", on_click=toggle_overlay)

# CSS to hide Streamlit UI and to style overlay full screen
css = """
<style>
/* Hide Streamlit padding, header, footer */
.css-1d391kg, .css-10trblm, .css-18e3th9 {
    padding: 0 !important;
    margin: 0 !important;
}
header, footer {
    display: none !important;
}
body, html {
    overflow: hidden;
    height: 100%;
}

/* Overlay container, hidden by default via translateY */
#map-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    z-index: 9999;
    background: white;
    transition: transform 0.4s ease-in-out;
    transform: translateY(100%);
}
/* Show overlay by resetting translate */
#map-overlay.show {
    transform: translateY(0);
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# Leaflet map HTML+JS inside overlay div container toggled visible via class
leaflet_html = f"""
<div id="map-overlay" class="{ 'show' if st.session_state.show_map_overlay else '' }">
  <div id="map" style="width:100vw; height:100vh;"></div>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"/>
  <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
  <script>
    var map = L.map('map').setView([37.8, -96], 4);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 19,
      attribution: '© OpenStreetMap'
    }}).addTo(map);
  </script>
</div>
"""

# Render the overlay component (height and width large enough to fill viewport)
components.html(leaflet_html, height=900, width=1600)
