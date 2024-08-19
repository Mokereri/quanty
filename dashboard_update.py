# Update dashboard based on user input
if st.sidebar.button('Update'):
    data = fetch_stock_data(ticker, time_period, interval_mapping[time_period])
    data = process_data(data)
    data = add_technical_indicators(data)
    
    last_close, change, pct_change, high, low, volume = calculate_metrics(data)

# Display main metrics
st.metric(label=f"{ticker} Last Price", value=f"{last_close:.2f} USD", delta=f"{change:.2f} ({pct_change:.2f}%)")

col1, col2, col3=st.columns(3)
col1.metric("High", f"{high:.2f} USD")
col2.metric("Low", f"{low:.2f} USD")
col3.metric("volume", f"{volume:,}")

# Plot stock price chart
fig = go.Figure()
if chart_type == 'Candlestick':
    fig.add_trace(go.Candlestick(x=data['Datetime'],
                                 open=data['open'],
                                 high=data['high'],
                                 low=data['low'],
                                 close=data['Close']))
else:
    fig = px.line(data, x='Datetime', y='Close')

st.plotly_chart(fig, use_container_width=True)