from openbb_terminal.sdk import openbb
import streamlit as st
import datetime
import pandas as pd
from st_aggrid import AgGrid


st.set_page_config(layout="wide")


homeTab, discoveryTab = st.tabs(["Home", "Discovery"])

with homeTab:
    text_input = st.text_input('Symbol')

    st.metric('Symbol', text_input , delta=None, delta_color="inverse", help=None)
    if text_input:
        data = openbb.stocks.load(text_input)
        
        df_max_scaled = data.copy()
    
        # apply normalization techniques
        for column in df_max_scaled.columns:
            df_max_scaled[column] = df_max_scaled[column]  / df_max_scaled[column].abs().max()
        
        st.subheader('openbb.stocks.load')
        st.line_chart(data=df_max_scaled,  x=None, y=None, width=0, height=0, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader('openbb.stocks.dd.supplier')
            st.dataframe(openbb.stocks.dd.supplier(text_input))

        with col2:
            st.subheader('openbb.stocks.dd.customer')
            st.dataframe(openbb.stocks.dd.customer(text_input))


        # st.subheader('openbb.stocks.options.hist')

        # d = st.date_input("Date")

        # options_hist = openbb.stocks.options.hist(f"{text_input}", d, 150, call=True, source="ChartExchange")
        # st.dataframe(options_hist)
        
        pd.set_option('display.max_columns', None)
        st.subheader('openbb.stocks.options.info')
        data = openbb.stocks.options.info(text_input)
        new_data = pd.DataFrame.from_dict(data, orient='index')

        new_data = new_data.reset_index(level=0)
        new_data.columns=['Heading','Value']

        AgGrid(new_data, height=300)


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