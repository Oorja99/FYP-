from matplotlib.colors import DivergingNorm
import streamlit as st
from bokeh.models.widgets import Div
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.

import pickle
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
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

# %matplotlib inline

pickle_in = open('classifier.pkl', 'rb') 
classifier = pickle.load(pickle_in)

def prediction(numberOfETFs,subtype,capacity,area): 
    if numberOfETFs == "Residential" and subtype =='Apartment':
        numberOfETFs=2
        subtype=5
    elif numberOfETFs == "Residential" and subtype =='Landed Property':
        numberOfETFs=2
        subtype=5
    elif numberOfETFs == "Commercial" and subtype =='Retail Mixed':
        numberOfETFs=1
        subtype=1
    elif numberOfETFs == "Commercial" and subtype =='Retail Non-Food':
        numberOfETFs=1
        subtype=3
    elif numberOfETFs == "Commercial" and subtype =='Office':
        numberOfETFs=1
        subtype=2
    elif numberOfETFs == "Industrial" and subtype =='Data Center':
        numberOfETFs=5
        subtype=13
    elif numberOfETFs == "Industrial" and subtype =='Manafacturing':
        numberOfETFs=5
        subtype=12
    elif numberOfETFs == "Institution" and subtype =='Airport':
        numberOfETFs=4
        subtype=9
    elif numberOfETFs == "Institution" and subtype =='Police Station':
        numberOfETFs=4
        subtype=10
    elif numberOfETFs == "Institution" and subtype =='Fire Station':
        numberOfETFs=4
        subtype=11
    elif numberOfETFs == "Educational" and subtype =='Nurseries':
        numberOfETFs=3
        subtype=7
    elif numberOfETFs == "Educational" and subtype =='University':
        numberOfETFs=3
        subtype=6
    elif numberOfETFs == "Educational" and subtype =='Student residences':
        numberOfETFs=3
        subtype=8
    elif numberOfETFs == "Storage" and subtype =='Warehouse':
        numberOfETFs=6
        subtype=14
    elif numberOfETFs == "Storage" and subtype =='Garage':
        numberOfETFs=6
        subtype=15
      
    prediction = classifier.predict([[numberOfETFs,subtype,capacity,area]])
    print(prediction)
    return prediction


#sidebar writings and tabs
st.markdown('<h2 style="background-color:MediumSeaGreen; text-align:center; font-family:arial;color:white">WASTE CALCULATOR</h2>', unsafe_allow_html=True)
img = Image.open('./download.jpeg')
st.image(img, width=700)
st.sidebar.title("Towards Zero Waste")
option = st.sidebar.selectbox("Service Selection", ('Waste Calculator','Insights','Geographical Analysis'))



if option == 'Waste Calculator':
    st.header("Welcome to our Waste Calculator! We provide **Visualizations** and **analytical waste data** for real estate developers to easily read and draw insights!")

    #STEP 1: get info
    st.header("Enter Building Information")

    numberOfETFs = st.selectbox('What is the type of building?',('Residential','Commercial','Institution','Industrial','Educational','Storage'))

    if numberOfETFs == 'Residential':
        subtype=st.selectbox('Residential Type', ('Apartment', 'Landed Property'))

    elif numberOfETFs == 'Commercial':
        subtype=st.selectbox('Commercial Type', ('Retail Mixed','Retail Non-Food', 'Office'))

    elif numberOfETFs == 'Institution':
        subtype=st.selectbox('Institution Type', ('Fire Station','Police Station', 'Airport'))

    elif numberOfETFs == 'Industrial':
        subtype=st.selectbox('Industrial Type', ('Data Center','Manufacturing'))

    elif numberOfETFs == 'Educational':
        subtype=st.selectbox('Purpose of Building', ('Nurseries', 'University','Student residences'))

    elif numberOfETFs == 'Storage':
        subtype=st.selectbox('Purpose of Building', ('Warehouse', 'Garage'))

    capacity = st.number_input('Building Capacity (Number of People)',)

    area = st.number_input('Ground Floor Area( In Square foot)',)

    if st.button("Predict"): 
        result = prediction(numberOfETFs, subtype, capacity,area) 
        st.success('Average amount of waste produced is in the category {}'.format(result))
        st.success("Go onto the next tab to gain more insights")


if option == 'Insights':
    st.header("*Get further insights into the waste you are likely to produce!*")
    typo = st.selectbox('What is the type of building?',('Select an option','Residential','Commercial','Institution','Industrial','Educational','Storage'))
    if typo == 'Residential':
        labels = 'Trash', 'Cardboard', 'Paper', 'Organic Waste', 'MGP', 'Textiles', 'E-Waste'
        sizes = [17,10,20,24,13,9,7]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig1)

        labels = 'Can be recycled', 'Non-Recyclable'
        sizes = [76,24]
        explode = (0.1, 0)  

        fig2, ax2 = plt.subplots()
        ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
        ax2.axis('equal') 

        st.pyplot(fig2)
        st.header("Upto 76 percent of your waste can be recycled!")
        st.title("ACT NOW!")

    if typo == 'Commercial':
        df = pd.read_csv("./Waste_Audit_Data_v4_EDITED.csv")
        st.title("Waste Generated by Commercial Buildings")
        st.markdown('The dashboard visualises the distribution of past waste generated and its occupancy by commercial building sub-types: Retail Mixed, Retail Non-Food, Office. This data is based in America.')
        st.sidebar.title("Visualisation Selector")
        select = st.sidebar.selectbox('Visualisation type:', ['Pie Chart - Distribution', 'Bar Chart - Waste & Occupancy'], key='1')
    
        # filter
        subset_data = df
        subtype_input = st.sidebar.multiselect(
        'Filter Building Sub-type:',
        df.groupby('SubType').count().reset_index()['SubType'].tolist())
        if len(subtype_input) > 0:
            subset_data = df[df['SubType'].isin(subtype_input)]

        # pie 
        if select == 'Pie Chart - Distribution':
            st.header("Distribution of Waste Generated between Sub-types")
            fig = px.pie(subset_data, values=subset_data['TotalWaste'], names=subset_data['SubType'], title='Total Waste Generated in KG')
            st.plotly_chart(fig)

        # bar
        if select=='Bar Chart - Waste & Occupancy':
            st.header("Waste Generation & Occupancy by Sub-types")
            fig = go.Figure(data=[
            go.Bar(name='TotalWaste', x=subset_data['SubType'], y=subset_data['TotalWaste']),
            go.Bar(name='Avg_Daily_Occupants', x=subset_data['SubType'], y=subset_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)
    

if option == 'Geographical Analysis':
    st.title("Geographic Analysis of waste collection centres")
    st.header("Welcome to our Visualisations regarding geographic analysis! We provide visualisations for users to find the closest waste collection points from the comfort of their homes!")

    visualisation_choice = st.selectbox('What is the type of visualisation you would like to see?',('Please select an option','Closest E-recycling bins','Closest 2nd hand good collection point'))

    if visualisation_choice == 'Closest E-recycling bins':
        #st.selectbox('Closest E-recycling bins', ('Closest 2nd hand good collection point'))
        js = "window.open('https://www.learngis2.maps.arcgis.com/home/item.html?id=1fcf5b2deeb34e78bc3df27a4c3c2502')"  # New tab or window
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)


    elif visualisation_choice == 'Closest 2nd hand good collection point':
        #st.selectbox('Closest 2nd hand good collection point', ('Closest E-recycling bins'))
        js = "window.open('https://www.learngis2.maps.arcgis.com/home/item.html?id=f3e86e2e5df14a36a12c17ddb463b6c2')"  # New tab or window
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)
