import streamlit as st

def apply():
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
            width: 90vw;
            margin: 5px auto;
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
                            padding-top: 8px;      /* Adjust to taste */
                            padding-bottom: 0rem;
                            padding-left: 1rem;
                            padding-right: 1rem;
                    }
            </style>
            """,
            unsafe_allow_html=True
    )
