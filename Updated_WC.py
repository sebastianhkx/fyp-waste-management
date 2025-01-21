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
    df = pd.read_csv("./Waste_Audit_Fake_Data.csv")
    st.title("Waste Generated by Buildings")
    st.markdown('The dashboard visualises the distribution of past waste generated and its occupancy by building type. This data is based in America.' + ' Based on a total of ' + str(len(df.index)) + ' buildings.')
    st.markdown('Breakdown:')
    st.sidebar.title("Visualisation Selector")
    select = st.sidebar.selectbox('Visualisation type:', ['Pie Chart - Distribution', 'Bar Chart - Waste & Occupancy'], key='1')

    # filter by typology
    subset_data = df
    subset_input = st.sidebar.multiselect(
    'Filter Building Type:',
    df.groupby('Typology').count().reset_index()['Typology'].tolist())
    if len(subset_input) > 0:
        subset_data = df[df['Typology'].isin(subset_input)]
    #st.dataframe(subset_data)

    # breakdown numbers of selected building display
    if 'Commercial' in subset_data.values:
         st.markdown(str(df[df.Typology=='Commercial'].shape[0]) + ' Commercial buildings: ' + str(df[df.SubType=='Retail Non-Food'].shape[0]) + ' Non-Food Retails, ' + str(df[df.SubType=='Retail Mixed'].shape[0]) + ' Mixed Retails, and ' + str(df[df.SubType=='Office'].shape[0]) + ' Offices.')

    if 'Educational' in subset_data.values:
        st.markdown(str(df[df.Typology=='Educational'].shape[0]) + ' Educational buildings: ' + str(df[df.SubType=='Nurseries'].shape[0]) + ' Nurseries, ' + str(df[df.SubType=='Student residences'].shape[0]) + ' Student Residences, and ' + str(df[df.SubType=='University'].shape[0]) + ' Universities.')
    
    if 'Industrial' in subset_data.values:
        st.markdown(str(df[df.Typology=='Industrial'].shape[0]) + ' Industrial buildings: ' + str(df[df.SubType=='Manufacturing'].shape[0]) + ' Manufacturing Factories & ' + str(df[df.SubType=='Data Center'].shape[0]) + ' Data Centres.')
    
    if 'Institutional' in subset_data.values:
        st.markdown(str(df[df.Typology=='Institutional'].shape[0]) + ' Institutional buildings: ' + str(df[df.SubType=='Fire Station'].shape[0]) + ' Fire Stations, ' + str(df[df.SubType=='Police Station'].shape[0]) + ' Police Stations, and ' + str(df[df.SubType=='Airport'].shape[0]) + ' Airports.')
    
    if 'Residential' in subset_data.values:
        st.markdown(str(df[df.Typology=='Residential'].shape[0]) + ' Residential buildings: ' + str(df[df.SubType=='Apartment'].shape[0]) + ' Apartments & ' + str(df[df.SubType=='Landed Property'].shape[0]) + ' Landed Properties.')

    if 'Storage' in subset_data.values:
        st.markdown(str(df[df.Typology=='Storage'].shape[0]) + ' Storage buildings: ' + str(df[df.SubType=='Garage'].shape[0]) + ' Garages & ' + str(df[df.SubType=='Warehouse'].shape[0]) + ' Warehouses.')


    # chart display
    if 'Residential' in subset_data.values:
        # filter by subtype
        R_subtype_data = subset_data
        R_subtype_input = st.sidebar.multiselect(
        'Filter Building Sub-type:',
        R_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
        if len(R_subtype_input) > 0:
            R_subtype_data = subset_data[subset_data['SubType'].isin(R_subtype_input)]
        #st.dataframe(R_subtype_data)

        # bar
        if select == 'Bar Chart - Waste & Occupancy':
            st.header("Waste Generation & Occupancy by Sub-types")
            fig = go.Figure(data=[
            go.Bar(name='Avg Waste Produced in KG', x=R_subtype_data['SubType'], y=R_subtype_data['Audit_Avg']),
            go.Bar(name='Avg Daily Occupants', x=R_subtype_data['SubType'], y=R_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)

        # pie


    if 'Commercial' in subset_data.values:
        # filter by subtype
        C_subtype_data = subset_data
        C_subtype_input = st.sidebar.multiselect(
        'Filter Building Sub-type:',
        C_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
        if len(C_subtype_input) > 0:
            C_subtype_data = subset_data[subset_data['SubType'].isin(C_subtype_input)]
        #st.dataframe(subtype_data)
        
        # bar
        if select == 'Bar Chart - Waste & Occupancy':
            st.header("Waste Generation & Occupancy by Sub-types")
            #waste = sum(R_subtype_data['Audit_Avg'])
            #occupants = sum(R_subtype_data['Avg_Daily_Occupants'])
            #st.markdown('Based on ' + str(len(C_subtype_data.index)) + ' commercial buildings: ' + str(C_subtype_data[C_subtype_data.SubType=='Retail Non-Food'].shape[0]) + ' Non-Food Retails, ' + str(C_subtype_data[C_subtype_data.SubType=='Retail Mixed'].shape[0]) + ' Mixed Retails, and ' + str(C_subtype_data[C_subtype_data.SubType=='Office'].shape[0]) + ' Offices.')
            fig = go.Figure(data=[
            go.Bar(name='Avg Waste Produced in KG', x=C_subtype_data['SubType'], y=C_subtype_data['Audit_Avg']),
            go.Bar(name='Avg Daily Occupants', x=C_subtype_data['SubType'], y=C_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)
    
        # pie


    if 'Educational' in subset_data.values:
        # filter by subtype
        E_subtype_data = subset_data
        E_subtype_input = st.sidebar.multiselect(
        'Filter Building Sub-type:',
        E_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
        if len(E_subtype_input) > 0:
            E_subtype_data = subset_data[subset_data['SubType'].isin(E_subtype_input)]
        #st.dataframe(subtype_data)
        
        # bar
        if select == 'Bar Chart - Waste & Occupancy':
            st.header("Waste Generation & Occupancy by Sub-types")
            #st.markdown('Based on ' + str(len(E_subtype_data.index)) + ' educational buildings: ' + str(E_subtype_data[E_subtype_data.SubType=='Nurseries'].shape[0]) + ' Nurseries, ' + str(E_subtype_data[E_subtype_data.SubType=='Student residences'].shape[0]) + ' Student Residences, and ' + str(E_subtype_data[E_subtype_data.SubType=='University'].shape[0]) + ' Universities.')
            fig = go.Figure(data=[
            go.Bar(name='Waste Produced', x=E_subtype_data['SubType'], y=E_subtype_data['Audit_Avg']),
            go.Bar(name='Daily Occupants', x=E_subtype_data['SubType'], y=E_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)

        # pie 


    if 'Industrial' in subset_data.values:
        # filter by subtype
        Ind_subtype_data = subset_data
        Ind_subtype_input = st.sidebar.multiselect(
        'Filter Building Sub-type:',
        Ind_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
        if len(Ind_subtype_input) > 0:
            Ind_subtype_data = subset_data[subset_data['SubType'].isin(Ind_subtype_input)]
        #st.dataframe(subtype_data)
        
        # bar
        if select == 'Bar Chart - Waste & Occupancy':
            st.header("Waste Generation & Occupancy by Sub-types")
            #st.markdown('Based on ' + str(len(Ind_subtype_data.index)) + ' industrial buildings: ' + str(Ind_subtype_data[Ind_subtype_data.SubType=='Manufacturing'].shape[0]) + ' Manufacturing Factories & ' + str(Ind_subtype_data[Ind_subtype_data.SubType=='Data Center'].shape[0]) + ' Data Centres.')
            fig = go.Figure(data=[
            go.Bar(name='Waste Produced', x=Ind_subtype_data['SubType'], y=Ind_subtype_data['Audit_Avg']),
            go.Bar(name='Daily Occupants', x=Ind_subtype_data['SubType'], y=Ind_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)
        #pie


    if 'Institutional' in subset_data.values:
        # filter by subtype
        Ins_subtype_data = subset_data
        Ins_subtype_input = st.sidebar.multiselect(
        'Filter Building Sub-type:',
        Ins_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
        if len(Ins_subtype_input) > 0:
            Ins_subtype_data = subset_data[subset_data['SubType'].isin(Ins_subtype_input)]
        #st.dataframe(subtype_data)
        
        # bar
        if select == 'Bar Chart - Waste & Occupancy':
            st.header("Waste Generation & Occupancy by Sub-types")
            #st.markdown('Based on ' + str(len(Ins_subtype_data.index)) + ' institutional buildings: ' + str(Ins_subtype_data[Ins_subtype_data.SubType=='Fire Station'].shape[0]) + ' Fire Stations, ' + str(Ins_subtype_data[Ins_subtype_data.SubType=='Police Station'].shape[0]) + ' Police Stations, and ' + str(Ins_subtype_data[Ins_subtype_data.SubType=='Airport'].shape[0]) + ' Airports.')
            fig = go.Figure(data=[
            go.Bar(name='Waste Produced', x=Ins_subtype_data['SubType'], y=Ins_subtype_data['Audit_Avg']),
            go.Bar(name='Daily Occupants', x=Ins_subtype_data['SubType'], y=Ins_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)

        #pie


    if 'Storage' in subset_data.values:
        # filter by subtype
        S_subtype_data = subset_data
        S_subtype_input = st.sidebar.multiselect(
        'Filter Building Sub-type:',
        S_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
        if len(S_subtype_input) > 0:
            S_subtype_data = subset_data[subset_data['SubType'].isin(S_subtype_input)]
        #st.dataframe(subtype_data)
        
        # bar
        if select == 'Bar Chart - Waste & Occupancy':
            st.header("Waste Generation & Occupancy by Sub-types")
            #st.markdown('Based on ' + str(len(S_subtype_data.index)) + ' storage buildings: ' + str(S_subtype_data[S_subtype_data.SubType=='Garage'].shape[0]) + ' Garages & ' + str(S_subtype_data[S_subtype_data.SubType=='Warehouse'].shape[0]) + ' Warehouses.')
            fig = go.Figure(data=[
            go.Bar(name='Waste Produced', x=S_subtype_data['SubType'], y=S_subtype_data['Audit_Avg']),
            go.Bar(name='Daily Occupants', x=S_subtype_data['SubType'], y=S_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)

        #pie

    

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
