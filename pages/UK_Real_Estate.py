import pandas as pd
import streamlit as st
from openbb_terminal.sdk import openbb
import plotly.graph_objects as go
import datetime


st.title('openbb.alt.realestate')


col1, col2 = st.columns(2)

startdate = col1.date_input(
    "Start Date ",
    datetime.date(2012, 1, 1))

enddate = col2.date_input(
    "End Date ",
    datetime.date(2023, 1, 1))

kent_data = pd.DataFrame()
gravesham_data = pd.DataFrame()
dartford_data = pd.DataFrame()
ashford_data = pd.DataFrame()
swale_data = pd.DataFrame()
london_data = pd.DataFrame()
england_data = pd.DataFrame()

selector = st.selectbox(
        'Plot',
        ('HPI','Average Price','Average Price Cash','Total Sales Volume','Avg Price Existing Property','Avg Price First Time Buyer','Avg Price Detached'))
column = 'hpi'
if selector == 'Average Price':
    column = 'avgPrice'
elif selector == 'Average Price Cash':
    column = 'avgPriceCash'
elif selector == 'Total Sales Volume':
    column = 'totalSalesVolume'
elif selector == 'Avg Price Existing Property':
    column = 'avgPriceExistingProperty'
elif selector == 'Avg Price First Time Buyer':
    column = 'avgPriceFirstTimeBuyer'
elif selector == 'Avg Price Detached':
    column = 'avgPriceDetached'

col1, col2, col3, col4 = st.columns(4)
kent_checkbox = col1.checkbox('Kent')
london_checkbox = col2.checkbox('London')
england_checkbox = col3.checkbox('England')
swale_checkbox = col1.checkbox('Swale')
gravesham_checkbox = col2.checkbox('Gravesham')
dartford_checkbox = col3.checkbox('Dartford')
ashford_checkbox = col4.checkbox('Ashford')




fig = go.Figure()
if kent_checkbox:
    kent_data = openbb.alt.realestate.get_region_stats('kent',  startdate, enddate)
    fig = fig.add_trace(go.Scatter(x=kent_data["month"], y=kent_data[column], name='Kent'))
if gravesham_checkbox:
    gravesham_data = openbb.alt.realestate.get_region_stats('gravesham',  startdate, enddate)
    fig = fig.add_trace(go.Scatter(x=gravesham_data["month"], y=gravesham_data[column], name='Gravesham'))
if dartford_checkbox:
    dartford_data = openbb.alt.realestate.get_region_stats('dartford',  startdate, enddate)
    fig = fig.add_trace(go.Scatter(x=dartford_data["month"], y=dartford_data[column], name='Dartford'))
if ashford_checkbox:
    ashford_data = openbb.alt.realestate.get_region_stats('ashford',  startdate, enddate)
    fig = fig.add_trace(go.Scatter(x=ashford_data["month"], y=ashford_data[column], name='Ashford'))
if swale_checkbox:
    swale_data = openbb.alt.realestate.get_region_stats('swale',  startdate, enddate)
    fig = fig.add_trace(go.Scatter(x=swale_data["month"], y=swale_data[column], name='Swale'))
if london_checkbox:
    london_data = openbb.alt.realestate.get_region_stats('london',  startdate, enddate)
    fig = fig.add_trace(go.Scatter(x=london_data["month"], y=london_data[column], name='London'))
if england_checkbox:
    england_data = openbb.alt.realestate.get_region_stats('england',  startdate, enddate)
    fig = fig.add_trace(go.Scatter(x=england_data["month"], y=england_data[column], name='England'))

st.plotly_chart(fig,use_container_width=True)


