import streamlit as st 
from openbb_terminal.sdk import openbb
import pandas as pd


st.set_page_config(layout="wide")
st.title('openbb.etf')


st.subheader('openbb.etf.symbols')
data = openbb.etf.symbols()
data = pd.DataFrame(data).T
st.dataframe(data)



symbol = st.text_input('ETF Symbol')

if symbol:
    st.subheader('openbb.etf.summary')
    st.write(openbb.etf.summary(symbol))

    c1, c2 = st.columns((2, 3))
    with c1:
        st.subheader('openbb.etf.overview')
        st.dataframe(openbb.etf.overview(symbol))

    data = openbb.etf.load(symbol)
    with c2:
        st.subheader('openbb.etf.load')
        st.dataframe(data)

    df_max_scaled = data.copy()
  
    # apply normalization techniques
    for column in df_max_scaled.columns:
        df_max_scaled[column] = df_max_scaled[column]  / df_max_scaled[column].abs().max()
      
    st.subheader('openbb.etf.load')
    st.line_chart(data=df_max_scaled,  x=None, y=None, width=0, height=0, use_container_width=True)


    st.subheader('openbb.etf.weights')
    data = openbb.etf.weights(symbol)
    new_data = pd.DataFrame.from_dict(data, orient='index')
    # st.dataframe(pd.DataFrame.from_dict(data))
    st.bar_chart(new_data)


st.subheader("openbb.etf.etf_by_category('Technology')")
data = openbb.etf.etf_by_category('Financial')
data = pd.DataFrame(data)
st.dataframe(data.T)