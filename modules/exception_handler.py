

def handler(exception):
    import streamlit as st
    st.warning("An error has occurred 😵. If this issue persists, please contact the ArcheoNet team via our email.")
    print(f"Exception: {exception}")