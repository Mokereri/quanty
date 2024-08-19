# Add selected technical indicators to the chart
for indicator in indicators:
    if indicator == 'SMA 20':
        fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA 20'], name='SMA 20'))
    elif indicator == 'EMA 20':
        fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA 20'], name=['EMA 20']))

# Format graph
fig.update_layout(title=f'{ticker} {time_period.upper()} Chart',
                  xaxis_title='Time',
                  yaxis_title='Price (USD)',
                  height=600)
st.plotly_chart(fig, use_container_width=True)