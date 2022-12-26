from openbb_terminal.sdk import openbb
import streamlit as st
import datetime
import pandas as pd
from st_aggrid import AgGrid
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Candlestick code from 
# https://medium.com/@dannygrovesn7/using-streamlit-and-plotly-to-create-interactive-candlestick-charts-a2a764ad0d8e

ma1=10
ma2=30
days_to_plot=120

def get_candlestick_plot(
        df: pd.DataFrame,
        ma1: int,
        ma2: int,
        ticker: str,
        transaction_dates_sales: list = [],
        transaction_dates_purchases: list = []
):
    '''
    Create the candlestick chart with two moving avgs + a plot of the volume
    Parameters
    ----------
    df : pd.DataFrame
        The price dataframe
    ma1 : int
        The length of the first moving average (days)
    ma2 : int
        The length of the second moving average (days)
    ticker : str
        The ticker we are plotting (for the title).
    '''
    
    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.1,
        subplot_titles = (f'{ticker} Stock Price', 'Volume Chart'),
        row_width = [0.3, 0.7],
        row_heights=150
    )
    
    fig.add_trace(
        go.Candlestick(
            x = df['Date'],
            open = df['Open'], 
            high = df['High'],
            low = df['Low'],
            close = df['Close'],
            name = 'Candlestick chart'
        ),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Line(x = df['Date'], y = df[f'{ma1}_ma'], name = f'{ma1} SMA'),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Line(x = df['Date'], y = df[f'{ma2}_ma'], name = f'{ma2} SMA'),
        row = 1,
        col = 1,
    )

    for data in transaction_dates_sales:
        fig.add_vline(x=data, line_width=1, line_color="red")

    for data in transaction_dates_purchases:
        fig.add_vline(x=data, line_width=1, line_color="green")
    
    fig.add_trace(
        go.Bar(x = df['Date'], y = df['Volume'], name = 'Volume'),
        row = 2,
        col = 1,
    )
    
    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    
    fig.update_xaxes(
        rangebreaks = [{'bounds': ['sat', 'mon']}],
        rangeslider_visible = False,
    )

    
    
    return fig
    

st.set_page_config(layout="wide")


homeTab, discoveryTab = st.tabs(["Home", "Discovery"])



with homeTab:
    ticker = st.text_input('Symbol')

    if ticker:
        data = openbb.stocks.load(ticker)

        if len(data)>0:
            
            df = data.reset_index()
            df.columns = [x.title() for x in df.columns]

            df[f'{ma1}_ma'] = df['Close'].rolling(ma1).mean()
            df[f'{ma2}_ma'] = df['Close'].rolling(ma2).mean()
            df = df[-days_to_plot:]

            # Display the plotly chart on the dashboard
            st.plotly_chart(
                get_candlestick_plot(df, ma1, ma2, ticker),
                width=0, height=0,
                use_container_width = True,
            )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader('openbb.stocks.dd.supplier')
                st.dataframe(openbb.stocks.dd.supplier(ticker))

            with col2:
                st.subheader('openbb.stocks.dd.customer')
                st.dataframe(openbb.stocks.dd.customer(ticker))
            
            pd.set_option('display.max_columns', None)
            st.subheader('openbb.stocks.options.info')
            data = openbb.stocks.options.info(ticker)
            new_data = pd.DataFrame.from_dict(data, orient='index')

            new_data = new_data.reset_index(level=0)
            new_data.columns=['Heading','Value']

            AgGrid(new_data, height=300)
        else:
            st.write('No Data Found for '+ticker)


with discoveryTab:
    st.subheader('openbb.stocks.disc.gainers')
    gainers = openbb.stocks.disc.gainers()
    st.dataframe(gainers)

    st.subheader('openbb.stocks.disc.losers')
    losers = openbb.stocks.disc.losers()
    st.dataframe(losers)

    st.subheader('openbb.stocks.disc.gtech')
    gtech = openbb.stocks.disc.gtech()
    st.dataframe(gtech)

    st.subheader('openbb.stocks.disc.hotpenny')
    hotpenny = openbb.stocks.disc.hotpenny()
    st.dataframe(hotpenny)