import streamlit as st
import requests
import pandas as pd
import time

# Mobile layout configuration
st.set_page_config(page_title="Olym Core", layout="centered")

st.title("🎯 Private Signal Dashboard")
st.caption("Live Real-Time Market Analysis Engine")

# Choose asset to monitor
asset = st.selectbox("Select Asset", ["BTCUSDT", "ETHUSDT"])

# Dynamic UI Placeholders
status_box = st.empty()
signal_box = st.empty()
metrics_box = st.empty()

# Calculate Technical Indicators
def calculate_indicators(prices):
    df = pd.DataFrame(prices, columns=['close'])
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    df['sma_fast'] = df['close'].rolling(window=5).mean()
    df['sma_slow'] = df['close'].rolling(window=20).mean()
    return df.iloc[-1]

price_history = []

# Live tracking engine loop
while True:
    try:
        status_box.success("🟢 System Connected to Market Feed")
        
        # Pull live crypto data from free Binance API
        url = f"https://binance.com{asset}"
        data = requests.get(url).json()
        current_price = float(data['price'])
        
        price_history.append(current_price)
        if len(price_history) > 30:
            price_history.pop(0)
            
        if len(price_history) >= 20:
            metrics = calculate_indicators(price_history)
            rsi = metrics['rsi']
            sma_f = metrics['sma_fast']
            sma_s = metrics['sma_slow']
            
            metrics_box.metric(label=f"Live {asset} Price", value=f"${current_price:,.2f}", delta=f"RSI: {rsi:.1f}")
            
            # Pure Mathematical Rules for Exact Timing Signals
            if rsi < 30 and sma_f > sma_s:
                signal_box.markdown(
                    "<div style='background-color:#052e16;padding:25px;border-radius:12px;text-align:center;border:2px solid #22c55e;'>"
                    "<h2 style='color:#22c55e;margin:0;'>🟢 CALL / BUY</h2>"
                    f"<p style='color:white;margin:5px 0 0 0;'>Open position on Olym Trade now.</p>"
                    "</div>", unsafe_style_html=True
                )
            elif rsi > 70 and sma_f < sma_s:
                signal_box.markdown(
                    "<div style='background-color:#450a0a;padding:25px;border-radius:12px;text-align:center;border:2px solid #ef4444;'>"
                    "<h2 style='color:#ef4444;margin:0;'>🔴 PUT / SELL</h2>"
                    f"<p style='color:white;margin:5px 0 0 0;'>Open position on Olym Trade now.</p>"
                    "</div>", unsafe_style_html=True
                )
            else:
                signal_box.markdown(
                    "<div style='background-color:#1e293b;padding:25px;border-radius:12px;text-align:center;'>"
                    "<h4 style='color:#94a3b8;margin:0;'>⏳ ANALYZING MARKET CONDITIONS...</h4>"
                    "</div>", unsafe_style_html=True
                )
        else:
            status_box.warning(f"📥 Syncing market charts... ({len(price_history)}/20)")
            
    except Exception as e:
        status_box.error("⚠️ Connection lagging. Syncing...")
        
    time.sleep(2) # Computes mathematical rules every 2 seconds
