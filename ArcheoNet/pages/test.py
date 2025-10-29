import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import pydeck as pdk

# Get viewport height asynchronously
height = streamlit_js_eval(js_expressions='window.innerHeight', key='height', want_output=True)

if height is None:
    st.write("Loading map size...")
else:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=[{"position": [-122.4194, 37.7749]}],
        get_position="position",
        get_color=[255, 0, 0],
        get_radius=10000,
    )
    view_state = pdk.ViewState(longitude=-122.4194, latitude=37.7749, zoom=10)

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/streets-v11",
    )

    st.pydeck_chart(r, height=int(height))

# Minimal CSS to keep page scroll enabled
st.markdown(
    """
    <style>
        body, html, #root, .block-container {
            overflow-y: auto !important;
            height: auto !important;
            margin: 0;
            padding: 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)
