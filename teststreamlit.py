import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm

# Set the title of the entire Streamlit application
st.title("AB Test Calculator")

# Collect user inputs
control_visitors = st.number_input('Enter Control Visitors:', min_value=1)
control_conversions = st.number_input('Enter Control Conversions:', min_value=0)
experiment_visitors = st.number_input('Enter Experiment Visitors:', min_value=1)
experiment_conversions = st.number_input('Enter Experiment Conversions:', min_value=0)
confidence_level = st.slider('Select Confidence Level:', min_value=0, max_value=100, step=1, value=95)

# Check if all required inputs are provided
inputs_filled = control_visitors is not None and control_conversions is not None and \
                experiment_visitors is not None and experiment_conversions is not None and \
                confidence_level is not None

# Define function to perform AB test
def perform_ab_test(control_visitors, control_conversions, experiment_visitors, experiment_conversions, confidence_level):
    # Calculate conversion rates
    control_conversion_rate = control_conversions / control_visitors
    experiment_conversion_rate = experiment_conversions / experiment_visitors
    
    # Calculate the standard error
    standard_error = ((control_conversion_rate * (1 - control_conversion_rate)) / control_visitors +
                     (experiment_conversion_rate * (1 - experiment_conversion_rate)) / experiment_visitors) ** 0.5
    
    # Calculate the z-score
    z_score = (experiment_conversion_rate - control_conversion_rate) / standard_error
    
    # Determine the critical z-value for the given confidence level
    alpha = 1 - (confidence_level / 100)
    critical_z_value = norm.ppf(1 - alpha / 2)
    
    # Determine the result
    if abs(z_score) > critical_z_value:
        if z_score > 0:
            result = "Experiment Group is Better"
        else:
            result = "Control Group is Better"
    else:
        result = "Indeterminate"
    
    return result

# Create a button to calculate the AB test if all inputs are filled
if inputs_filled and st.button('Calculate'):
    result = perform_ab_test(control_visitors, control_conversions, experiment_visitors, experiment_conversions, confidence_level)
    st.write(f"AB Test Result: {result}")

# Show a warning message if inputs are not filled
if not inputs_filled:
    st.warning("Please fill in all the required input fields.")
