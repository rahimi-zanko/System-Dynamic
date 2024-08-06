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
  
# System Dynamic Function  

def nlInputCostPerHaPerCrop(i_subsidyOnNLInput, i_unitNLCost):
  """returns the NL input cost per Ha per crop"""
  o_nlInputCostPerHaPerCrop = max(0,i_unitNLCost - i_subsidyOnNLInput)

  return o_nlInputCostPerHaPerCrop

def laborCostPerHaPerCrop(i_laborUsePerHaPerCrop, i_unitLaborCost):
  """returns the labor cost per Ha per crop"""
  o_laborCostPerHaPerCrop = i_unitLaborCost * i_laborUsePerHaPerCrop

  return o_laborCostPerHaPerCrop

def laborUseRatio(i_laborCostPerHaPerCrop, i_indicateLaborUsefromYieldProfile):
  """returns the labor cost per Ha per crop"""
  o_laborUseRatio = i_laborCostPerHaPerCrop / i_indicateLaborUsefromYieldProfile

  return o_laborUseRatio

def desiredNLInputUse(i_indicatedDesireNLInputUse, i_indicatedNLinputUsefromYieldProfile):
  """returns the desired input use"""
  o_desiredNLInputUse = min(i_indicatedDesireNLInputUse, i_indicatedNLinputUsefromYieldProfile)

  return o_desiredNLInputUse

def nlInputUseIndexPerHaPerCrop(i_desiredNLInputUse, i_nlInputUseIndexPerHaPerCrop,  i_timestep):
  """returns the NL input cost per Ha per crop"""
  i_NLinputGap = i_desiredNLInputUse - i_nlInputUseIndexPerHaPerCrop
  i_changeinInput = i_NLinputGap / 1
  o_nlInputUseIndexPerHaPerCrop = INTEG(i_changeinInput, 100, i_timestep)

  return o_nlInputUseIndexPerHaPerCrop

def labourUsePerHaPerCrop(i_changeInLabourUse, i_timestep):
  """returns the labour use per ha per crop"""
  o_labourUsePerHaPerCrop = INTEG (i_changeInLabourUse, 35, i_timestep)

  return o_labourUsePerHaPerCrop

def labourGap (i_desiredLabourUse, i_changeInLabourUse, i_timestep):
  """returns the labourgap"""
  v_labourUsePerHaPerCrop = labourUsePerHaPerCrop (i_changeInLabourUse, i_timestep)
  o_labourGap = i_desiredLabourUse - v_labourUsePerHaPerCrop
  
  return o_labourGap

def nlInputUseRatio (i_nlInputUseIndexPerHaPerCrop, i_indicatedNLinputUsefromYieldProfile):
  """return the NL input use ratio"""
  o_nlInputUseRatio = i_nlInputUseIndexPerHaPerCrop - i_indicatedNLinputUsefromYieldProfile

  return o_nlInputUseRatio

def expectedLabourCostPerHaPerCrop (i_laborUsePerHaPerCrop, i_unitLaborCost, i_timetoAdjustExpectedCost):
  """return the expected labour cost per ha per crop"""
  time_step = 1
  o_laborCostPerHaPerCrop = []
  v_laborCostPerHaPerCrop = laborCostPerHaPerCrop(i_laborUsePerHaPerCrop, i_unitLaborCost)
  o_expectedLabourCostPerHaPerCrop = SMOOTH([v_laborCostPerHaPerCrop], i_timetoAdjustExpectedCost, time_step)
  o_laborCostPerHaPerCrop.append(v_laborCostPerHaPerCrop)

  return o_expectedLabourCostPerHaPerCrop, o_laborCostPerHaPerCrop

def expectedNLInputCostPerHaPerCrop (i_subsidyOnNLInput, i_unitNLCost, i_timetoAdjustExpectedCost):
  """return the expected NL input cost per ha per crop"""
  time_step = 1
  o_nlInputCostPerHaPerCrop = []
  v_nlInputCostPerHaPerCrop = nlInputCostPerHaPerCrop(i_subsidyOnNLInput, i_unitNLCost)
  o_expectedNLInputCostPerHaPerCrop = SMOOTH([v_nlInputCostPerHaPerCrop], i_timetoAdjustExpectedCost, time_step)
  o_nlInputCostPerHaPerCrop.append(v_nlInputCostPerHaPerCrop)

  return o_expectedNLInputCostPerHaPerCrop, o_nlInputCostPerHaPerCrop

#Apps body
subpage = st.selectbox('Pick one:', ['Expected labor cost per ha per crop','Expected NL input cost per ha per crop'])

if subpage == 'Expected labor cost per ha per crop':

  #parameter for the expected labor cost per ha per crop
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    i_unitLaborCost = int(st.number_input("Please enter the unit labor cost (RM/man days):", value=1000, key="2"))
  with col2:
    i_laborUsePerHaPerCrop = int(st.number_input("Please enter days of labor use per ha per crop (man days/ha/crop):", value=100, key="3"))
  with col3:
    i_timetoAdjustExpectedCost = st.select_slider("Slide to select the time to adjust expected cost (year):", options=[1,2,3,4,5], key="4")
  with col4:
    i_startyear = int(st.number_input("Please enter the starting year:", value=2000, key="5"))
    i_endyear = int(st.number_input("Please enter the ending year:", value=2010, key="6"))
  
  #System dynamic to compute the expected labor cost per ha per crop

  def compute_expected_labor_cost_over_years(i_laborUsePerHaPerCrop, i_unitLaborCost, i_timetoAdjustExpectedCost, i_startyear, i_endyear):
    i_startyear = int(i_startyear)
    i_endyear = int(i_endyear)
    years_range = list(range(int(i_startyear), int(i_endyear) + 1))
    expectedLaborCost = []
    o_laborCostPerHaPerCrop = []
    for year in years_range:
        expectedLaborCost.append(expectedLabourCostPerHaPerCrop (i_laborUsePerHaPerCrop, i_unitLaborCost, i_timetoAdjustExpectedCost))
        
    return years_range, expectedLaborCost, o_laborCostPerHaPerCrop

  years_range, expectedLaborCost, o_laborCostPerHaPerCrop = compute_expected_labor_cost_over_years(i_laborUsePerHaPerCrop, i_unitLaborCost, i_timetoAdjustExpectedCost, i_startyear, i_endyear)

#plotting the ouput
  fig = go.Figure()

  fig.add_trace(go.Scatter(
    x=years_range,
    y=o_laborCostPerHaPerCrop,
    #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
    textposition='top center',
    mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
    marker_color='skyblue',
    line=dict(color='skyblue', width=2)
    ))

# Set chart's layout details
  fig.update_layout(
    title=dict(text='Labor cost per ha per crop Over the Years (RM/ha*crop)',x=0.35),
    xaxis_title="Year",
    yaxis_title="Labor Cost per ha per crop (RM)"
    )

#Set the tooltip size
  fig.update_traces(hoverlabel=dict(bgcolor='#e0dcdc',font_size=15))

# Display the plotly chart in Streamlit
  st.plotly_chart(fig, use_container_width=True)


  fig = go.Figure()

  fig.add_trace(go.Scatter(
    x=years_range,
    y=expectedLaborCost,
    #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
    textposition='top center',
    mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
    marker_color='skyblue',
    line=dict(color='skyblue', width=2)
    ))

# Set chart's layout details
  fig.update_layout(
    title=dict(text='Expected labor cost per ha per crop Over the Years (RM/ha*crop)',x=0.35),
    xaxis_title="Year",
    yaxis_title="Expected labor cost per ha per crop (RM)"
    )
  
#Set the tooltip size
  fig.update_traces(hoverlabel=dict(bgcolor='#e0dcdc',font_size=15))  

# Display the plotly chart in Streamlit
  st.plotly_chart(fig, use_container_width=True)

else:

  #parameter for the expected non-labor input cost per ha per crop expectedNLInputCostPerHaPerCrop (i_subsidyOnNLInput, i_unitNLCost, i_timetoAdjustExpectedCost)
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    i_subsidyOnNLInput = int(st.number_input("Please enter the subsidy on non-labor input (RM):", value=1000, key="2"))
  with col2:
    i_unitNLCost = int(st.number_input("Please enter the price of paddy (RM/ton):", value=1000, key="3"))
  with col3:
    i_timetoAdjustExpectedCost = st.select_slider("Slide to select the time to adjust expected cost (year):", options=[1,2,3,4,5], key="4")
  with col4:
    i_startyear = int(st.number_input("Please enter the starting year:", value=2000, key="5"))
    i_endyear = int(st.number_input("Please enter the ending year:", value=2010, key="6"))

    #System dynamic to compute the expected labor cost per ha per crop

  def compute_expected_NLInput_cost_over_years(i_subsidyOnNLInput, i_unitNLCost, i_timetoAdjustExpectedCost, i_startyear, i_endyear):
    i_startyear = int(i_startyear)
    i_endyear = int(i_endyear)
    years_range = list(range(int(i_startyear), int(i_endyear) + 1))
    expectedNLInputCost = []
    o_nlInputCostPerHaPerCrop = []
    for year in years_range:
        expectedNLInputCost.append(expectedLabourCostPerHaPerCrop (i_subsidyOnNLInput, i_unitNLCost, i_timetoAdjustExpectedCost))
        
    return years_range, expectedNLInputCost, o_nlInputCostPerHaPerCrop

  years_range, expectedNLInputCost, o_nlInputCostPerHaPerCrop = compute_expected_NLInput_cost_over_years(i_subsidyOnNLInput, i_unitNLCost, i_timetoAdjustExpectedCost, i_startyear, i_endyear)

#plotting the ouput
  fig = go.Figure()

  fig.add_trace(go.Scatter(
    x=years_range,
    y=o_nlInputCostPerHaPerCrop,
    #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
    textposition='top center',
    mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
    marker_color='skyblue',
    line=dict(color='skyblue', width=2)
    ))

# Set chart's layout details
  fig.update_layout(
    title=dict(text='Non-labor input cost per ha per crop Over the Years (RM/ha*crop)',x=0.35),
    xaxis_title="Year",
    yaxis_title="Non-labor input Cost per ha per crop (RM)"
    )

# Display the plotly chart in Streamlit
  st.plotly_chart(fig)


  fig = go.Figure()

  fig.add_trace(go.Scatter(
    x=years_range,
    y=expectedNLInputCost,
    #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
    textposition='top center',
    mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
    marker_color='skyblue',
    line=dict(color='skyblue', width=2)
    ))

# Set chart's layout details
  fig.update_layout(
    title=dict(text='Expected Non-labor input cost per ha per crop Over the Years (RM/ha*crop)',x=0.35),
    xaxis_title="Year",
    yaxis_title="Non-labor input cost per ha per crop (RM)"
    )

# Display the plotly chart in Streamlit
  st.plotly_chart(fig)
