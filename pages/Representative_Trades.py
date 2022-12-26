from openbb_terminal.sdk import openbb
import streamlit as st
import altair as alt
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from pages.Stocks import get_candlestick_plot

st.set_page_config(layout="wide")

data = openbb.stocks.gov.lasttrades()

gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_selection('single')
gridOptions = gb.build()

      
st.subheader('openbb.stocks.gov.lasttrades')


grid_response = AgGrid(data, gridOptions=gridOptions, height=300)

sales = data[data['Transaction']=='Sale']
purchases = data[data['Transaction']=='Purchase']

selected = grid_response['selected_rows'] 
if len(selected) > 0:
     df_selected = pd.DataFrame(selected)
     ticker = df_selected['Ticker'].values[0]
     stock_data = openbb.stocks.load(ticker)

     selected_ticker_sales = data[(data['Transaction']=='Sale') & (data['Ticker']==ticker)]

     selected_ticker_purchases = data[(data['Transaction']=='Purchase') & (data['Ticker']==ticker)]

     ma1=10
     ma2=30
     df = stock_data.reset_index()
     df.columns = [x.title() for x in df.columns]
     df[f'{ma1}_ma'] = df['Close'].rolling(ma1).mean()
     df[f'{ma2}_ma'] = df['Close'].rolling(ma2).mean()
     df = df[-250:]

     st.plotly_chart(
            get_candlestick_plot(df, ma1, ma2, ticker, selected_ticker_sales['Transaction Date'].tolist(), 
            selected_ticker_purchases['Transaction Date'].tolist()),
            width=0, height=0,
            use_container_width = True,
        )


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
