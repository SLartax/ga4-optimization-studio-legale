"""Trading System Dashboard - Streamlit
Dashboard interattiva per visualizzare equity curve, metriche e segnali trading
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Configurazione pagina Streamlit
st.set_page_config(
    page_title="Trading System Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato
st.markdown("""<style>
 .header { text-align: center; color: #1f77b4; }
 .metric-box { background-color: #f0f2f6; padding: 10px; border-radius: 5px; }
 .signal-flat { background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; }
 .signal-buy { background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; }
 .signal-sell { background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; }
</style>""", unsafe_allow_html=True)

# Titolo
st.markdown('<h1 class="header">📈 Trading System Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: gray;">Real-time Equity Curve & Performance Metrics</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚙️ Configurazione")
refresh_data = st.sidebar.checkbox("Aggiorna Dati", value=True)
aggiungi_annotazioni = st.sidebar.checkbox("Mostra Annotazioni", value=True)

# GENERATE MOCK DATA
@st.cache_data(ttl=3600)
def load_trading_data():
    # Genera dati di equity curve simulati
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2025-01-19', freq='D')
    
    # Simula equity curve con trend positivo
    returns = np.random.normal(0.0005, 0.015, len(dates))
    equity = 10000 * np.exp(np.cumsum(returns))
    daily_returns = np.diff(returns) * 100  # In percentuale
    daily_returns = np.append(daily_returns, daily_returns[-1])
    
    equity_df = pd.DataFrame({
        'Date': dates,
        'Equity': equity,
        'Daily_Return': daily_returns
    })
    
    # Metriche
    total_trades = 1529
    winning_trades = int(total_trades * 0.6625)
    losing_trades = total_trades - winning_trades
    
    metrics = {
        'Total_Trades': total_trades,
        'Winrate': '66.25%',
        'Total_Return': '+1,161.78%',
        'CAGR': '17.43%',
        'Avg_Pct_Trade': '0.1674%',
        'Avg_Points': '37.23',
        'Max_Drawdown': '-12.45%',
        'Sharpe_Ratio': '1.85',
        'Latest_Equity': f'${equity[-1]:,.2f}',
        'Signal_Tomorrow': 'FLAT'
    }
    
    trade_dist = {
        'Winning_Trades': winning_trades,
        'Losing_Trades': losing_trades
    }
    
    return equity_df, metrics, trade_dist

equity_df, metrics, trade_dist = load_trading_data()

# Layout principale con colonne
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Trades",
        value=f"{metrics['Total_Trades']:,}",
        delta="+5.2%"
    )

with col2:
    st.metric(
        label="Win Rate",
        value=metrics['Winrate'],
        delta="+1.3%"
    )

with col3:
    st.metric(
        label="Total Return",
        value=metrics['Total_Return'],
        delta="+45.2%"
    )

with col4:
    st.metric(
        label="CAGR",
        value=metrics['CAGR'],
        delta="+2.1%"
    )

st.divider()

# Sezione Equity Curve
st.subheader("📊 Equity Curve")
fig_equity = go.Figure()

fig_equity.add_trace(go.Scatter(
    x=equity_df['Date'],
    y=equity_df['Equity'],
    mode='lines',
    name='Equity',
    line=dict(color='#1f77b4', width=2),
    fill='tozeroy',
    fillcolor='rgba(31, 119, 180, 0.2)',
    hovertemplate='<b>Data:</b> %{x|%Y-%m-%d}<br><b>Equity:</b> $%{y:,.2f}<extra></extra>'
))

fig_equity.update_layout(
    title="Equity Curve Over Time",
    xaxis_title="Date",
    yaxis_title="Equity ($)",
    hovermode='x unified',
    template='plotly_white',
    height=500,
    showlegend=True
)

st.plotly_chart(fig_equity, use_container_width=True)

# Sezione Daily Returns Distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Daily Returns Distribution")
    fig_returns = px.histogram(
        x=equity_df['Daily_Return'],
        nbins=30,
        title="Distribution of Daily Returns (%)",
        labels={'x': 'Daily Return (%)', 'y': 'Frequency'},
        color_discrete_sequence=['#2ecc71']
    )
    fig_returns.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig_returns, use_container_width=True)

with col2:
    st.subheader("🎯 Trade Win/Loss Distribution")
    
    winning = int(trade_dist['Winning_Trades'])
    losing = int(trade_dist['Losing_Trades'])
    
    fig_trade = go.Figure(data=[
        go.Pie(
            labels=['Winning Trades', 'Losing Trades'],
            values=[winning, losing],
            marker=dict(colors=['#2ecc71', '#e74c3c']),
            hole=0.3,
            textinfo='label+percent+value'
        )
    ])
    fig_trade.update_layout(height=400, template='plotly_white')
    st.plotly_chart(fig_trade, use_container_width=True)

st.divider()

# Sezione Metriche Dettagliate
st.subheader("📋 Detailed Metrics")
metrics_df = pd.DataFrame([
    {'Metric': 'Average % per Trade', 'Value': metrics['Avg_Pct_Trade']},
    {'Metric': 'Average Points', 'Value': metrics['Avg_Points']},
    {'Metric': 'Max Drawdown', 'Value': metrics['Max_Drawdown']},
    {'Metric': 'Sharpe Ratio', 'Value': metrics['Sharpe_Ratio']},
    {'Metric': 'Latest Equity', 'Value': metrics['Latest_Equity']},
])
st.dataframe(metrics_df, use_container_width=True, hide_index=True)

st.divider()

# Sezione Segnale
st.subheader("🔔 Signal for Tomorrow")
signal = metrics['Signal_Tomorrow']

if signal == "FLAT":
    st.markdown(
        f'<div class="signal-flat"><h3>🔴 {signal}</h3><p>No trading signal for tomorrow. Market conditions neutral.</p></div>',
        unsafe_allow_html=True
    )
elif signal == "BUY":
    st.markdown(
        f'<div class="signal-buy"><h3>🟢 {signal}</h3><p>Buy signal detected for tomorrow!</p></div>',
        unsafe_allow_html=True
    )
elif signal == "SELL":
    st.markdown(
        f'<div class="signal-sell"><h3>🔴 {signal}</h3><p>Sell signal detected for tomorrow!</p></div>',
        unsafe_allow_html=True
    )

st.divider()

# Footer
st.markdown(
    f"<p style='text-align: center; color: gray; font-size: 12px;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
    unsafe_allow_html=True
)
