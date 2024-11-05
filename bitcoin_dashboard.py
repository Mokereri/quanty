import requests
import pandas as pd
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
import time

def get_historical_data_binance(interval, start_time, end_time):
    url = 'https://api.binance.com/api/v3/klines'
    all_data = []
    
    limit = 1000
    while start_time < end_time:
        params = {
            'symbol': 'BTCUSDT',
            'interval': interval,
            'limit': limit,
            'startTime': start_time,
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.status_code}, Response: {response.text}")
        
        data = response.json()

        if not data:
            break
        
        all_data.extend(data)
        start_time = int(data[-1][0]) + 1
        time.sleep(0.1)

    prices = [(float(item[0]), float(item[1]), float(item[2]), float(item[3]), float(item[4])) for item in all_data]
    volumes = [float(item[5]) for item in all_data]
    
    df = pd.DataFrame(prices, columns=['timestamp', 'open', 'high', 'low', 'close'])
    df['volume'] = volumes
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    return df

def calculate_metrics(df):
    df['daily_return'] = df['close'].pct_change()
    df['SMA_30'] = df['close'].rolling(window=30).mean()
    df['EMA_30'] = df['close'].ewm(span=30, adjust=False).mean()
    
    volatility = df['daily_return'].std() * 100
    highest_price = df['close'].max()
    lowest_price = df['close'].min()
    price_change = ((highest_price - lowest_price) / lowest_price) * 100
    average_volume = df['volume'].mean()

    # Get dates of highest and lowest prices
    highest_price_date = df.loc[df['close'] == highest_price, 'timestamp'].dt.strftime('%Y-%m-%d').values[0]
    lowest_price_date = df.loc[df['close'] == lowest_price, 'timestamp'].dt.strftime('%Y-%m-%d').values[0]

    return volatility, highest_price, highest_price_date, lowest_price, lowest_price_date, price_change, average_volume

# Main execution for Streamlit
if __name__ == "__main__":
    st.title("Bitcoin/US Dollar Historical Data Analysis")

    st.sidebar.header("Customize")
    
    interval = st.sidebar.selectbox(
        "Select Time Interval:",
        options=["1h", "4h", "1d", "1w", "1M", "1y"],
        index=1
    )
    
    year_range = st.sidebar.selectbox(
        "Select Year Range:",
        options=["2017-2020", "2021-2024"],
        index=0
    )

    if year_range == "2017-2020":
        start_time = int(datetime(2017, 1, 1).timestamp() * 1000)
        end_time = int(datetime(2020, 12, 31).timestamp() * 1000)
    else:
        start_time = int(datetime(2021, 1, 1).timestamp() * 1000)
        end_time = int(datetime(2024, 10, 31).timestamp() * 1000)

    chart_type = st.sidebar.selectbox(
        "Select Chart Type:",
        options=["Line Chart", "Candlestick Chart"],
        index=0
    )

    if st.sidebar.button("Update"):
        df = get_historical_data_binance(interval, start_time, end_time)
        
        volatility, highest_price, highest_price_date, lowest_price, lowest_price_date, price_change, average_volume = calculate_metrics(df)

        # Display metrics in cards with uniform light green borders
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div style="border: 2px solid lightgreen; border-radius: 10px; padding: 10px; height: 150px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h3 style="text-align: center;">Annualized Volatility</h3>
                <p style="text-align: center; font-size: 24px; font-weight: bold; color: darkblue;">{volatility:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="border: 2px solid lightgreen; border-radius: 10px; padding: 10px; height: 150px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h3 style="text-align: center;">Average Trading Volume</h3>
                <p style="text-align: center; font-size: 24px; font-weight: bold; color: darkblue;">{average_volume:.2f}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col3, col4, col5 = st.columns(3)

        with col3:
            st.markdown(f"""
            <div style="border: 2px solid lightgreen; border-radius: 10px; padding: 10px; height: 150px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h3 style="text-align: center;">Highest Price</h3>
                <p style="text-align: center; font-size: 24px; font-weight: bold; color: darkblue;">${highest_price:.2f}</p>
                <p style="text-align: center; font-size: 16px;">Date: {highest_price_date}</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style="border: 2px solid lightgreen; border-radius: 10px; padding: 10px; height: 150px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h3 style="text-align: center;">Lowest Price</h3>
                <p style="text-align: center; font-size: 24px; font-weight: bold; color: darkblue;">${lowest_price:.2f}</p>
                <p style="text-align: center; font-size: 16px;">Date: {lowest_price_date}</p>
            </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
            <div style="border: 2px solid lightgreen; border-radius: 10px; padding: 10px; height: 150px; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <h3 style="text-align: center;">Price Change (%)</h3>
                <p style="text-align: center; font-size: 24px; font-weight: bold; color: darkblue;">{price_change:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("Price Trend Analysis")
        
        if chart_type == "Line Chart":
            st.line_chart(df[['timestamp', 'close']].set_index('timestamp'))
        elif chart_type == "Candlestick Chart":
            fig = go.Figure(data=[go.Candlestick(x=df['timestamp'],
                                                   open=df['open'],
                                                   high=df['high'],
                                                   low=df['low'],
                                                   close=df['close'])])
            fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price (USDT)')
            st.plotly_chart(fig)

        st.subheader("Moving Averages")
        st.line_chart(df[['timestamp', 'SMA_30', 'EMA_30']].set_index('timestamp'))

        st.subheader("Data Used")
        st.write(df)

    else:
        st.write("Select an interval and click 'Update' to fetch data.")
    
    st.sidebar.markdown("This dashboard shows historical trading data for the Bitcoin/US Dollar pair over the selected year range.")
