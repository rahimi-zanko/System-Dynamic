import streamlit as st
#from streamlit_chat import message
import base64
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from numerize import numerize
import plotly.graph_objects as go
#import streamlit_authenticator as stauth
import hashlib

#set up authentication
#stauth.authenticate()
your_username = "Zanko"
your_password = "Zanko_2024"

# set sidebar collapsed before login
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'

# hide collapsed control button
hide_bar = """
           <style>
           [data-testid='collapsedControl"] {visibility:hidden;}
           </style>
           """

#set up page configuration
st.set_page_config(
    page_title="Agriculture Analytic Platform",
    layout="wide",
    page_icon="favicon.png",
    initial_sidebar_state=st.session_state.sidebar_state   
)

# Headers and Logo
col1, col2, col3, col4, col5 = st.columns((1,1,2,1,1))
with col3:
    st.image("NEW_AAP LOGO-1.png")
st.markdown("<h3 style='text-align: center; color: green;'> System Dynamics Application </h>", unsafe_allow_html= True)

#sidebar
#st.sidebar.success("Select a page above.")
st.sidebar.header("About")
st.sidebar.markdown("[Agriculture Analytics Platform](https://infocenter.com.my/aap/commodity.html) is an analytical platform that provides the analytics, databanks and data repository of agriculutre to the user.")
st.sidebar.header("Resources")
st.sidebar.markdown("[System Dynamics Model of Industrial Crops](https://www.krinstitute.org/assets/contentMS/img/template/editor/0.Full%20report%20200410.pdf) published in 2021 by Khazanah Research Institute (KRI). ")
#if st.sidebar.button('System Dynamic Model- Paddy & Rice Sector'): 
#displayPDF("C:/Users/user/Desktop/Python Project/Streamlit/0.Full report 200410.pdf")

#login section
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_after = st.button("Login")

if login_after:
    #Add your authentication logic here
    if username == your_username and password == your_password:
        st.success("Login successful!")
        st.session_state.sidebar_state = "expanded"
    else:
        st.error("Login failed. Please check your credentials.")

#content
#if username == your_username and password == your_password:
    #st.write("You are authenticated.")
    #Add the rest of your content here.
else:
    st.warning("Please log in to access the content")
    st.session_state.sidebar_state = "collapsed"

# set sidebar expanded after login
if login_after:
    st.session_state.sidebar_state = 'expanded'
else:
    st.session_state.sidebar_state = 'collapsed'
    st.markdown(hide_bar, unsafe_allow_html=True)

#st.image("Picture2.png")