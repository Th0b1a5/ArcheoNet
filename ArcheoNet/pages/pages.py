import streamlit as st

import modules.get_ip as get_ip
import modules.location as location
import modules.styles as styles

# ===== SETUP =====
st.set_page_config(
    page_title="ArcheoNet DEV VERSION (alpaha) Login",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

styles.apply()

if st.button("Make a post"):
	st.switch_page("pages/map_post.py")
	
if st.button("Browse posts"):
	st.switch_page("pages/posts.py")

if st.button("Map"):
	st.switch_page("pages/map.py")
	
if st.button("Testpage"):
	st.switch_page("pages/test.py")
	
if st.button("Test 2"):
	st.switch_page("pages/test2.py")
	
if st.button("Slideup"):
	st.switch_page("pages/slideup.py")

if st.button("Back"):
	st.switch_page("pages/app.py")

if st.button("fetchdb"):
	st.switch_page("pages/fetchdb.py")
 
if st.button("Map tests"):
	st.switch_page("pages/map_tests.py")