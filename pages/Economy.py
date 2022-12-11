import streamlit as st 
from openbb_terminal.sdk import openbb
import pandas as pd


def color_negative_red(val):
    if type(val) != 'str':
        color = 'green' if val >0 else 'red'
        return f'color: {color}'


st.set_page_config(layout="wide")
st.title('openbb.economy')

col1, col2 = st.columns(2)

with col1:
    st.subheader('openbb.economy.currencies')
    data = openbb.economy.currencies()
    data[['Chng']] = data[['Chng']].apply(pd.to_numeric)
    st.dataframe(data.style.applymap(color_negative_red, subset=['Chng']))

with col2:
    st.subheader('openbb.economy.usbonds')
    data = openbb.economy.usbonds()
    data[data.columns[1]] = data[data.columns[1]].apply(pd.to_numeric)
    data[data.columns[2]] = data[data.columns[2]].apply(pd.to_numeric)
    data[data.columns[3]] = data[data.columns[3]].apply(pd.to_numeric)

    columns = data.columns[3]

    st.dataframe(data.style.applymap(color_negative_red, subset=[columns]))


col1, col2 = st.columns(2)

with col1:
    st.subheader('openbb.economy.macro_countries')
    countries = pd.DataFrame.from_dict(openbb.economy.macro_countries(), orient='index')
    st.dataframe(countries)


with col2:
    st.subheader('openbb.economy.indices')
    data = openbb.economy.indices()

    data[['Chg']] = data[['Chg']].apply(pd.to_numeric)

    st.dataframe(data.style.applymap(color_negative_red, subset=['Chg']))



data = openbb.economy.treasury()
st.subheader('openbb.economy.treasury')
st.line_chart(data=data,  x=None, y=None, width=0, height=0, use_container_width=True)


st.subheader('openbb.economy.events')
data = openbb.economy.events()
st.dataframe(data)