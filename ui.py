import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt

st.title('_CRYPTO BOT_')
st.subheader('DASHBOARD')

dataframe = pd.DataFrame(np.random.randn(10, 5),
  columns = ('col %d' % i
    for i in range(5)))
dataframe
st.write('This is a line_chart.')
st.line_chart(dataframe)
st.area_chart(dataframe)
