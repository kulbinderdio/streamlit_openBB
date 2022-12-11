from openbb_terminal.sdk import openbb
import streamlit as st
import altair as alt
import pandas as pd
from st_aggrid import AgGrid


st.set_page_config(layout="wide")




data = openbb.stocks.gov.lasttrades()

      
st.subheader('openbb.stocks.gov.lasttrades')


AgGrid(data, height=300)

sales = data[data['Transaction']=='Sale']
purchases = data[data['Transaction']=='Purchase']
# AgGrid(sales, height=300)
# AgGrid(purchases, height=300)

highestTradersPurchase = sales.value_counts(['Representative']).reset_index(name='count')
highestTradersPurchase.columns=['Representative','Purchases']
highestTradersSales = purchases.value_counts(['Representative']).reset_index(name='count')
highestTradersSales.columns=['Representative','Sales']


c = alt.Chart(highestTradersPurchase, title='Total Number of Purchases Made').mark_bar().encode(
     x='Representative', y='Purchases',color=alt.value('green')).configure_title(fontSize=26).configure(background='#e8f4ff')
st.altair_chart(c, use_container_width=True)

c = alt.Chart(highestTradersSales, title='Total Number of Sales Made').mark_bar().encode(
     x='Representative', y='Sales',color=alt.value('red')).configure_title(fontSize=26).configure(background='#e8f4ff')
st.altair_chart(c, use_container_width=True)


highestTickerPurchase = sales.value_counts(['Ticker']).reset_index(name='count')
highestTickerPurchase.columns=['Ticker','Purchases']
highestTickerSales = purchases.value_counts(['Ticker']).reset_index(name='count')
highestTickerSales.columns=['Ticker','Sales']


c = alt.Chart(highestTickerPurchase, title='Total Number of Purchases Made').mark_bar().encode(
     x='Ticker', y='Purchases',color=alt.value('green')).configure_title(
        fontSize=26).configure(background='#e8f4ff').configure_axis(labelFontSize=6)
st.altair_chart(c, use_container_width=True)

c = alt.Chart(highestTickerSales, title='Total Number of Sales Made').mark_bar().encode(
     x='Ticker', y=alt.Y('Sales',axis=alt.Axis(labels=False)),color=alt.value('red')).configure_title(
        fontSize=26).configure(background='#e8f4ff').configure_axis(labelFontSize=6)
st.altair_chart(c, use_container_width=True)
