# import libraries
import streamlit as st
import base64
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from numerize import numerize
import plotly.graph_objects as go 

#set up page configuration
st.set_page_config(
    page_title="Agriculture Analytic Platform",
    layout="wide",
    page_icon="favicon.png",
    initial_sidebar_state=st.session_state.sidebar_state   
)

# Resource (report)
def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

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

#parameter
col1, col2, col3, col4 = st.columns(4)
with col1:
    i_currentPopulation = st.number_input("Please enter the no. of current population:", key="1")
with col2:
    i_growthRate = st.number_input("Slide to select the P net growth fraction:", format= "%.3f", key="2")             
with col3:
    i_startyear = st.number_input("Please enter the starting year:", value=2000, key="3")
    i_endyear = st.number_input("Please enter the ending year:",value=2010, key="4")
with col4:
    i_perCapitaConsumption = st.number_input("Please enter per capita consumption: (kg)", value=100, key="5")

def populationGrowth(i_currentPopulation, i_growthRate, years):
    v_populations = [i_currentPopulation]
    for year in range(years):
        v_populations.append(v_populations[-1] * (1 + i_growthRate))
    return v_populations[-1] - v_populations[0], v_populations[-1]

def consumptionYear(i_perCapitaConsumption, years):
    v_consumption = [i_perCapitaConsumption]
    for year in range(years):
        v_consumption.append(v_consumption[-1] * (1+0.02))
    return v_consumption [-1]

years = int(i_endyear - i_startyear)
pG, tP = populationGrowth(i_currentPopulation, i_growthRate, years)

col1, col2 = st.columns(2)
with col1:
    #st.markdown("<h4 style='text-align:left;'> Population net growth rate calculation </h4>", unsafe_allow_html=True)
    #st.markdown("<h6 style='text-align:left;'> P net growth rate = P net growth fraction x Total Population </h6>", unsafe_allow_html=True)
    #st.write(f"Population Growth: {pG:.4f}")
    pG_numerized = numerize.numerize(pG)
    #st.markdown(f"<h6 style='text-align: center;'>Population Growth: {pG_numerized}</h6>", unsafe_allow_html=True)

with col2:
    #st.markdown("<h4 style='text-align:left;'> Total population calculation </h4>", unsafe_allow_html=True)
    #st.markdown("<h6 style='text-align:left;'> Total population = INTEG (P net growth rate, Population^(no of years-1)) </h6>", unsafe_allow_html=True)
    #st.write(f"Total Population: {tP:.4f}")
    tP_numerized = numerize.numerize(tP)
    #st.markdown(f"<h6 style='text-align: center;'>Total Population: {tP_numerized}</h6>", unsafe_allow_html=True)

#st.markdown("<h4 style='text-align:center;'> Rice requirement calculation </h4>", unsafe_allow_html=True)
#st.markdown("<h6 style='text-align:center;'> Rice requirement = Per capita consumption x Total population </h6>", unsafe_allow_html=True)

def riceRequirement(totalPopulation, perCapitaConsumption):
    return totalPopulation * perCapitaConsumption

def compute_rice_requirements_over_years_vary_growth(currentPopulation, initial_growth_rate, perCapitaConsumption, i_startyear, i_endyear):
    i_startyear = int(i_startyear)
    i_endyear = int(i_endyear)
    years_range = list(range(int(i_startyear), int(i_endyear) + 1))
    rice_requirements = []
    growth_rate = initial_growth_rate

    for year in years_range:
        growth, total_pop = populationGrowth(currentPopulation, growth_rate, year - i_startyear)
        per_consumption = consumptionYear(perCapitaConsumption, year - i_startyear)
        rice_requirements.append(riceRequirement(total_pop, per_consumption))
        
        # Update current population and per capita consumption for the next iteration
        currentPopulation = total_pop
        #perCapitaConsumption = per_consumption
        
        # Vary the growth rate (you can modify this logic based on your preference)
        if year % 2 == 0:
            growth_rate *= 1  # Increase the growth rate every even year
        else:
            growth_rate *= 1.5  # Decrease the growth rate every odd year

    return years_range, rice_requirements

years_range, rice_requirements = compute_rice_requirements_over_years_vary_growth(i_currentPopulation, i_growthRate, i_perCapitaConsumption, i_startyear, i_endyear)

# Create the line chart
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=years_range,
    y=rice_requirements,
    mode= 'lines+markers',
    text=[numerize.numerize(val) for val in rice_requirements],
    #textposition='auto',
    marker=dict(color='skyblue')
))

# Set chart's layout details
fig.update_layout(
    title= dict(text='Rice Requirement Over the Years (ton/year)', x=0.35),
    xaxis_title="Year",
    yaxis_title="Rice Requirement (ton)",
)
#Set the tooltip size
fig.update_traces(hoverlabel=dict(bgcolor='#e0dcdc',font_size=15))

# Display the plotly chart in Streamlit
st.plotly_chart(fig, use_container_width=True)