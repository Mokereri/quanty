# Compute basic metrics from stock data
def calculate_metrics(data):
    last_close = data ['close'].iloc[-1]
    prev_close = data ['close'].iloc[0]
    change = last_close-prev_close
    pct_change = (change / last_close)*100
    High = data['High'].max()
    Low = data['Low'].min()
    Volume = data['Volume'].sum()
    
    return last_close, prev_close, change, pct_change, High, Low, Volume