# Real time stock prices 
st.sidebar.header('Real-Time Stock Prices')
stock_symbols = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
for symbol in stock_symbols:
    real_time_data = fetch_stock_data(symbol, '1d', '1m')
    if not real_time_data.empty:
        real_time_data = process_data(real_time_data)
        last_price = real_time_data['Close'].iloc[-1]
        change = last_price - real_time_data['Open'].iloc[0]
        pct_change = (change/real_time_data['Open'].iloc[0]) * 100
        st.bar.metric(f"{symbol}", f"{last_price} USD", f"{change:.2f} ({pct_change:.2f}%)")

# Information section
st.sidebar.subheader('About')
st.sidebar.info('This Dashboard Stock data and technical indicators for various time periods')
