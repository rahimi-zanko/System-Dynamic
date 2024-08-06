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

#VENSIM-PYTHON FUNCTION
def SMOOTH(input_series, smoothing_time, time_step):

  #Simple exponential smoothing function.
    
  #:param input_series: Input data series (a list or array).
  #:param smoothing_time: Time over which the smoothing occurs.
  #:param time_step: Simulation time step.
  #:return: Smoothed data series.

  # Exponential smoothing factor
  alpha = time_step / (smoothing_time + time_step)
    
  # Initialize the smoothed series with the first value of the input series
  smoothed_series = [input_series[0]]
    
  for i in range(1, len(input_series)):
    next_value = alpha * input_series[i] + (1 - alpha) * smoothed_series[-1]
    smoothed_series.append(next_value)
        
    return smoothed_series
  
def INTEG(flow_series, initial_value, time_step):

  #Integrate a flow series using the Euler method.
    
  #:param flow_series: Flow rate data series (a list or array).
  #:param initial_value: Initial value of the stock/accumulator.
  #:param time_step: Simulation time step.
  #:return: Accumulated stock series.
  
  stock_series = [initial_value]
  
  for flow in flow_series:
    next_value = stock_series[-1] + flow * time_step
    stock_series.append(next_value)
        
    return stock_series
  
def SMOOTHI(input_series, integration_time, time_step):
    
    #Integral version of the SMOOTH function. 
    #Represents the cumulative sum of past values of a variable with exponential decay.
    
    #:param input_series: Input data series (a list or array).
    #:param integration_time: Time over which the integration occurs.
    #:param time_step: Simulation time step.
    #:return: Cumulative sum with exponential decay.
  
    
    # Exponential decay factor
    alpha = time_step / (integration_time + time_step)
    
    # Initialize the integrated series with the first value of the input series multiplied by the time step
    integrated_series = [input_series[0] * time_step]
    
    for i in range(1, len(input_series)):
        next_value = integrated_series[-1] + alpha * (input_series[i] * time_step - integrated_series[-1])
        integrated_series.append(next_value)
        
    return integrated_series
  
#System Dynamic Functions

def timeToImplementPotentialYield(i_yieldDelayTime):
  """returns the time to implement potential yield"""
  o_timeToImplementPotentialYield = i_yieldDelayTime

  return o_timeToImplementPotentialYield


#def implementedPotentialYieldPerHaPerCrop(i_timeToImplementPotentialYield, i_potentialPaddyYieldPerHaPerCrop):
  """returns the implemented potential yield per Ha per crop"""
  time_step = 1
  smoothImplementedPotentialYieldPerHaPerCrop = SMOOTH([i_potentialPaddyYieldPerHaPerCrop], i_timeToImplementPotentialYield, time_step)
  if smoothImplementedPotentialYieldPerHaPerCrop is not None:
    smoothImplementedPotentialYieldPerHaPerCrop = [1 if x is None else x for x in smoothImplementedPotentialYieldPerHaPerCrop]
    o_implementedPotentialYieldPerHaPerCrop = [x/2 for x in smoothImplementedPotentialYieldPerHaPerCrop]
  else:
    # handle the None case or assign a default value, e.g.
    o_implementedPotentialYieldPerHaPerCrop = [1]

  return o_implementedPotentialYieldPerHaPerCrop

def implementedPotentialYieldPerHaPerCrop(i_timeToImplementPotentialYield, i_potentialPaddyYieldPerHaPerCrop, i_initialPotentitalPaddyYieldPerhaPerCrop):
  """returns the implemented potential yield per Ha per crop"""
  o_implementedPotentialYieldPerHaPerCrop = []
  o_implementedPotentialYieldPerHaPerCrop.append(SMOOTH([i_potentialPaddyYieldPerHaPerCrop] , i_timeToImplementPotentialYield, 0.95 * i_initialPotentitalPaddyYieldPerhaPerCrop))

  return o_implementedPotentialYieldPerHaPerCrop

#def indicatedInputUse(i_implementedPotentialYieldPerHaPerCrop):
  """returns the indicated input use"""
  o_indicatedInputUse = i_implementedPotentialYieldPerHaPerCrop * 5

  return o_indicatedInputUse

def paddyYieldRealizedPerHaPerCrop(i_implementedPotentialYieldPerHaPerCrop,i_effectOfLabourUseOnYield,i_effectOfNLInputOnYield):
  """returns the paddy yield realized per ha per crop"""
  o_paddyYieldRealizedPerHaPerCrop = int(i_implementedPotentialYieldPerHaPerCrop * i_effectOfLabourUseOnYield * i_effectOfNLInputOnYield)

  return o_paddyYieldRealizedPerHaPerCrop

def desiredRnD(i_pressureofSSLOnRnD, i_RnDCapacityIndex):
  """returns the desired R&D"""
  o_desiredRnD = i_pressureofSSLOnRnD * i_RnDCapacityIndex

  return o_desiredRnD

def changeInRnD(i_RnDGap, i_AdjustmentTimeForRnD):
  """returns the changes in R&D"""
  o_changeInRnD = i_RnDGap / i_AdjustmentTimeForRnD

  return o_changeInRnD

def paddyProducedPerHaPerCrop(i_paddyYieldRealizedPerHaPerCrop, i_paddyPostHarvestLoss):
  """returns the paddy produced per Ha per crop"""
  o_paddyProducedPerHaPerCrop = int(i_paddyYieldRealizedPerHaPerCrop * ( 1 - i_paddyPostHarvestLoss))

  return o_paddyProducedPerHaPerCrop

def paddySoldPerHaPerCrop(i_paddyProducedPerHaPerCrop, i_paddyDeductionFraction):
  """returns the paddy sold per Ha per crop"""
  o_paddySoldPerHaPerCrop = i_paddyProducedPerHaPerCrop * ( 1 - i_paddyDeductionFraction )

  return o_paddySoldPerHaPerCrop

def riceProductionPerHaPerCrop(i_paddyToRiceConversion,i_paddySoldPerHaPerCrop):
  """returns the rice production per Ha per crop"""
  o_riceProductionPerHaPerCrop = i_paddyToRiceConversion * i_paddySoldPerHaPerCrop

  return o_riceProductionPerHaPerCrop

def totalRiceProductionPerYr(i_riceProductionPerHaPerCrop,i_paddyPlantedArea,i_adjustmentFactorForProductionCalculation):
  """returns the total rice production per year"""
  #o_totalRiceProductionPerYr = i_riceProductionPerHaPerCrop * i_paddyPlantedArea * i_adjustmentFactorForProductionCalculation
  o_totalRiceProductionPerYr = [i_riceProductionPerHaPerCrop * val * i_adjustmentFactorForProductionCalculation for val in i_paddyPlantedArea]

  return o_totalRiceProductionPerYr

def ssl(i_riceRequirement, i_totalRiceProductionPerHaPerYr):
  """returns the ssl"""
  o_ssl = (i_riceRequirement/ i_totalRiceProductionPerHaPerYr) * 100
  #o_ssl = i_totalRiceProductionPerHaPerYr / i_riceRequirement

  return o_ssl

def smoothedSsl(i_timeToSmoothSSL, i_riceRequirement, i_totalRiceProductionPerHaPerYr):
  """returns the Smoothed SSL"""
  time_step = 1
  v_ssl = [ssl(i_riceRequirement, i_totalRiceProductionPerHaPerYr)]
  o_smoothedSsl = SMOOTH(v_ssl, i_timeToSmoothSSL, time_step)
  if o_smoothedSsl is None:
    o_smoothedSsl = 0
  return o_smoothedSsl

def sslRatio(i_sslTarget, i_ssl, i_timeToSmoothSSL, i_riceRequirement, i_totalRiceProductionPerHaPerYr):
  """returns the SSL ratio"""
  v_smoothedSsl = smoothedSsl(i_ssl, i_timeToSmoothSSL, i_riceRequirement, i_totalRiceProductionPerHaPerYr, 1)
  o_sslRatio = min(i_sslTarget, v_smoothedSsl / i_sslTarget)

  return o_sslRatio

#def expectedSSL(i_ssl):
  """returns the expected SSL"""
  o_expectedSSL = i_ssl * 0.5

  return o_expectedSSL

def rndCapacityIndex(i_changeInRnd, i_initRndCapacityIndex, i_time_step):
  """returns the rnd capacity index"""
  o_rndCapacityIndex = INTEG(i_changeInRnd, i_initRndCapacityIndex, i_time_step)

  return o_rndCapacityIndex

def changeInIntensity(i_croppingIntensity, i_effectOfRndOnIntensity):
  """returns the change in intensity"""
  o_changeInIntensity = i_croppingIntensity * (0.002/2) * i_effectOfRndOnIntensity

  return o_changeInIntensity

#def physicalPaddyLand(i_expectedSSL):
  """returns the physical paddy land"""
  o_physicalPaddyLand = i_expectedSSL * 0.4

  return o_physicalPaddyLand

#def rdCapacity(i_expectedSSL):
  """returns the rd capacity"""
  o_rdCapacity = i_expectedSSL * 6

  return o_rdCapacity

def croppingIntesity(i_changesInIntensity):
  """returns the cropping intesity"""
  time_step = 1
  initial_value = 1.6
  o_croppingIntesity = INTEG ([i_changesInIntensity],initial_value, time_step)

  return o_croppingIntesity

def paddyPlantedArea(i_physicalPaddyLand, i_changesInIntensity):
  """returns the paddy planted area"""
  v_croppingIntensity = croppingIntesity(i_changesInIntensity)
  o_paddyPlantedArea = i_physicalPaddyLand * v_croppingIntensity

  return o_paddyPlantedArea

def change_in_potential_yield(i_indicated_yield, i_paddy_yield, i_adjustment_time):
  """returns the change in potential yield"""
  o_change_in_potential_yield = (i_indicated_yield - i_paddy_yield) / i_adjustment_time

  return o_change_in_potential_yield

def potentialPaddyYieldPerHaPerCrop(indicated_yield, paddy_yield, adjustment_time, i_initialPotentialPaddyYieldPerhaPerCrop, i_timeStep):
  """returns the cropping intesity"""
  v_ChangeInPotentialYeild = change_in_potential_yield(indicated_yield, paddy_yield, adjustment_time)
  o_potentialPaddyYieldPerHaPerCrop = INTEG(v_ChangeInPotentialYeild, i_initialPotentialPaddyYieldPerhaPerCrop, i_timeStep)

  return o_potentialPaddyYieldPerHaPerCrop

def calculate_yield_change_fraction(i_normal_yield_growth_fraction, i_rndEffect, i_yield_target_effect):
  """returns the calculated yield change fraction"""
  i_normal_yield_growth_fraction = 1.6
  o_yield_change_fraction = i_normal_yield_growth_fraction * i_rndEffect * i_yield_target_effect
  
  return o_yield_change_fraction

#Apps body
subpage = st.selectbox('Pick one:', ['Self-Suffiency Level (SSL)','Paddy produced per ha per crop', 'Paddy sold per ha per crop', 'Total rice production per ha per crop', 'Implemented potential yield per ha per crop'])

if subpage == 'Self-Suffiency Level (SSL)':

#parameter for SSL
  col1, col2, col3 = st.columns(3)
  with col1:
    i_totalRiceProductionPerHaPerYr = int(st.number_input("Please enter the total weight of rice production (ton): ", value=1000, key="2"))
  with col2:
    i_riceRequirement = int(st.number_input("Please enter the number for rice requirement (ton):", value=1000, key="3"))
  with col3:
    i_startyear = int(st.number_input("Please enter the starting year:", value=2000, key="4"))
    i_endyear = int(st.number_input("Please enter the ending year:", value=2010, key="5"))

#System dynamic to compute the self-suffiency level (SSL)

  def compute_SSL_over_years(i_totalRiceProductionPerHaPerYr, i_riceRequirement, i_startyear, i_endyear):
    i_startyear = int(i_startyear)
    i_endyear = int(i_endyear)
    years_range = list(range(int(i_startyear), int(i_endyear) + 1))
    i_timeToSmoothSSL = 2
    expected_ssl = []
    smoothed_ssl = []
    for year in years_range:
        expected_ssl.append(ssl(i_totalRiceProductionPerHaPerYr, i_riceRequirement))
        smoothed_ssl.append(smoothedSsl(i_riceRequirement, i_totalRiceProductionPerHaPerYr, i_timeToSmoothSSL))
        
        # Vary the growth rate (you can modify this logic based on your preference)
        #if year % 2 == 0:
            #growth_rate *= 1  # Increase the growth rate every even year
        #else:
            #growth_rate *= 1.04  # Decrease the growth rate every odd year

    return years_range, expected_ssl, smoothed_ssl
    
  years_range, expected_ssl, smoothed_ssl = compute_SSL_over_years(i_totalRiceProductionPerHaPerYr, i_riceRequirement, i_startyear, i_endyear)

#plotting the ouput
  #col1, col2 = st.columns(2)
  #with col1:
  fig = go.Figure()

  fig.add_trace(go.Scatter(
    x=years_range,
    y=expected_ssl,
    #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
    textposition='top center',
    mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
    marker_color='skyblue',
    line=dict(color='skyblue', width=2)
    ))

# Set chart's layout details
  fig.update_layout(
    title=dict(text='Self-sufficiency level (SSL) Over the Years', x=0.35),
    xaxis_title="Year",
    yaxis_title="Self-sufficiency level (SSL)"
    )

#Set the tooltip size
  fig.update_traces(hoverlabel=dict(bgcolor='#e0dcdc',font_size=15))

# Display the plotly chart in Streamlit
  st.plotly_chart(fig, use_container_width=True)

  #with col2:
    #fig = go.Figure()

    #fig.add_trace(go.Scatter(
      #x=years_range,
      #y=smoothed_ssl,
      #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
      #textposition='top center',
      #mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
      #marker_color='skyblue',
      #line=dict(color='skyblue', width=2)
      #))

# Set chart's layout details
    #fig.update_layout(
      #title='Smoothed Self-sufficiency level Over the Years',
      #xaxis_title="Year",
      #yaxis_title="Smoothed SSL"
      #)

# Display the plotly chart in Streamlit
    #st.plotly_chart(fig)

elif subpage == 'Paddy produced per ha per crop':

#parameter for Paddy produce per ha per crop
  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    i_implementedPotentialYieldPerHaPerCrop = int(st.number_input("Please enter the implemented potential yield per ha per crop (ton/ha*corp):", value=1000, key="6"))
  with col2:
    i_effectOfLabourUseOnYield = st.select_slider("Slide to select the effect of labour use on yield (dmnl):", options=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0] , key="7")
  with col3:
    i_effectOfNLInputOnYield = st.select_slider("Slide to select the effect of non-labour input on yield (dmnl):", options=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0], key="8")
  with col4:
    i_startyear = int(st.number_input("Please enter the starting year:", value=2000, key="9"))
    i_endyear = int(st.number_input("Please enter the ending year:", value=2010, key="10"))
  with col5:
    i_paddyPostHarvestLoss = st.select_slider("Slide to select the paddy post harvest loss (dmnl):", options=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], key="11")

#System dynamic to compute the paddy produce per ha per crop

  def compute_paddy_produce_over_years(i_implementedPotentialYieldPerHaPerCrop, i_effectOfLabourUseOnYield, i_effectOfNLInputOnYield, i_paddyPostHarvestLoss, i_startyear, i_endyear):
    i_startyear = int(i_startyear)
    i_endyear = int(i_endyear)
    years_range = list(range(int(i_startyear), int(i_endyear) + 1))
    paddy_produce = []
    paddy_yield = []
    for year in years_range:
        v_paddyYield = paddyYieldRealizedPerHaPerCrop(i_implementedPotentialYieldPerHaPerCrop, i_effectOfLabourUseOnYield, i_effectOfNLInputOnYield)
        paddy_produce.append(paddyProducedPerHaPerCrop(v_paddyYield, i_paddyPostHarvestLoss))
        paddy_yield.append(v_paddyYield)
        
    return years_range, paddy_yield, paddy_produce

  years_range, paddy_yield, paddy_produce = compute_paddy_produce_over_years(i_implementedPotentialYieldPerHaPerCrop, i_effectOfLabourUseOnYield, i_effectOfNLInputOnYield, i_paddyPostHarvestLoss, i_startyear, i_endyear)

#plotting the ouput
  col1, col2, = st.columns(2)
  with col1:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
      x=years_range,
      y=paddy_yield,
      #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
      textposition='top center',
      mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
      marker_color='skyblue',
      line=dict(color='skyblue', width=2)
      ))

# Set chart's layout details
    fig.update_layout(
      title=dict(text='Paddy Yield Realized per ha per crop Over the Years'),
      xaxis_title="Year",
      yaxis_title="Paddy Yield Realized per ha per crop (ton/ha*crop)"
      )

#Set the tooltip size
    fig.update_traces(hoverlabel=dict(bgcolor='#e0dcdc',font_size=15))

# Display the plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

  with col2:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
      x=years_range,
      y=paddy_produce,
      #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
      textposition='top center',
      mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
      marker_color='skyblue',
      line=dict(color='skyblue', width=2)
      ))

# Set chart's layout details
    fig.update_layout(
      title=dict(text='Paddy Produced per ha per crop Over the Years'),
      xaxis_title="Year",
      yaxis_title="Paddy Produced per ha per crop (ton/ha*crop)"
      )

#Set the tooltip size
    fig.update_traces(hoverlabel=dict(bgcolor='#e0dcdc',font_size=15))

# Display the plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif subpage == 'Paddy sold per ha per crop':

#parameter for paddy sold per ha per crop
  col1, col2, col3= st.columns(3)
  with col1:
    i_paddyProducedPerHaPerCrop = int(st.number_input("Please enter the paddy produced per ha per crop (ton/ha*crop):", value=1000, key="12"))
  with col2:
    i_paddyDeductionFraction = st.select_slider("Slide to select the paddy deduction fraction (dmnl):", options=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], key="13")
  with col3:
    i_startyear = int(st.number_input("Please enter the starting year:", value=2000, key="14"))
    i_endyear = int(st.number_input("Please enter the ending year:", value=2010, key="15"))

#System dynamic to compute the paddy sold per ha per crop

  def compute_paddy_sold_over_years(i_paddyProducedPerHaPerCrop, i_paddyDeductionFraction, i_startyear, i_endyear):
    i_startyear = int(i_startyear)
    i_endyear = int(i_endyear)
    years_range = list(range(int(i_startyear), int(i_endyear) + 1))
    paddy_sold = []
    for year in years_range:
        paddy_sold.append(paddyProducedPerHaPerCrop(i_paddyProducedPerHaPerCrop, i_paddyDeductionFraction))
        
    return years_range, paddy_sold

  years_range, paddy_sold = compute_paddy_sold_over_years(i_paddyProducedPerHaPerCrop, i_paddyDeductionFraction, i_startyear, i_endyear)

#plotting the ouput

  fig = go.Figure()

  fig.add_trace(go.Scatter(
    x=years_range,
    y=paddy_sold,
    #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
    textposition='top center',
    mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
    marker_color='skyblue',
    line=dict(color='skyblue', width=2)
    ))

# Set chart's layout details
  fig.update_layout(
    title=dict(text='Paddy Sold per ha per crop Over the Years', x=0.35),
    xaxis_title="Year",
    yaxis_title="Paddy Sold per ha per crop (ton/ha*crop)"
    )

#Set the tooltip size
  fig.update_traces(hoverlabel=dict(bgcolor='#e0dcdc',font_size=15))

# Display the plotly chart in Streamlit
  st.plotly_chart(fig, use_container_width=True)

elif subpage == 'Total rice production per ha per crop':

#parameter for the total rice production per ha per crop
  col1, col2, col3, col4, col5, col6 = st.columns(6)
  with col1:
    i_physicalPaddyLand = int(st.number_input("Please enter area of paddy planted (ha):", value=1000, key="16"))
  with col2:
    i_croppingIntensity = int(st.number_input("Please enter the cropping intensity (crop/year):", value = 1000, key="17"))
  with col3:
    i_paddyToRiceConversion = st.select_slider("Slide to select paddy to rice conversion (dmnl):", options=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], key="18")
  with col4:
    i_paddySoldPerHaPerCrop = int(st.number_input("Please enter the paddy sold per ha per crop (ton/ha*crop):", value=2000, key="19"))
  with col5:
    i_adjustmentFactorForProductionCalculation = st.slider("Slide to select the cropping intensity:", 0, 10, key="20")
  with col6:
    i_startyear = int(st.number_input("Please enter the starting year:", value=2000, key="21"))
    i_endyear = int(st.number_input("Please enter the ending year:", value=2010, key="22"))

#System dynamic to compute the rice production per ha per crop

  def compute_rice_production_over_years(i_physicalPaddyLand, i_croppingIntensity, i_paddyToRiceConversion, i_paddySoldPerHaPerCrop, i_adjustmentFactorForProductionCalculation, i_startyear, i_endyear):
    i_startyear = int(i_startyear)
    i_endyear = int(i_endyear)
    years_range = list(range(int(i_startyear), int(i_endyear) + 1))
    paddy_planted = []
    rice_production = []
    totalrice_production = []
    for year in years_range:
        v_paddyPlanted = paddyPlantedArea(i_physicalPaddyLand, i_croppingIntensity)
        v_riceProduction = riceProductionPerHaPerCrop(i_paddyToRiceConversion,i_paddySoldPerHaPerCrop)
        #print(type(v_riceProduction))
        #print(type(v_paddyPlanted))
        totalrice_production.append(totalRiceProductionPerYr(v_riceProduction,v_paddyPlanted, i_adjustmentFactorForProductionCalculation))
        paddy_planted.append(v_paddyPlanted)
        rice_production.append(v_riceProduction)
      
    return years_range, paddy_planted, rice_production, totalrice_production
  
  years_range, paddy_planted, rice_production, totalrice_production = compute_rice_production_over_years(i_physicalPaddyLand, i_croppingIntensity, i_paddyToRiceConversion, i_paddySoldPerHaPerCrop, i_adjustmentFactorForProductionCalculation, i_startyear, i_endyear)
#plotting the ouput
  col1, col2 = st.columns(2)
  with col1:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
      x=years_range,
      y=paddy_planted,
      #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
      textposition='top center',
      mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
      marker_color='skyblue',
      line=dict(color='skyblue', width=2)
      ))

# Set chart's layout details
    fig.update_layout(
      title=dict(text='Area of Paddy Planted per ha per crop Over the Years'),
      xaxis_title="Year",
      yaxis_title="Area of Paddy Planted per ha per crop (ha)"
      )

#Set the tooltip size
    fig.update_traces(hoverlabel=dict(bgcolor='#e0dcdc',font_size=15))

# Display the plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

  with col2:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
      x=years_range,
      y=rice_production,
      #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
      textposition='top center',
      mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
      marker_color='skyblue',
      line=dict(color='skyblue', width=2)
      ))

# Set chart's layout details
    fig.update_layout(
      title=dict(text='Rice Production per ha per crop Over the Years'),
      xaxis_title="Year",
      yaxis_title="Rice Production per ha per crop (ton/ha*crop)"
      )

#Set the tooltip size
    fig.update_traces(hoverlabel=dict(bgcolor='#e0dcdc',font_size=15))

# Display the plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

  fig = go.Figure()

  fig.add_trace(go.Scatter(
    x=years_range,
    y=totalrice_production,
    #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
    textposition='top center',
    mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
    marker_color='skyblue',
    line=dict(color='skyblue', width=2)
    ))

# Set chart's layout details
  fig.update_layout(
    title=dict(text='Total rice production Over the Years', x=0.35),
    xaxis_title="Year",
    yaxis_title="Total rice production (ton/year)"
    )

#Set the tooltip size
  fig.update_traces(hoverlabel=dict(bgcolor='#e0dcdc',font_size=15))

# Display the plotly chart in Streamlit
  st.plotly_chart(fig, use_container_width=True)

else:
  
#parameter for the implemented potential yield per ha per crop
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    i_timeToImplementPotentialYield = st.slider("Slide to select the time to implemented potential yield (year):",0, 10, key="23")
  with col2:
    i_potentialPaddyYieldPerHaPerCrop = int(st.number_input("Please enter the potential paddy yield per ha per crop (ton):", value=1000, key="24"))
  with col3:
    i_initialPotentialPaddyYieldPerHaPerCrop = int(st.number_input("Slide to select the effect of labor use on yield (ton):", value=1000, key="25"))
  with col4:
    i_startyear = int(st.number_input("Please enter the starting year:", value=2000, key="26"))
    i_endyear = int(st.number_input("Please enter the ending year:", value=2010, key="27"))
  
#System dynamic to compute the implemented potential yield per ha per crop

  def compute_implemented_potential_yield_over_years(i_timeToImplementPotentialYield, i_potentialPaddyYieldPerHaPerCrop, i_initialPotentialPaddyYieldPerHaPerCrop, i_startyear, i_endyear):
    i_startyear = int(i_startyear)
    i_endyear = int(i_endyear)
    years_range = list(range(int(i_startyear), int(i_endyear) + 1))
    implementedPotentialYield = []
    for year in years_range:
      implementedPotentialYield.append(implementedPotentialYieldPerHaPerCrop(i_timeToImplementPotentialYield, i_potentialPaddyYieldPerHaPerCrop, i_initialPotentialPaddyYieldPerHaPerCrop))
      
    return years_range, implementedPotentialYield
  
  years_range, implementedPotentialYield = compute_implemented_potential_yield_over_years(i_timeToImplementPotentialYield, i_potentialPaddyYieldPerHaPerCrop, i_initialPotentialPaddyYieldPerHaPerCrop, i_startyear, i_endyear)

#plotting the ouput
  #col1, col2 = st.columns(2)
  #with col1:
  fig = go.Figure()

  fig.add_trace(go.Scatter(
    x=years_range,
    y=implementedPotentialYield,
    #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
    textposition='top center',
    mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
    marker_color='skyblue',
    line=dict(color='skyblue', width=2)
    ))

# Set chart's layout details
  fig.update_layout(
    title=dict(text='Implemented Potential Yield per ha per crop Over the Years',x=0.20),
    xaxis_title="Year",
    yaxis_title="Implemented Potential Yield per ha per crop (ton/ha*crop)"
    )

#Set the tooltip size
  fig.update_traces(hoverlabel=dict(bgcolor='#e0dcdc',font_size=15))

# Display the plotly chart in Streamlit
  st.plotly_chart(fig, use_container_width=True)
