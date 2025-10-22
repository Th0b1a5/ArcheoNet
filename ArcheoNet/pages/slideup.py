import streamlit as st

# ======= Setup and scripts =======
st.set_page_config(
	page_title="ArcheoNet DEV VERSION (alpaha)",
	page_icon="📚",
	layout="wide",
	initial_sidebar_state="collapsed"
)


try:
	username = (st.session_state['userID'])
except:
	st.switch_page("login.py")
if st.session_state["userID"] == None or st.session_state["userID"] == "":
	st.switch_page("login.py")
	
# Initialize session state for toggle
if "slide_up_visible" not in st.session_state:
    st.session_state.slide_up_visible = False

def toggle_slide_up():
    st.session_state.slide_up_visible = not st.session_state.slide_up_visible

# Button to toggle sliding div
st.button("Toggle Slide Up Window", on_click=toggle_slide_up)

# CSS styles for sliding div
slide_up_css = """
<style>
#slide-up-window {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 70vh;
  background-color: var(--primary-color);
  border-top: 3px solid #666;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
  overflow: auto;
  transition: transform 0.4s ease-in-out;
  transform: translateY(100%);
  z-index: 9999;
  padding: 20px;
}
#slide-up-window.open {
  transform: translateY(0);
}
button.inner-btn {
  margin: 5px;
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
}
button.inner-btn:hover {
  background-color: #0056b3;
  cursor: pointer;
}
</style>
"""

# Embed the CSS
st.markdown(slide_up_css, unsafe_allow_html=True)

# HTML div for sliding window
slide_up_html = f"""
<div id="slide-up-window" class="{ 'open' if st.session_state.slide_up_visible else '' }">
  <h3>This is the sliding window content</h3>
  <p>You can put any normal text or other Streamlit elements here.</p>
  <button class="inner-btn" onclick="alert('Button 1 clicked!')">Button 1</button>
  <button class="inner-btn" onclick="alert('Button 2 clicked!')">Button 2</button>
</div>
"""
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

st.markdown("""
<style>
div.stButton > button {
    width: 87vw;
    margin: 100px auto;
    display: block;
    font-size: 1.2em;
    padding: 1em 0.5em;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
        div.block-container {
            padding-top: 0rem;      /* Adjust to taste */
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(slide_up_html, unsafe_allow_html=True)
