# Display historical data and technical indicators
st.subheader('Historical Data')
st.dataframe(data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']])

st.subheader('Technical Indicators')
st.dataframe(data[['Datetime', 'SMA 20', 'EMA 20']])
