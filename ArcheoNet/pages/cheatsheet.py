import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import pandas as pd
import numpy as np
from datetime import datetime
import time

# ===== SCRIPTS =====

# ===== BASIC PAGE SETUP =====
st.set_page_config(
    page_title="Streamlit Cheat Sheet",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("📚 Streamlit Feature Showcase")
st.caption("A comprehensive demo of Streamlit's core functionality")

# ===== SESSION STATE & CACHE =====
st.header("1. State Management")

# Session state (persists between reruns)
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# Cache decorator for expensive functions
@st.cache_data
def expensive_computation(n):
    st.write("⚠️ Calculating (only runs once!)")
    return n * n

# ===== BASIC WIDGETS =====
st.header("2. Basic Widgets")

with st.expander("Click to show widgets"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Buttons
        if st.button("Increment Counter"):
            st.session_state.counter += 1
        
        # Checkbox
        checked = st.checkbox("Show secret message", True)
        if checked:
            st.write("🔒 You found the secret!")
    
    with col2:
        # Radio buttons
        color = st.radio(
            "Pick a color",
            ["Red", "Green", "Blue"],
            index=1
        )
        
        # Select slider
        size = st.select_slider(
            "Select size",
            options=["S", "M", "L", "XL"]
        )
    
    with col3:
        # Slider
        temp = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=100.0,
            value=25.0,
            step=0.5
        )
        
        # Number input
        quantity = st.number_input(
            "How many?",
            min_value=1,
            max_value=10,
            value=3
        )

# ===== TEXT & DISPLAY =====
st.header("3. Text & Display")

st.write(f"Current counter: {st.session_state.counter}")
st.metric("Temperature", f"{temp}°C", "1.2°C")  # Delta shows change

# Markdown with emojis
st.markdown("""
### 📝 Markdown Support
- **Bold** and *italic* text
- `Code` snippets
- [Links](https://streamlit.io)
""")

# JSON display
st.json({
    "name": "Streamlit",
    "type": "Library",
    "awesome": True
})

# ===== DATA DISPLAY =====
st.header("4. Data Display")

# Sample dataframe
df = pd.DataFrame({
    "Date": pd.date_range("2023-01-01", periods=5),
    "Sales": np.random.randint(100, 1000, 5),
    "Region": ["North", "South", "East", "West", "Central"]
})

# Show dataframe with options
st.dataframe(df.style.highlight_max(axis=0))

# Interactive table
st.data_editor(df, num_rows="dynamic")

# Chart
st.line_chart(df.set_index("Date"))

# ===== LAYOUTS =====
st.header("5. Layouts")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Chart", "🗃 Data", "📝 Notes"])

with tab1:
    st.area_chart(df.set_index("Date"))

with tab2:
    st.table(df.sample(3))

with tab3:
    st.text_area("Enter your notes here")

# Columns
col1, col2 = st.columns([3, 1])

with col1:
    st.write("Wider column (3/4 width)")

with col2:
    st.write("Narrow column (1/4 width)")

# Expander
with st.expander("Click to show more"):
    st.write("Hidden content that appears when expanded")

# ===== MEDIA =====
st.header("6. Media")

# Images
st.image("https://streamlit.io/images/brand/streamlit-mark-color.png",
        width=100)

# Audio
st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

# Video
st.video("https://www.youtube.com/watch?v=jq0lKF9WPmc")

# ===== FORMS =====
st.header("7. Forms")

with st.form("user_info"):
    name = st.text_input("Your name")
    age = st.slider("Your age", 1, 100)
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.success(f"Hello {name}, age {age}!")

# ===== PROGRESS & STATUS =====
st.header("8. Status Indicators")

if st.button("Show progress"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        progress_bar.progress(i + 1)
        status_text.text(f"Progress: {i+1}%")
        time.sleep(0.02)
    
    st.balloons()  # Celebration!

# ===== SIDEBAR =====
with st.sidebar:
    st.header("Sidebar Controls")
    user_input = st.text_input("What's your name?")
    st.write(f"Hello, {user_input or 'stranger'}!")
    
    if st.button("Magic"):
        st.snow()  # Snow effect!

# ===== FOOTER =====
st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

df = pd.DataFrame({
    'latitude': [37.7749551, 34.0522, 40.7128],
    'longitude': [-122.41941465, -118.2437, -74.0060]
})
st.map(df)


# ===== REQUEST USER LOCATION =====
st.title("Request User Location in Streamlit - Old")

#time.sleep(2)

location = streamlit_geolocation()
print(location)

if location["longitude"] != None and location["latitude"] != None:
    latitude = location["latitude"]
    longitude = location["longitude"]
    st.write(f"Longitude: {location["longitude"]}, Latitude: {location["latitude"]}")

    current_pos = pd.DataFrame({
        'latitude': [latitude],
        'longitude': [longitude],
    })

else:
    current_pos = pd.DataFrame({
        'latitude': [0.0],
        'longitude': [0.0],
    })

st.map(current_pos, color="#008000", size=10)

# ===== User location =====
st.title("Request User Location in Streamlit - New")

if st.checkbox("Check my location"):
    loc = get_geolocation()
    print(loc)
    st.write(f"Your coordinates are {loc}")

st.title("Request User Location in Streamlit - Custom Component")

getgeolocation = """
new Promise((resolve, reject) => {
  navigator.geolocation.getCurrentPosition(
    pos => resolve({
      latitude: pos.coords.latitude,
      longitude: pos.coords.longitude,
      accuracy: pos.coords.accuracy,
      error: null
    }),
    err => resolve({
      latitude: null,
      longitude: null,
      accuracy: null,
      error: err.message
    })
  );
});
"""

loc = streamlit_js_eval(js_expressions=getgeolocation, key="getgeolocation")
st.write(loc)
st.write(f"Latitude: {loc["latitude"]}")
st.write(f"Longitude: {loc["longitude"]}")