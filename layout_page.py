# set up streamlit layout page
st.set_page_config(layout='wide')
st.title('Real Time Stock Dashboard')

# Sidebar user input parameters
st.sidebar.header('Chart Parameters')
ticker = st.sidebar.text_input('Ticker', 'ADBE')
time_period = st.sidebar.selectbox('Time period', ['1d', '1wk', '1mo', '1y', 'max'])
chart_type = st.sidebar.selectbox('chart type', ['Candlestick', 'Line'])
indicators = st.sidebar.multiselect('Technical Indicators', ['SMA 20', 'EMA 20'])

# Mapping time periods to data intervals
interval_mapping = {
    '1d': '1m',
    '1wk': '30m',
    '1mo': '1d',
    '1y': '1wk',
    'max': '1wk'
}