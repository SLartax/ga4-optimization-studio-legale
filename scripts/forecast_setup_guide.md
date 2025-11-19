# GA4 Forecast Scheduler - Setup Guide

## 🍐 Automazione Aggiornamento Previsioni alle 17:30

Guida completa per configurare l'automazione del forecast GA4 con aggiornamento giornaliero alle 17:30 CET.

---

## 1. Prerequisiti

- **Python 3.8+** installato
- **pip** per la gestione dei pacchetti
- **Linux server** (o Windows con WSL2) per esecuzione in background
- **GA4 Property ID** del tuo account
- **Google Cloud credentials** (JSON service account)

---

## 2. Installazione Dipendenze

### Step 2.1: Installare librerie Python richieste

```bash
pip install apscheduler pytz google-analytics-data pandas requests
```

### Step 2.2: Verifica installazione

```bash
python -c "import apscheduler; print('APScheduler OK')"
python -c "import pytz; print('Pytz OK')"
```

---

## 3. Configurazione Credenziali GA4

### Step 3.1: Posizionare credenziali

1. Scarica il file JSON dalle tue Google Cloud Console
2. Salva come `credentials.json` nella root del progetto
3. Imposta la variabile d'ambiente:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```

### Step 3.2: Configurare variabili d'ambiente

Crea un file `.env` nella root del progetto:

```env
GA4_PROPERTY_ID=123456789
ADMIN_EMAIL=admin@artax-studio.it
TIMEZONE=Europe/Rome
FORECAST_TIME=17:30
```

O esporta direttamente nel terminale:

```bash
export GA4_PROPERTY_ID="123456789"
export ADMIN_EMAIL="admin@artax-studio.it"
```

---

## 4. Avvio Scheduler - Opzione A (Sviluppo Locale)

### Esecuzione in foreground (debugging)

```bash
cd /path/to/ga4-optimization-studio-legale
python scripts/ga4_forecast_scheduler.py
```

**Output atteso:**

```
======================================================================
GA4 FORECAST SCHEDULER - Startup
======================================================================
Config: {
    "scheduler_timezone": "Europe/Rome",
    "forecast_time": "17:30",
    "property_id": "123456789",
    ...
}
======================================================================

[SUCCESS] Scheduler pronto. Premi CTRL+C per fermare.

[JOB_START] Inizio update forecast - 2025-11-19 13:45:22
[STEP 1/3] Estrazione dati da GA4...
[OK] Estratti 7 record da GA4
[STEP 2/3] Elaborazione dati...
[OK] Elaborati dati per forecast
[STEP 3/3] Salvataggio forecast...
[OK] Forecast salvato: forecasts/forecast_2025-11-19_13-45-22.json
[JOB_COMPLETE] Aggiornamento completato con successo
```

---

## 5. Avvio Scheduler - Opzione B (Production Linux con systemd)

### Step 5.1: Crea service file

```bash
sudo nano /etc/systemd/system/ga4-forecast.service
```

### Step 5.2: Contenuto del file

```ini
[Unit]
Description=GA4 Forecast Scheduler
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=www-data
WorkingDirectory=/home/user/ga4-optimization-studio-legale
Environment="GOOGLE_APPLICATION_CREDENTIALS=/home/user/ga4-optimization-studio-legale/credentials.json"
Environment="GA4_PROPERTY_ID=123456789"
Environment="ADMIN_EMAIL=admin@artax-studio.it"
ExecStart=/usr/bin/python3 /home/user/ga4-optimization-studio-legale/scripts/ga4_forecast_scheduler.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/ga4-forecast/scheduler.log
StandardError=append:/var/log/ga4-forecast/error.log

[Install]
WantedBy=multi-user.target
```

### Step 5.3: Abilitare e avviare il servizio

```bash
# Crea directory log
sudo mkdir -p /var/log/ga4-forecast
sudo chown www-data:www-data /var/log/ga4-forecast

# Ricarica systemd
sudo systemctl daemon-reload

# Abilita all'avvio
sudo systemctl enable ga4-forecast.service

# Avvia il servizio
sudo systemctl start ga4-forecast.service

# Verifica lo stato
sudo systemctl status ga4-forecast.service
```

---

## 6. Avvio Scheduler - Opzione C (Production Linux con Cron)

### Step 6.1: Modifica crontab

```bash
crontab -e
```

### Step 6.2: Aggiungi la riga cron

```cron
# Esegui il scheduler 24/7 (mantieni il processo attivo)
@reboot nohup python3 /home/user/ga4-optimization-studio-legale/scripts/ga4_forecast_scheduler.py > /var/log/ga4-forecast/cron.log 2>&1 &

# Oppure con diretto con APScheduler ogni giorno a 17:30
# (solo se usi versione basata su cron puro, non questa)
30 17 * * * export GA4_PROPERTY_ID=123456789 && python3 /home/user/ga4-optimization-studio-legale/scripts/ga4_forecast_scheduler.py
```

---

## 7. Monitoraggio e Logging

### Visualizza log in tempo reale

```bash
tail -f logs/forecast_scheduler.log
```

### Visualizza log del servizio systemd

```bash
sudo journalctl -u ga4-forecast.service -f
sudo journalctl -u ga4-forecast.service -n 50  # Ultimi 50 log
```

### Analizza forecast generati

```bash
ls -lh forecasts/
cat forecasts/forecast_latest.json | jq .  # Richiede jq installato
```

---

## 8. Verifica Aggiornamento Automatico

### Visualizza prossimo run

```python
python3 << 'EOF'
from scripts.ga4_forecast_scheduler import GA4ForecastScheduler, CONFIG
import json

scheduler = GA4ForecastScheduler(CONFIG)
status = scheduler.get_status()
print(json.dumps(status, indent=2, default=str))
EOF
```

### Trigger manuale test

```bash
python3 -c "
from scripts.ga4_forecast_scheduler import GA4ForecastScheduler, CONFIG
scheduler = GA4ForecastScheduler(CONFIG)
scheduler.forecast_update_job()
"
```

---

## 9. Troubleshooting

### Errore: "APScheduler not installed"

```bash
pip install --upgrade apscheduler
pip install pytz
```

### Errore: "No module named 'google.analytics.data'"

```bash
pip install --upgrade google-analytics-data
```

### Errore: "credentials.json not found"

- Verifica che `credentials.json` sia nella root del progetto
- Controlla che `GOOGLE_APPLICATION_CREDENTIALS` sia settato correttamente

```bash
echo $GOOGLE_APPLICATION_CREDENTIALS
```

### Errore: "Failed to connect to GA4"

- Verifica che il GA4_PROPERTY_ID sia corretto
- Assicurati che le credenziali abbiano permessi di lettura su GA4
- Controlla la connessione internet

### Log vuoti o non aggiornati

```bash
# Verifica permessi directory
ls -la logs/
ls -la forecasts/

# Ricrea directory se necessario
mkdir -p logs forecasts
chmod 755 logs forecasts
```

---

## 10. Configurazione Email Alerts (Opzionale)

Il sistema supporta email alerts. Per abilitarli:

### Step 10.1: Installa libreria email

```bash
pip install smtplib email-validator
```

### Step 10.2: Modifica il metodo `_send_alert()` in ga4_forecast_scheduler.py

```python
def _send_alert(self, subject, message):
    import smtplib
    from email.mime.text import MIMEText
    
    try:
        msg = MIMEText(message)
        msg['Subject'] = f"[GA4-Forecast] {subject}"
        msg['From'] = "system@artax-studio.it"
        msg['To'] = self.config['admin_email']
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your-email@gmail.com', 'your-app-password')
        server.send_message(msg)
        server.quit()
        
        logger.info(f"[ALERT_SENT] Email inviata a {self.config['admin_email']}")
    except Exception as e:
        logger.warning(f"[ALERT_FAILED] Errore invio email: {str(e)}")
```

---

## 11. Verifica Prossimo Run a 17:30

### Controlla il log per la schedulazione

```bash
grep "NEXT_RUN" logs/forecast_scheduler.log

# Output atteso:
# 2025-11-19 13:45:22 - INFO - [NEXT_RUN] Prossimo aggiornamento previsto alle 17:30
```

### Attendi fino alle 17:30 e verifica nuovo forecast

```bash
# Monitoraggio in tempo reale
watch -n 10 'ls -lh forecasts/ | tail -5'
```

---

## 12. Statistiche e Metriche

### Numero forecast generati

```bash
ls forecasts/ | wc -l
```

### Spazio occupato

```bash
du -sh forecasts/
du -sh logs/
```

### Forecast più recente

```bash
ls -lt forecasts/ | head -1
cat forecasts/$(ls -t forecasts/ | head -1) | jq .
```

---

## 13. Roll Back e Disabilitazione

### Ferma il servizio

```bash
# Con systemd
sudo systemctl stop ga4-forecast.service
sudo systemctl disable ga4-forecast.service

# Con cron
killall python3  # Ferma il processo manualmente
```

### Rimuovi il servizio

```bash
sudo rm /etc/systemd/system/ga4-forecast.service
sudo systemctl daemon-reload
```

---

## 14. Checklist Finale

- [x] Python 3.8+ installato
- [x] APScheduler e dipendenze installate
- [x] Credenziali GA4 scaricate e posizionate
- [x] GA4_PROPERTY_ID configurato
- [x] Test run eseguito con successo
- [x] Scheduler avviato (systemd o cron)
- [x] Log monitorati e funzionanti
- [x] Prossimo run a 17:30 confermato
- [x] Forecast generati e salvati
- [x] Alert email configurati (opzionale)

---

**Versione:** 1.0  
**Ultimo aggiornamento:** 2025-11-19  
**Supporto:** admin@artax-studio.it
