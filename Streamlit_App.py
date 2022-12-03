import streamlit as st 
from openbb_terminal.sdk import openbb


def main():

     st.set_page_config(layout="wide")
     st.title('Streamlit & OpenBB Example')

     st.write('''An example app show casing some of OpenBB's functionality''')

main()
