import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Milk Calculation UJ", 
    page_icon=":material/grocery:",
    initial_sidebar_state="expanded"
    )
st.logo("https://digitalcv.id/ultrajaya/assets/images/logo.png",size='large')
st.sidebar.markdown("Ultrajaya!")

with st.sidebar:
    with st.expander('Main Menu',True):
        dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:",default=True)
        milk_calc = st.Page("pages/milk-calculation.py", title="Milk Calculation", icon=":material/function:")
        datasets = st.Page("pages/datasets.py", title="Datasets", icon=":material/dataset:")

pg = st.navigation([dashboard, milk_calc, datasets])
pg.run()

