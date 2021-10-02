import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.

import altair as alt
from altair.expr import datum
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm
from tabulate import tabulate
import seaborn as sns

# %matplotlib inline

#sidebar writings and tabs
st.sidebar.title("Towards Zero Waste")
option = st.sidebar.selectbox("Service Selection", ('Waste Calculator','Waste Disposal Strategies','Geographical Analysis'))



if option == 'Waste Calculator':
    st.title("Waste Overview and Calculations")
    st.header("Welcome to our Waste Calculator! We provide **Visualizations** and **analytical waste data** for real estate developers to easily read and draw insights!")

    #STEP 1: get info
    st.header("Enter Building Information")

    numberOfETFs = st.selectbox('What is the type of building?',('Residential','Commercial','Institution','Industrial','Others'))

    if numberOfETFs == 'Residential':
        st.selectbox('Residential Type', ('HDB Housing','Condominium', 'Private Apartment', 'Landed Property'))

    elif numberOfETFs == 'Commercial':
        st.selectbox('Commercial Type', ('Bank','Office Building', 'Shopping Complex', 'Hotel', 'Supermarket'))

    elif numberOfETFs == 'Institution':
        st.selectbox('Institution Type', ('Fire Station','Police Station', 'Dormitory', 'Prison', 'Library', 'School'))

    elif numberOfETFs == 'Industrial':
        st.selectbox('Industrial Type', ('Refineries','Fertilizer Plant', 'Warehouse', 'Power Station', 'Light Manufacturing', 'Heavy Manufacturing'))

    elif numberOfETFs == 'Others':
        st.selectbox('Purpose of Building', ('Stadium', 'Carpark'))

    capacity = st.text_input('Building Capacity (Number of People)',)

    units = st.text_input('Number of Units',)

    
    if units != '' : 

        st.header("*Waste Calculations and Visualizations*")

        fig = plt.figure(figsize =(13, 10))
        allocation = (0.2, 0.3, 0.1,0.12,0.12,0.02,0.25)
        waste_breakdown = ('metal', 'plastic', 'paper', 'Organic Waste', 'Hazardous Waste', 'Recyclable Rubbish', 'Liquid Waste')
        plt.pie(allocation, labels = waste_breakdown, autopct='%1.1f%%')
        plt.legend()
        st.pyplot(fig)

