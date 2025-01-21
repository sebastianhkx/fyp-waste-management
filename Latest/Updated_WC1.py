from matplotlib.colors import DivergingNorm
import streamlit as st
from bokeh.models.widgets import Div

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

pickle_in = open('classifier2.pkl', 'rb') 
classifier = pickle.load(pickle_in)

def prediction(numberOfETFs,subtype,capacity,area): 
    if numberOfETFs == "Residential" and subtype =='Apartment':
        numberOfETFs=2
        subtype=5
    elif numberOfETFs == "Residential" and subtype =='Landed Property':
        numberOfETFs=2
        subtype=4
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
    elif numberOfETFs == "Institutional" and subtype =='Airport':
        numberOfETFs=4
        subtype=9
    elif numberOfETFs == "Institutional" and subtype =='Police Station':
        numberOfETFs=4
        subtype=10
    elif numberOfETFs == "Institutional" and subtype =='Fire Station':
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


st.sidebar.title("Towards Zero Waste")
option = st.sidebar.selectbox("Service Selection", ('Select a service','Add to Database','Waste Calculator','Insights','Geographical Analysis'))

if option == 'Select a service':
    img = Image.open('./download.jpeg')
    st.image(img, width=700)
    original_title = '<p style="background-color:Green; font-family:Courier; text-align:center; color:white; font-size: 30px;">WASTE CALCULATOR AND DISPOSAL STRATEGIES</p>'
    st.markdown(original_title, unsafe_allow_html=True) 
    original_title = '<p style="font-family:Courier; text-align:center; color:Green; font-size: 20px;">The first step towards making the world a greener place</p>'
    st.markdown(original_title, unsafe_allow_html=True) 

if option == 'Waste Calculator':
    img3 = Image.open('./waste.jpg')
    st.image(img3, width=700)
    original_title = '<p style="background-color:CadetBlue; font-family:Courier; text-align:center; color:White; font-size: 30px;">WASTE CALCULATOR</p>'
    st.markdown(original_title, unsafe_allow_html=True) 
    original_title = '<p style="font-family:Courier; text-align:center; color:CadetBlue; font-size: 20px;">We provide Visualizations and Analytical results for real estate developers to easily read and draw insights!</p>'
    st.markdown(original_title, unsafe_allow_html=True)

    #STEP 1: get info
    st.header("Enter Building Information")

    numberOfETFs = st.selectbox('What is the type of building?',('Residential','Commercial','Institutional','Industrial','Educational','Storage'))

    if numberOfETFs == 'Residential':
        subtype=st.selectbox('Residential Type', ('Apartment', 'Landed Property'))

    elif numberOfETFs == 'Commercial':
        subtype=st.selectbox('Commercial Type', ('Retail Mixed','Retail Non-Food', 'Office'))

    elif numberOfETFs == 'Institutional':
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
    img4 = Image.open('./bulb.png')
    st.image(img4, width=700)
    original_title = '<p style="background-color:LightCyan; font-family:Courier; text-align:center; color:DarkBlue; font-size: 30px;">VISUALISATIONS AND STRATEGIES FOR WASTE MANAGEMENT</p>'
    st.markdown(original_title, unsafe_allow_html=True) 
    original_title = '<p style="font-family:Courier; text-align:center; color:DarkBlue; font-size: 20px;">Get further insights into the waste you are likely to produce!</p>'
    st.markdown(original_title, unsafe_allow_html=True)

    df = pd.read_csv("./Waste_Audit_Data.csv")
    st.markdown('The dashboard visualises the distribution of past waste generated and its occupancy by building type. This data is based in America.' + ' Based on a total of ' + str(len(df.index)) + ' buildings.')
    st.markdown('Breakdown:')
    st.sidebar.title("Visualisation Selector")

    # filter by typology
    subset_data = df
    subset_input = st.sidebar.multiselect(
    'Filter Building Type:',
    df.groupby('Typology').count().reset_index()['Typology'].tolist())
    if len(subset_input) > 0:
        subset_data = df[df['Typology'].isin(subset_input)]
    #st.dataframe(subset_data)

    select = st.sidebar.selectbox('Visualisation type:', ['Select a visualisation','Pie Chart - Distribution', 'Bar Chart - Waste & Occupancy'])

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

    if 'Residential' in subset_data.values:
        # bar
        if select == 'Bar Chart - Waste & Occupancy':

            R_subtype_data = subset_data
            R_subtype_input = st.sidebar.multiselect('Filter Residential Sub-type:',
            R_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
            if len(R_subtype_input) > 0:
                R_subtype_data = subset_data[subset_data['SubType'].isin(R_subtype_input)]

            st.header("Waste Generation & Occupancy by Sub-types")
            fig = go.Figure(data=[
            go.Bar(name='Avg Waste Produced in KG', x=R_subtype_data['SubType'], y=R_subtype_data['Audit_Avg']),
            go.Bar(name='Avg Daily Occupants', x=R_subtype_data['SubType'], y=R_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)

        # pie
        if select == 'Pie Chart - Distribution':
            labels = 'Trash', 'Cardboard', 'Paper', 'Organic Waste', 'Textiles', 'E-Waste'
            sizes = [17,12,20,34,10,7]
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

        #Recommendations    
        if 'Residential' in subset_data.values:
            st.info("Recyclable wastes should be disposed to nearby recycle bins. For HDB estates, commingled blue recycling bins are placed at open areas that are convenient and accessible to the residents. Cardboard and paper as well as textiles are recyclable, you are recommended to keep them dry and dispose them in the local blue-colored recycle bins. For metal(cans) and plastic waste, you should rinse the them with clean water, crush the can/bottle, and then separate them from wet waste and dispose in nearby recycle bins.")
            if st.button('Find the nearest recycle bin'):
                js = "window.open('http://storage.googleapis.com/fyp-e-recycling-bins/index.html')"  # New tab or window
                js = "window.location.href = 'http://storage.googleapis.com/fyp-e-recycling-bins/index.html'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)

            st.info("These are the wastes that come from our kitchen and it includes food remains, garden waste, etc. Biodegradable waste is also known as wet/moist waste. This can be composted to obtain manure. Biodegradable wastes decompose themselves over a period of time depending on the material. You are recommended to dispose them in a green colored dustbin in your neighborhood. If you have a garden, you may choose to compost them.")
            st.info("As an individual or as part of a household, you are encouraged to make use of e-waste recycling programmes voluntarily offered by industry stakeholders. Simply drop off your e-waste at the nearby recycling points to properly recycle your e-waste. ")

            if st.button('Get more info on E-waste'):
                js = "window.open('https://www.nea.gov.sg/our-services/waste-management/3r-programmes-and-resources/e-waste-management/where-to-recycle-e-waste')"  # New tab or window
                js = "window.location.href = 'https://www.nea.gov.sg/our-services/waste-management/3r-programmes-and-resources/e-waste-management/where-to-recycle-e-waste'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)


    if 'Commercial' in subset_data.values:
        if select == 'Bar Chart - Waste & Occupancy':

            C_subtype_data = subset_data
            C_subtype_input = st.sidebar.multiselect('Filter Commercial Sub-type:',
            C_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
            if len(C_subtype_input) > 0:
                C_subtype_data = subset_data[subset_data['SubType'].isin(C_subtype_input)]
            #st.dataframe(subtype_data)
        
        # bar
        
            st.header("Waste Generation & Occupancy by Sub-types")
            #waste = sum(R_subtype_data['Audit_Avg'])
            #occupants = sum(R_subtype_data['Avg_Daily_Occupants'])
            #st.markdown('Based on ' + str(len(C_subtype_data.index)) + ' commercial buildings: ' + str(C_subtype_data[C_subtype_data.SubType=='Retail Non-Food'].shape[0]) + ' Non-Food Retails, ' + str(C_subtype_data[C_subtype_data.SubType=='Retail Mixed'].shape[0]) + ' Mixed Retails, and ' + str(C_subtype_data[C_subtype_data.SubType=='Office'].shape[0]) + ' Offices.')
            fig = go.Figure(data=[
            go.Bar(name='Avg Waste Produced in KG', x=C_subtype_data['SubType'], y=C_subtype_data['Audit_Avg']),
            go.Bar(name='Avg Daily Occupants', x=C_subtype_data['SubType'], y=C_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)
    
        # pie
        if select == 'Pie Chart - Distribution':
            labels = 'Food Waste', 'Paper', 'Plastic', 'Textiles', 'Metal', 'Glass'
            sizes = [24,32,20,10,10,4]
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%',startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)

            labels = 'Can be recycled', 'Non-Recyclable'
            sizes = [76,24]
            explode = (0, 0.2)  

            fig2, ax2 = plt.subplots()
            ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
            ax2.axis('equal') 

            st.pyplot(fig2)
            st.header("Upto 76 percent of your waste can be recycled!")

            #Recommendations  
            st.info("A large portion of commercial waste is recyclable. For users with moderate Waste Production or above, you are recommended to contact a professional waste disposal service provider. Cardboard and paper as well as textiles are recyclable, you are recommended to keep them dry and dispose them in the local blue-colored recycle bins. For metal(cans) and plastic waste, you should rinse the them with clean water, crush the can/bottle, and then separate them from wet waste and dispose in nearby recycle bins.")
            st.info("Recyclable wastes should be disposed to nearby recycle bins. Commingled blue recycling bins are placed at open areas that are convenient and accessible to the residents. Cardboard and paper as well as textiles are recyclable, you are recommended to keep them dry and dispose them in the local blue-colored recycle bins. For metal(cans) and plastic waste, you should rinse the them with clean water, crush the can/bottle, and then separate them from wet waste and dispose in nearby recycle bins.")
            if st.button('Find the nearest recycle bin'):
                js = "window.open('http://storage.googleapis.com/fyp-e-recycling-bins/index.html')"  # New tab or window
                js = "window.location.href = 'http://storage.googleapis.com/fyp-e-recycling-bins/index.html'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)
            st.info("If you have large quantities of waste generated according to the waste calculator, please contact your local waste handler provider")

            if st.button('Find your waste management provider'):
                js = "window.open('https://www.nea.gov.sg/our-services/waste-management/waste-collection-systems')"  # New tab or window
                js = "window.location.href = 'https://www.nea.gov.sg/our-services/waste-management/waste-collection-systems'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)


    if 'Educational' in subset_data.values:
        # bar
        if select == 'Bar Chart - Waste & Occupancy':
        # filter by subtype
            E_subtype_data = subset_data
            E_subtype_input = st.sidebar.multiselect('Filter Educational Sub-type:',
            E_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
            if len(E_subtype_input) > 0:
                E_subtype_data = subset_data[subset_data['SubType'].isin(E_subtype_input)]
            #st.dataframe(subtype_data)
        
        
            st.header("Waste Generation & Occupancy by Sub-types")
            #st.markdown('Based on ' + str(len(E_subtype_data.index)) + ' educational buildings: ' + str(E_subtype_data[E_subtype_data.SubType=='Nurseries'].shape[0]) + ' Nurseries, ' + str(E_subtype_data[E_subtype_data.SubType=='Student residences'].shape[0]) + ' Student Residences, and ' + str(E_subtype_data[E_subtype_data.SubType=='University'].shape[0]) + ' Universities.')
            fig = go.Figure(data=[
            go.Bar(name='Waste Produced', x=E_subtype_data['SubType'], y=E_subtype_data['Audit_Avg']),
            go.Bar(name='Daily Occupants', x=E_subtype_data['SubType'], y=E_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)

        # pie 
        if select == 'Pie Chart - Distribution':
            labels = 'Food Waste', 'Paper', 'Plastic', 'Textiles', 'Metal', 'Glass'
            sizes = [24,32,20,10,10,4]
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%',startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)

            labels = 'Can be recycled', 'Non-Recyclable'
            sizes = [76,24]
            explode = (0, 0.2)  

            fig2, ax2 = plt.subplots()
            ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
            ax2.axis('equal') 

            st.pyplot(fig2)
            st.header("Upto 76 percent of your waste can be recycled!")

            #Recommendations  
            st.info("A large portion of waste produced in education facilities is recyclable. For users with moderate Waste Production or above, you are recommended to contact a professional waste disposal service provider. Cardboard and paper as well as textiles are recyclable, you are recommended to keep them dry and dispose them in the local blue-colored recycle bins. For metal(cans) and plastic waste, you should rinse the them with clean water, crush the can/bottle, and then separate them from wet waste and dispose in nearby recycle bins.")
            st.info("Recyclable wastes should be disposed to nearby recycle bins. Commingled blue recycling bins are placed at open areas that are convenient and accessible to the residents. Cardboard and paper as well as textiles are recyclable, you are recommended to keep them dry and dispose them in the local blue-colored recycle bins. For metal(cans) and plastic waste, you should rinse the them with clean water, crush the can/bottle, and then separate them from wet waste and dispose in nearby recycle bins.")
            if st.button('Find the nearest recycle bin'):
                js = "window.open('http://storage.googleapis.com/fyp-e-recycling-bins/index.html')"  # New tab or window
                js = "window.location.href = 'http://storage.googleapis.com/fyp-e-recycling-bins/index.html'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)
            st.info("If you have large quantities of waste generated according to the waste calculator, please contact your local waste handler provider")

            if st.button('Find your waste management provider'):
                js = "window.open('https://www.nea.gov.sg/our-services/waste-management/waste-collection-systems')"  # New tab or window
                js = "window.location.href = 'https://www.nea.gov.sg/our-services/waste-management/waste-collection-systems'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)


    if 'Industrial' in subset_data.values:
        # bar
        if select == 'Bar Chart - Waste & Occupancy':
        # filter by subtype
            Ind_subtype_data = subset_data
            Ind_subtype_input = st.sidebar.multiselect('Filter Industrial Sub-type:',
            Ind_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
            if len(Ind_subtype_input) > 0:
                Ind_subtype_data = subset_data[subset_data['SubType'].isin(Ind_subtype_input)]
            #st.dataframe(subtype_data)
        
       
            st.header("Waste Generation & Occupancy by Sub-types")
            #st.markdown('Based on ' + str(len(Ind_subtype_data.index)) + ' industrial buildings: ' + str(Ind_subtype_data[Ind_subtype_data.SubType=='Manufacturing'].shape[0]) + ' Manufacturing Factories & ' + str(Ind_subtype_data[Ind_subtype_data.SubType=='Data Center'].shape[0]) + ' Data Centres.')
            fig = go.Figure(data=[
            go.Bar(name='Waste Produced', x=Ind_subtype_data['SubType'], y=Ind_subtype_data['Audit_Avg']),
            go.Bar(name='Daily Occupants', x=Ind_subtype_data['SubType'], y=Ind_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)
         # pie 
        if select == 'Pie Chart - Distribution':
            st.info("The composition of industrial waste varies greatly with the production, thus the below chart is merely a reference.")
            labels = 'Liquid waste', 'Solid waste', 'Emissions'
            sizes = [48, 40, 12]
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%',startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)

            #Recommendations  
            st.info("For industrial waste, you are recommended to contact professional waste disposal providers. Waste water and exhaust should be treated so that they are within environmental regulations before releasing. Solid waste should be handle by professional waste disposal service providers.")
            st.info("A large portion of commercial waste is recyclable. For users with moderate Waste Production or above, you are recommended to contact a professional waste disposal service provider. Cardboard and paper as well as textiles are recyclable, you are recommended to keep them dry and dispose them in the local blue-colored recycle bins. For metal(cans) and plastic waste, you should rinse the them with clean water, crush the can/bottle, and then separate them from wet waste and dispose in nearby recycle bins.")
            if st.button('Find your waste management provider'):
                js = "window.open('https://www.nea.gov.sg/our-services/waste-management/waste-collection-systems')"  # New tab or window
                js = "window.location.href = 'https://www.nea.gov.sg/our-services/waste-management/waste-collection-systems'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)
            
            st.header("For more information on environmental guidelines for new industrial developments, please click the button below.")
            if st.button('Find your industrial waste management solution'):
                js = "window.open('https://www.nea.gov.sg/docs/default-source/our-services/building-planning/guide-on-environmental-requirements-for-industrial-and-non-industrial-developments.pdf)"
                js = "window.location.href = 'https://www.nea.gov.sg/docs/default-source/our-services/building-planning/guide-on-environmental-requirements-for-industrial-and-non-industrial-developments.pdf'"
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)


    if 'Institutional' in subset_data.values:
        # bar
        if select == 'Bar Chart - Waste & Occupancy':
        # filter by subtype
            Ins_subtype_data = subset_data
            Ins_subtype_input = st.sidebar.multiselect('Filter Institutional Sub-type:',
            Ins_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
            if len(Ins_subtype_input) > 0:
                Ins_subtype_data = subset_data[subset_data['SubType'].isin(Ins_subtype_input)]
        #st.dataframe(subtype_data)
        
            st.header("Waste Generation & Occupancy by Sub-types")
            #st.markdown('Based on ' + str(len(Ins_subtype_data.index)) + ' institutional buildings: ' + str(Ins_subtype_data[Ins_subtype_data.SubType=='Fire Station'].shape[0]) + ' Fire Stations, ' + str(Ins_subtype_data[Ins_subtype_data.SubType=='Police Station'].shape[0]) + ' Police Stations, and ' + str(Ins_subtype_data[Ins_subtype_data.SubType=='Airport'].shape[0]) + ' Airports.')
            fig = go.Figure(data=[
            go.Bar(name='Waste Produced', x=Ins_subtype_data['SubType'], y=Ins_subtype_data['Audit_Avg']),
            go.Bar(name='Daily Occupants', x=Ins_subtype_data['SubType'], y=Ins_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)

        #pie
        if select == 'Pie Chart - Distribution':
            labels = 'Food Waste', 'Paper', 'Plastic', 'Textiles', 'Metal', 'Glass'
            sizes = [24,32,20,10,10,4]
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%',startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)

            labels = 'Can be recycled', 'Non-Recyclable'
            sizes = [76,24]
            explode = (0, 0.2)  

            fig2, ax2 = plt.subplots()
            ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
            ax2.axis('equal') 

            st.pyplot(fig2)
            st.header("Upto 76 percent of your waste can be recycled!")

            #Recommendations  
            st.info("A large portion of waste produced in institutional facilities is recyclable. For users with moderate Waste Production or above, you are recommended to contact a professional waste disposal service provider. Cardboard and paper as well as textiles are recyclable, you are recommended to keep them dry and dispose them in the local blue-colored recycle bins. For metal(cans) and plastic waste, you should rinse the them with clean water, crush the can/bottle, and then separate them from wet waste and dispose in nearby recycle bins.")
            st.info("Recyclable wastes should be disposed to nearby recycle bins. Commingled blue recycling bins are placed at open areas that are convenient and accessible to the residents. Cardboard and paper as well as textiles are recyclable, you are recommended to keep them dry and dispose them in the local blue-colored recycle bins. For metal(cans) and plastic waste, you should rinse the them with clean water, crush the can/bottle, and then separate them from wet waste and dispose in nearby recycle bins.")
            if st.button('Find the nearest recycle bin'):
                js = "window.open('http://storage.googleapis.com/fyp-e-recycling-bins/index.html')"  # New tab or window
                js = "window.location.href = 'http://storage.googleapis.com/fyp-e-recycling-bins/index.html'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)
            st.info("If you have large quantities of waste generated according to the waste calculator, please contact your local waste handler provider")

            if st.button('Find your waste management provider'):
                js = "window.open('https://www.nea.gov.sg/our-services/waste-management/waste-collection-systems')"  # New tab or window
                js = "window.location.href = 'https://www.nea.gov.sg/our-services/waste-management/waste-collection-systems'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)


    if 'Storage' in subset_data.values:
         # bar
        if select == 'Bar Chart - Waste & Occupancy':
        # filter by subtype
            S_subtype_data = subset_data
            S_subtype_input = st.sidebar.multiselect('Filter Storage Sub-type:',
            S_subtype_data.groupby('SubType').count().reset_index()['SubType'].tolist())
            if len(S_subtype_input) > 0:
                S_subtype_data = subset_data[subset_data['SubType'].isin(S_subtype_input)]
            #st.dataframe(subtype_data)
        
       
            st.header("Waste Generation & Occupancy by Sub-types")
            #st.markdown('Based on ' + str(len(S_subtype_data.index)) + ' storage buildings: ' + str(S_subtype_data[S_subtype_data.SubType=='Garage'].shape[0]) + ' Garages & ' + str(S_subtype_data[S_subtype_data.SubType=='Warehouse'].shape[0]) + ' Warehouses.')
            fig = go.Figure(data=[
            go.Bar(name='Waste Produced', x=S_subtype_data['SubType'], y=S_subtype_data['Audit_Avg']),
            go.Bar(name='Daily Occupants', x=S_subtype_data['SubType'], y=S_subtype_data['Avg_Daily_Occupants'])])
            st.plotly_chart(fig)

        #pie
        if select == 'Pie Chart - Distribution':
            labels = 'Paper', 'Plastic', 'Textiles', 'Metal'
            sizes = [40,32,14,14]
            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, labels=labels, autopct='%1.1f%%',startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)

            st.header("Stroage facilities waste are mainly generated from item packaging")
            st.header("Up to 100 percent of your waste can be recycled!")

            #Recommendations  
            st.info("A large portion of waste produced in storage facilities is recyclable. For users with moderate Waste Production or above, you are recommended to contact a professional waste disposal service provider. Cardboard and paper as well as textiles are recyclable, you are recommended to keep them dry and dispose them in the local blue-colored recycle bins. For metal(cans) and plastic waste, you should rinse the them with clean water, crush the can/bottle, and then separate them from wet waste and dispose in nearby recycle bins.")
            st.info("Recyclable wastes should be disposed to nearby recycle bins. Commingled blue recycling bins are placed at open areas that are convenient and accessible to the residents. Cardboard and paper as well as textiles are recyclable, you are recommended to keep them dry and dispose them in the local blue-colored recycle bins. For metal(cans) and plastic waste, you should rinse the them with clean water, crush the can/bottle, and then separate them from wet waste and dispose in nearby recycle bins.")
            if st.button('Find the nearest recycle bin'):
                js = "window.open('http://storage.googleapis.com/fyp-e-recycling-bins/index.html')"  # New tab or window
                js = "window.location.href = 'http://storage.googleapis.com/fyp-e-recycling-bins/index.html'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)
            st.info("If you have large quantities of waste generated according to the waste calculator, please contact your local waste handler provider")

            if st.button('Find your waste management provider'):
                js = "window.open('https://www.nea.gov.sg/our-services/waste-management/waste-collection-systems')"  # New tab or window
                js = "window.location.href = 'https://www.nea.gov.sg/our-services/waste-management/waste-collection-systems'"  # Current tab
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)


if option == 'Geographical Analysis':
    img4 = Image.open('./navigate.jpg')
    st.image(img4, width=700)
    original_title = '<p style="background-color:LightGreen; font-family:Courier; text-align:center; color:Black; font-size: 30px;">GEOGRAPHICAL ANALYSIS OF WASTE COLLECTION CENTRES</p>'
    st.markdown(original_title, unsafe_allow_html=True) 
    original_title = '<p style="font-family:Courier; text-align:center; color:Black; font-size: 20px;">We provide visualisations for users to find the closest waste collection points from the comfort of their homes!</p>'
    st.markdown(original_title, unsafe_allow_html=True)

    visualisation_choice = st.selectbox('What is the type of visualisation you would like to see?',('Please select an option','Closest E-recycling bins','Closest 2nd hand good collection point'))

    if visualisation_choice == 'Closest E-recycling bins':
        #st.selectbox('Closest E-recycling bins', ('Closest 2nd hand good collection point'))
        js = "window.open('http://storage.googleapis.com/fyp-e-recycling-bins/index.html')"  # New tab or window
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)


    elif visualisation_choice == 'Closest 2nd hand good collection point':
        #st.selectbox('Closest 2nd hand good collection point', ('Closest E-recycling bins'))
        js = "window.open('http://storage.googleapis.com/fyp-2nd-hands-goods-collection/index.html')"  # New tab or window
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)

if option =='Add to Database':
    img2 = Image.open('./contribute.png')
    st.image(img2, width=700)
    original_title = '<p style="background-color:BurlyWood; font-family:Courier; text-align:center; color:Brown; font-size: 30px;">CONTRIBUTE TO OUR CAUSE!</p>'
    st.markdown(original_title, unsafe_allow_html=True) 
    original_title = '<p style="font-family:Courier; text-align:center; color:Brown; font-size: 20px;">Help us improve our accuracy by sharing your data! We promise to keep it safe. </p>'
    st.markdown(original_title, unsafe_allow_html=True)
    # save annotated results after every button click
    def save_results(results_df,button_press,type_input, subtype_input, capacity_input, area_input,waste_input):
        results_df.at[button_press, 'Typology'] = type_input
        results_df.at[button_press, 'Sub-Type'] = subtype_input
        results_df.at[button_press, 'GFA'] = area_input
        results_df.at[button_press, 'Est. Average Daily Occupancy (Continuous Basis)'] = capacity_input
        results_df.at[button_press, 'audit_avg'] = waste_input
        results_df.to_csv('Final_data.csv', index=None)
        return None

    # load spreadsheet with data to be annotated
    @st.cache(allow_output_mutation=True)
    def load_data():
        # If this is your first run, create an empty csv file with
        # columns kms_biked and location_visited
        df = pd.read_csv('Final_data.csv')
        return df


    results_df = load_data()

    # track which row of results_df to read
    with open("progress.txt", "r") as f:
            button_press = f.readline()  # starts as a string
            button_press = 0 if button_press == "" else int(button_press)  # check if its an empty string, otherwise should be able to cast using int()

    #ENTER INPUTS
    type_input = st.selectbox('What is the type of building?',('Residential','Commercial','Institutional','Industrial','Educational','Storage'))
    if type_input == 'Residential':
        subtype_input=st.selectbox('Residential Type', ('Apartment', 'Landed Property'))

    elif type_input == 'Commercial':
        subtype_input=st.selectbox('Commercial Type', ('Retail Mixed','Retail Non-Food', 'Office'))

    elif type_input == 'Institutional':
        subtype_input=st.selectbox('Institution Type', ('Fire Station','Police Station', 'Airport'))

    elif type_input == 'Industrial':
        subtype_input=st.selectbox('Industrial Type', ('Data Center','Manufacturing'))

    elif type_input == 'Educational':
        subtype_input=st.selectbox('Purpose of Building', ('Nurseries', 'University','Student residences'))

    elif type_input == 'Storage':
        subtype_input=st.selectbox('Purpose of Building', ('Warehouse', 'Garage'))

    capacity_input = st.number_input('What is the average Building Capacity (Number of People)?',)

    area_input = st.number_input('What is the average Ground Floor Area( In Square foot)?',)

    waste_input = st.number_input('What is the average waste produced daily (In Kilograms)?',)

    if st.button("Add to database!"):
        st.success("Information added to database")
        button_press += 1
        save_results(results_df, button_press, type_input, subtype_input, capacity_input, area_input,waste_input)

    # track which row of results_df to write to
    with open("progress.txt", "w") as f:
            f.truncate()
            f.write(f"{button_press}")