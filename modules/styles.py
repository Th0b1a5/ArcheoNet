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
		.block-container {
			padding-top: 2rem !important;
			padding-bottom: 0rem !important;
			margin-top: -5rem !important; /* Volitelné: agresivnější posun nahoru */
		}

		/* Skryje prázdný prostor pro header lištu */
		header {
			visibility: hidden;
			height: 0px;
		}

	</style>
	""",
	unsafe_allow_html=True)
