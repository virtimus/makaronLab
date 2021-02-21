import yfinance as yf

import streamlit as st

import pandas as pd


st.write("""

## Simple Stock price APP

Shown are the **stock closing** price and **volume** of Google




""")


tickerSymbol = 'GOOGL'
tickerData = yf.Ticker(tickerSymbol)

tickerDf = tickerData.history(period = '1d', start = '2010-05-31', end = '2020-05-31')

st.write("""
### Closing price
""")
st.line_chart(tickerDf.Close)
st.write("""
### Volume
""")
st.line_chart(tickerDf.Volume)