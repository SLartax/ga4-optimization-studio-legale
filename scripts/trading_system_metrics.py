"""Trading System Metrics Generator
Genera equity curve, metriche e segnali trading per dashboard
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import os

class TradingSystemMetrics:
    def __init__(self):
        self.trades = 1529
        self.winrate = 0.6625
        self.avg_pct_trade = 0.001674
        self.avg_points = 37.23
        self.cagr = 0.1743
        self.total_return = 11.6178
        self.max_drawdown = 0.0312
        self.signal_tomorrow = "FLAT"
        
    def generate_equity_curve(self, initial_balance=10000, days=500):
        """Genera equity curve simulata basata sulle metriche del sistema"""
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # Distribuzione trade: ~3 trade al giorno
        trades_per_day = self.trades / days
        equity = [initial_balance]
        
        daily_returns = []
        for day in range(1, days):
            # Numero trade del giorno
            n_trades = max(1, int(np.random.poisson(trades_per_day)))
            
            # Risultati trade (66.25% vincenti)
            wins = int(n_trades * self.winrate)
            losses = n_trades - wins
            
            # P&L giornaliero
            day_pnl = 0
            for _ in range(wins):
                pnl_trade = equity[-1] * self.avg_pct_trade
                day_pnl += pnl_trade
            
            for _ in range(losses):
                pnl_trade = equity[-1] * self.avg_pct_trade * -0.5
                day_pnl += pnl_trade
            
            new_equity = equity[-1] + day_pnl
            daily_returns.append((day_pnl / equity[-1]) * 100)
            equity.append(max(new_equity, equity[-1] * 0.97))  # Max drawdown limiter
        
        df = pd.DataFrame({
            'Date': dates,
            'Equity': equity[1:],
            'Daily_Return': daily_returns
        })
        
        return df
    
    def calculate_metrics(self, equity_df):
        """Calcola metriche dal dataframe equity curve"""
        equity = equity_df['Equity'].values
        daily_returns = equity_df['Daily_Return'].values
        
        metrics = {
            'Total_Trades': self.trades,
            'Winrate': f"{self.winrate*100:.2f}%",
            'Avg_Pct_Trade': f"{self.avg_pct_trade*100:.4f}%",
            'Avg_Points': f"{self.avg_points:.2f}",
            'CAGR': f"{self.cagr*100:.2f}%",
            'Total_Return': f"{self.total_return*100:.2f}%",
            'Max_Drawdown': f"{self.max_drawdown*100:.2f}%",
            'Sharpe_Ratio': f"{np.mean(daily_returns) / np.std(daily_returns):.2f}",
            'Latest_Equity': f"{equity[-1]:,.2f}",
            'Signal_Tomorrow': self.signal_tomorrow
        }
        
        return metrics
    
    def generate_trade_distribution(self):
        """Genera distribuzione dei trade"""
        # Generazione casuale ma realistica dei win/loss
        total_pnl = self.trades * self.avg_pct_trade * 100
        winning_trades = int(self.trades * self.winrate)
        losing_trades = self.trades - winning_trades
        
        return {
            'Winning_Trades': winning_trades,
            'Losing_Trades': losing_trades,
            'Avg_Win': f"{(total_pnl / winning_trades):.2f}%" if winning_trades > 0 else "0%",
            'Avg_Loss': f"{(-total_pnl / losing_trades / 2):.2f}%" if losing_trades > 0 else "0%"
        }
    
    def export_data(self, output_dir='trading_data'):
        """Esporta tutti i dati in JSON"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Genera equity curve
        equity_df = self.generate_equity_curve()
        equity_df.to_csv(f'{output_dir}/equity_curve.csv', index=False)
        
        # Calcola metriche
        metrics = self.calculate_metrics(equity_df)
        
        # Distribuzione trade
        trade_dist = self.generate_trade_distribution()
        
        # JSON export
        output_data = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'trade_distribution': trade_dist,
            'equity_stats': {
                'Initial': 10000,
                'Final': float(equity_df['Equity'].iloc[-1]),
                'Peak': float(equity_df['Equity'].max()),
                'Trough': float(equity_df['Equity'].min())
            }
        }
        
        with open(f'{output_dir}/trading_metrics.json', 'w') as f:
            json.dump(output_data, f, indent=2)
        
        return equity_df, metrics, trade_dist

if __name__ == '__main__':
    system = TradingSystemMetrics()
    equity_df, metrics, trade_dist = system.export_data()
    
    print("\n=== TRADING SYSTEM METRICS ===")
    print(f"\nMetriche Principali:")
    for key, value in metrics.items():
        print(f"{key}: {value}")
    
    print(f"\nDistribuzione Trade:")
    for key, value in trade_dist.items():
        print(f"{key}: {value}")
    
    print(f"\nDati esportati in cartella 'trading_data/'")
