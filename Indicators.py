# Add Simple Moving Average(SMA) and Eponential Moving Average(EMA) indicators 
def add_technical_indicators(data):
    data['SMA_20'] = ta.trend.sma_indicator(data['close'], window=20)
    data['EMA_20'] = ta.trend.sma_indicator(data['close'], window=20)
    return data