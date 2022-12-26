
import pandas as pd
import streamlit as st
from openbb_terminal.sdk import openbb
from io import StringIO
from pages.Stocks import get_candlestick_plot
from st_aggrid import AgGrid

st.set_page_config(layout="wide")

ma1=10
ma2=30
days_to_plot=180

st.subheader('Watchlist with Representative Trades')

uploaded_file = st.file_uploader("Choose a file of Tickers")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # To read file as string:
    string_data = stringio.read()

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file, header=0, names=['ticker'])

    representative_trades = openbb.stocks.gov.lasttrades()
    

    for i in dataframe['ticker'].tolist():
        dd = openbb.stocks.load(i)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(i.upper())
            
        df = dd.reset_index()
        df.columns = [x.title() for x in df.columns]
        df[f'{ma1}_ma'] = df['Close'].rolling(ma1).mean()
        df[f'{ma2}_ma'] = df['Close'].rolling(ma2).mean()
        df = df[-days_to_plot:]
        grid = AgGrid(df, height=300)
  
        trades = representative_trades[representative_trades['Ticker']==i.upper()]

        transaction_dates_sales = [] 
        transaction_dates_purchases = []
        if len(trades) > 0:
            transaction_dates_sales = trades[trades['Transaction']=='Sale']['Transaction Date'].tolist()
            transaction_dates_purchases = trades[trades['Transaction']=='Purchase']['Transaction Date'].tolist()

        # with col2:
        st.plotly_chart(
            get_candlestick_plot(df, ma1, ma2, i.upper(), transaction_dates_sales, transaction_dates_purchases),
            width=0, height=0,
            use_container_width = True,
        )

