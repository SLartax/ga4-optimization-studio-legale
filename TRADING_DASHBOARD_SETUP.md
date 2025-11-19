# Trading Dashboard - Setup & Deployment Guide

## Sistema Completo di Visualizzazione Equity Curve e Metriche Trading

Questa guida ti spiega come deployare la dashboard trading live online in pochi minuti.

---

## 📋 Requisiti

- Account Streamlit Cloud (gratuito)
- Account GitHub (hai gia' il repository)
- Python 3.8+ (installato localmente per test)

---

## 🚀 Quick Deploy su Streamlit Cloud (5 minuti)

### Step 1: Accedi a Streamlit Cloud
1. Vai a https://share.streamlit.io
2. Accedi con il tuo GitHub account (SLartax)
3. Clicca "New app"

### Step 2: Configura l'App
- **Repository**: SLartax/ga4-optimization-studio-legale
- **Branch**: main
- **Main file path**: scripts/trading_dashboard.py

### Step 3: Deploy
Clicca "Deploy" e aspetta circa 2-3 minuti. La dashboard sarà live!

URL della dashboard: `https://share.streamlit.io/SLartax/ga4-optimization-studio-legale/<ID>`

---

## 📊 Dashboard Features

✅ **Equity Curve** - Visualizzazione trend curve equity in tempo reale
✅ **KPI Metrics** - Total trades, Win Rate, CAGR, Total Return
✅ **Daily Returns Distribution** - Istogramma distribuzione rendimenti giornalieri
✅ **Win/Loss Distribution** - Grafico a torta trade vincenti/perdenti
✅ **Trading Signal** - Segnale predittivo per il giorno successivo
✅ **Detailed Metrics** - Tabella con tutti i parametri di performance

---

## 🔄 Aggiornamento Automatico Dati

Per aggiornare i dati giornalmente:

### Opzione 1: GitHub Actions (Automatico)
Creare un file `.github/workflows/update-metrics.yml`:

```yaml
name: Update Trading Metrics
on:
  schedule:
    - cron: '30 17 * * 1-4'  # Lun-Gio 17:30
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Update Metrics
        run: python scripts/trading_system_metrics.py
      - name: Commit & Push
        run: |
          git config user.email "action@github.com"
          git config user.name "GitHub Action"
          git add trading_data/
          git commit -m "Update trading metrics"
          git push
```

### Opzione 2: Manuale
Eseguire localmente:
```bash
python scripts/trading_system_metrics.py
git add .
git commit -m "Update trading metrics"
git push
```

La dashboard su Streamlit Cloud si aggiornera' automaticamente!

---

## 📈 Metriche Attuali (Aggiornato Oggi)

| Metrica | Valore |
|---------|--------|
| Total Trades | 1,529 |
| Win Rate | 66.25% |
| Avg % per Trade | 0.1674% |
| Avg Points | 37.23 |
| CAGR | 17.43% |
| Total Return | 1161.78% |
| Signal Tomorrow | 🔴 FLAT |

---

## 🔔 Segnali Supportati

- **🟢 BUY** - Segnale di acquisto per il giorno successivo
- **🔴 SELL** - Segnale di vendita per il giorno successivo  
- **🟡 FLAT** - Nessun segnale operativo, mercato neutro

---

## 📱 Accesso alla Dashboard

Una volta deployata:
- **URL Pubblica**: Condivisibile con chiunque
- **Aggiornamento**: Automatico ogni refresh pagina
- **Mobile-friendly**: Responsive design
- **Real-time**: Dati aggiornati in tempo reale

---

## 🛠️ Customizzazione

Per modificare la dashboard:
1. Edita `scripts/trading_dashboard.py`
2. Fai commit e push su GitHub
3. Streamlit Cloud si ricarichera' automaticamente

---

## 📞 Supporto

Per problemi:
1. Controlla il log su Streamlit Cloud
2. Verifica che `requirements.txt` abbia tutte le dipendenze
3. Assicurati che `trading_system_metrics.py` generi i dati

---

**Dashboard Status**: ✅ Ready for Production
**Last Updated**: 2025-11-19
