import streamlit  as st
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

#constant_value
timeToAdjustExpectedCost = 1
time_step = 1

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

#System Dynamic Function
def expectedVariableCostPerHaPerCrop(i_croppingIntensity, i_expectedNLInputCostPerHaPerCrop, i_expectedLaborCostPerHaPerCrop):
  """returns the expected variable cost per Ha per crop"""
  #i_croppingIntensity = INTEG(i_changeInIntensity, 1.6)
  #i_expectedNLInputCostPerHaPerCrop = SMOOTH (i_nlInputUseIndexPerHaPerCrop, i_timeToAdjustExpectedCost)
  #i_expectedLabourCostPerHaPerCrop = SMOOTH (i__laborCostPerHaPerCrop, i_timeToAdjustExpectedCost)
  o_expectedVariableCostPerHaPerCrop = i_croppingIntensity * (i_expectedNLInputCostPerHaPerCrop + i_expectedLaborCostPerHaPerCrop)

  return o_expectedVariableCostPerHaPerCrop

def farmerRevenuePerHaPerCrop(i_croppingIntensity, i_paddySoldPerHaPerCrop, i_subsidyPerUnitOutputSold, i_paddyPrice):
  """returns the expected revenue per Ha per crop"""
  #i_croppingIntensity = INTEG(changes in intensity, 1.6)
  o_farmerRevenuePerHaPerCrop = int((i_paddyPrice + i_subsidyPerUnitOutputSold) * i_croppingIntensity * i_paddySoldPerHaPerCrop)

  return o_farmerRevenuePerHaPerCrop

def expectedRevenuePerHaPerCrop(i_farmerRevenuePerHaPerCrop, i_incomeAverageTime, time_step):
  """returns the expected revenue per Ha per crop"""
  o_exprectedRevenuePerHaPerCrop = []
  o_exprectedRevenuePerHaPerCrop.append(SMOOTH(i_farmerRevenuePerHaPerCrop, i_incomeAverageTime, time_step))
  #smoothed_values = SMOOTH(i_farmerRevenuePerHaPerCrop, i_incomeAverageTime, time_step)
  #return smoothed_values[-1]  # Return the last value in the smoothed series

  return o_exprectedRevenuePerHaPerCrop [-1]

def expectedProfitabilityPerHaPerCrop(i_expectedVariableCostPerHaPerCrop, i_expectedRevenuePerHaPerCrop):
  """returns the expected profitability per Ha per crop"""
  o_expectedProfitabilityPerHaPerCrop = (i_expectedRevenuePerHaPerCrop - i_expectedVariableCostPerHaPerCrop) / i_expectedVariableCostPerHaPerCrop

  return o_expectedProfitabilityPerHaPerCrop

def paddyPrice_year(i_paddyPrice, years):
    v_paddyPrice = [i_paddyPrice]
    for year in range(years):
        v_paddyPrice.append(v_paddyPrice[-1] * (1+0.2))
    return v_paddyPrice [-1]

#def labour_cost(i_expectedLabourCostPerHaPerCrop, years):
    v_expectedLabourCostPerHaPerCrop = [i_expectedLabourCostPerHaPerCrop]
    for year in range(years):
        v_expectedLabourCostPerHaPerCrop.append(v_expectedLabourCostPerHaPerCrop[-1] * (1+2.1))
    return v_expectedLabourCostPerHaPerCrop [-1]

#def NLinput_cost(i_expectedLabourCostPerHaPerCrop, years):
    v_expectedLabourCostPerHaPerCrop = [i_expectedLabourCostPerHaPerCrop]
    for year in range(years):
        v_expectedLabourCostPerHaPerCrop.append(v_expectedLabourCostPerHaPerCrop[-1] * (1+2.1))
    return v_expectedLabourCostPerHaPerCrop [-1]

# Apps Body
col1, col2, col3= st.columns((1,2,1))
with col2:
  subpage = st.radio('Pick one:', ['Expected Revenue per ha per year','Expected Variable Cost per ha per year', 'Expected Profitability per ha per year'])

if subpage == 'Expected Revenue per ha per year':

#parameter Expected Revenue per ha per year
  col1, col2, col3, col4, col5, col6 = st.columns(6)
  with col1:
    i_subsidyPerUnitOutputSold = int(st.number_input("Please enter the subsidy per unit output sold (RM/ton):", value=1000, key="2"))
  with col2:
    i_paddyPrice = int(st.number_input("Please enter the price of paddy (RM/ton):", value=1000, key="3"))
  with col3:
    i_paddySoldPerHaPerCrop = int(st.number_input("Please enter the weight of paddy sold (ton):", key="4"))
  with col4:
    i_startyear = int(st.number_input("Please enter the starting year:", value=2000, key="5"))
    i_endyear = int(st.number_input("Please enter the ending year:", value=2010, key="6"))
  with col5:
    i_croppingIntensity = st.slider("Slide to select the cropping intensity:", 0, 10, key="7")
  with col6:
    i_incomeAverageTime = int(st.number_input("Please enter the income average time:", value=10, key="8"))

#System dynamic to compute the expected revenue per ha per crop

  def compute_expected_revenue_over_years(i_croppingIntensity, i_paddySoldPerHaPerCrop, i_subsidyPerUnitOutputSold, i_paddyPrice, i_incomeAverageTime, i_startyear, i_endyear):
    i_startyear = int(i_startyear)
    i_endyear = int(i_endyear)
    years_range = list(range(int(i_startyear), int(i_endyear) + 1))
    expected_revenue = []
    i_farmerRevenuePerHaPerCrop = []
    for year in years_range:
        i_farmerRevenuePerHaPerCrop.append(farmerRevenuePerHaPerCrop(i_croppingIntensity, i_paddySoldPerHaPerCrop, i_subsidyPerUnitOutputSold, i_paddyPrice))
        paddy_Price = paddyPrice_year(i_paddyPrice, year - i_startyear)
        expected_revenue.append(expectedRevenuePerHaPerCrop(i_farmerRevenuePerHaPerCrop, i_incomeAverageTime, time_step))
        
        # Update current paddy price for the next iteration
        i_paddyPrice = paddy_Price
        
    return years_range, expected_revenue

  years_range, expected_revenue = compute_expected_revenue_over_years(i_croppingIntensity, i_paddySoldPerHaPerCrop, i_subsidyPerUnitOutputSold, i_paddyPrice, i_incomeAverageTime, i_startyear, i_endyear)

#plotting the ouput
  fig = go.Figure()

  fig.add_trace(go.Scatter(
    x=years_range,
    y=expected_revenue,
    #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
    textposition='top center',
    mode='lines+markers+text',  # this means it will show lines, markers (dots) and text
    marker_color='skyblue',
    line=dict(color='skyblue', width=2)
    ))

  # Set chart's layout details
  fig.update_layout(
    title=dict(text='Expected Revenue per ha per crop Over the Years (RM/year)', x=0.35),
    xaxis_title="Year",
    yaxis_title="Expected Revenue per ha per crop (RM)"
    )

  # Display the plotly chart in Streamlit
  st.plotly_chart(fig, use_container_width=True)

elif subpage == 'Expected Profitability per ha per year':

#parameter Expected Profitability per ha per year
  col1, col2, col3 = st.columns(3)
  with col1:
    i_expectedRevenuePerHaPerCrop = int(st.number_input("Please enter the Expected revenue per ha per crop(RM/ha per year)", value=2000, key="8"))
  with col2:
    i_expectedVariableCostPerHaPerCrop = int(st.number_input("Please enter the Expected variable cost per ha per crop(RM/ha per year)", value=2000, key="9"))
  with col3:
    i_startyear = int(st.number_input("Please enter the starting year:", value=2000, key="10"))
    i_endyear = int(st.number_input("Please enter the ending year:", value=2010, key="11"))

# System dynamic to compute the expected profitability over the year
  def compute_expected_profitability_over_years(i_expectedRevenuePerHaPerCrop, i_expectedVariableCostPerHaPerCrop, i_startyear, i_endyear):
    i_startyear = int(i_startyear)
    i_endyear = int(i_endyear)
    years_range = list(range(int(i_startyear), int(i_endyear) + 1))
    expected_profitability = []
    for year in years_range:
        expected_profitability.append(expectedProfitabilityPerHaPerCrop(i_expectedRevenuePerHaPerCrop, i_expectedVariableCostPerHaPerCrop))
        
    return years_range, expected_profitability

  years_range, expected_profitability = compute_expected_profitability_over_years(i_expectedRevenuePerHaPerCrop, i_expectedVariableCostPerHaPerCrop, i_startyear, i_endyear)

#plotting the output
  fig = go.Figure()

  fig.add_trace(go.Scatter(
    x = years_range,
    y = expected_profitability,
    #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
    textposition = 'top center',
    mode = 'lines+markers+text',  # this means it will show lines, markers (dots) and text
    marker_color = 'skyblue',
    line=dict(color = 'skyblue', width = 2)
    ))

  # Set chart's layout details
  fig.update_layout(
    title=dict(text='Expected Profitability per ha per crop Over the Years (RM/year)',x=0.35),
    xaxis_title="Year",
    yaxis_title="Expected Profitability per ha per crop (RM)"
    )

  # Display the plotly chart in Streamlit
  st.plotly_chart(fig, use_container_width=True)

else:

#parameter Expected variable cost per ha per crop
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    i_expectedLabourCostPerHaPerCrop = int(st.number_input("Please enter the Expected labour cost per ha per crop", value=2000, key="12"))
  with col2:
    i_expectedNLCostPerHaPerCrop = int(st.number_input("Please enter the Expected non-labour cost per ha per crop", value=2000, key="13"))
  with col3:
    i_startyear = int(st.number_input("Please enter the starting year:", value=2000, key="14"))
    i_endyear = int(st.number_input("Please enter the ending year:", value=2010, key="15"))
  with col4:
    i_croppingIntensity = st.slider("Slide to select the cropping intensity:", 0, 10, key="16")

#System dynamic to compute the expected variable cost over years 
  def compute_expected_variable_cost_over_years(i_expectedLabourCostPerHaPerCrop, i_expectedNLCostPerHaPerCrop, i_croppingIntensity, i_startyear, i_endyear):
    i_startyear = int(i_startyear)
    i_endyear = int(i_endyear)
    years_range = list(range(int(i_startyear), int(i_endyear) + 1))
    expected_variable_cost = []
    #v_expectedLabourCostPerHaPerCrop = []
    #v_expectedNLCostPerHaPerCrop = []
    for year in years_range:
        #v_expectedLabourCostPerHaPerCrop.append(SMOOTH(i_expectedLabourCostPerHaPerCrop, 1, 1))
        #v_expectedNLCostPerHaPerCrop.append(SMOOTH(i_expectedNLCostPerHaPerCrop, 1, 1))
        expected_variable_cost.append(expectedVariableCostPerHaPerCrop(i_expectedLabourCostPerHaPerCrop, i_expectedNLCostPerHaPerCrop, i_croppingIntensity))

    return years_range, expected_variable_cost

  years_range, expected_variable_cost = compute_expected_variable_cost_over_years(i_expectedLabourCostPerHaPerCrop, i_expectedNLCostPerHaPerCrop, i_croppingIntensity, i_startyear, i_endyear)

#plotting the output
  fig = go.Figure()

  fig.add_trace(go.Scatter(
    x = years_range,
    y = expected_variable_cost,
    #text=[numerize.numerize(val) if val is not None else "N/A" for val in expected_revenue],
    textposition = 'top center',
    mode = 'lines+markers+text',  # this means it will show lines, markers (dots) and text
    marker_color = 'skyblue',
    line=dict(color = 'skyblue', width = 2)
    ))

  # Set chart's layout details
  fig.update_layout(
    title=dict(text='Expected variable cost per ha per crop Over the Years (RM/year)',x=0.35),
    xaxis_title="Year",
    yaxis_title="Expected variable cost per ha per crop (RM)"
    )

  # Display the plotly chart in Streamlit
  st.plotly_chart(fig, use_container_width=True)
