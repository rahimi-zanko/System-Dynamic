import streamlit as st
import base64
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from numerize import numerize
import plotly.graph_objects as go
import hashlib

# Set up authentication
your_username = "Zanko"
your_password = "Zanko_2024"

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Set up page configuration
st.set_page_config(
    page_title="Agriculture Analytic Platform",
    layout="wide",
    page_icon="favicon.png",
    initial_sidebar_state="collapsed" if not st.session_state.authenticated else "expanded"
)

# Headers and Logo
col1, col2, col3, col4, col5 = st.columns((1,1,2,1,1))
with col3:
    st.image("NEW_AAP LOGO-1.png")
st.markdown("<h3 style='text-align: center; color: green;'> System Dynamics Application </h>", unsafe_allow_html=True)

# Sidebar content
if st.session_state.authenticated:
    st.sidebar.header("About")
    st.sidebar.markdown("[Agriculture Analytics Platform](https://infocenter.com.my/aap/commodity.html) is an analytical platform that provides the analytics, databanks, and data repository of agriculture to the user.")
    st.sidebar.header("Resources")
    st.sidebar.markdown("[System Dynamics Model of Industrial Crops](https://www.krinstitute.org/assets/contentMS/img/template/editor/0.Full%20report%20200410.pdf) published in 2021 by Khazanah Research Institute (KRI). ")
else:
    st.sidebar.empty()

# Login section
if not st.session_state.authenticated:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_after = st.button("Login")

    if login_after:
        # Add your authentication logic here
        if username == your_username and password == your_password:
            st.session_state.authenticated = True
            st.success("Login successful!")
            st.experimental_rerun()  # Refresh the page to update sidebar state
        else:
            st.error("Login failed. Please check your credentials.")
else:
    st.write("You are authenticated.")
    # Add the rest of your content here

# Hide sidebar control button when authenticated
hide_bar = """
           <style>
           [data-testid='collapsedControl'] {visibility:hidden;}
           </style>
           """
if st.session_state.authenticated:
    st.markdown(hide_bar, unsafe_allow_html=True)
