import streamlit as st
import pandas as pd
import numpy as np
import time

st.title('Dashboard')

col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

st.subheader('Area Chart')
area_chart = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])  
st.area_chart(area_chart)

st.subheader('Bar Chart & Line Chart')
col4,col5 = st.columns(2)
with col4:
    bar_chart = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(bar_chart)
with col5:
    line_chart = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.line_chart(line_chart)
