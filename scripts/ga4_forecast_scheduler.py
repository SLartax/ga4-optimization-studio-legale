# -*- coding: utf-8 -*-
"""
GA4 FORECAST SCHEDULER - Automazione aggiornamento previsioni

Automatizza l'esecuzione della previsione GA4 ogni giorno alle 17:30
Per estrarre dati elaborati e generare forecast per il giorno successivo.

Author: Artax Studio Legale
Version: 1.0
Date: 2025-11-19
"""

import os
import sys
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    from pytz import timezone
except ImportError:
    print("\n[!] ERRORE: APScheduler non è installato")
    print("Installa con: pip install apscheduler pytz")
    sys.exit(1)

# ============================================================================
# CONFIGURAZIONE LOGGING
# ============================================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "forecast_scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURAZIONE GLOBALE
# ============================================================================

CONFIG = {
    "scheduler_timezone": "Europe/Rome",  # Timezone italiano
    "forecast_time": "17:30",  # Ora aggiornamento
    "property_id": os.getenv("GA4_PROPERTY_ID", "YOUR_GA4_PROPERTY_ID"),
    "admin_email": os.getenv("ADMIN_EMAIL", "admin@artax-studio.it"),
    "data_retention_days": 180,
    "max_retries": 3,
    "retry_delay_seconds": 30,
}

# ============================================================================
# CLASSE SCHEDULER
# ============================================================================

class GA4ForecastScheduler:
    """
    Gestisce l'automazione del forecast GA4 con scheduling a tempo fisso.
    """
    
    def __init__(self, config):
        self.config = config
        self.scheduler = BackgroundScheduler()
        self.tz = timezone(config["scheduler_timezone"])
        self.forecast_dir = Path("forecasts")
        self.forecast_dir.mkdir(exist_ok=True)
        logger.info(f"[INIT] GA4ForecastScheduler inizializzato")
        
    def forecast_update_job(self):
        """
        Job principale: esegue l'aggiornamento del forecast alle 17:30.
        """
        try:
            run_time = datetime.now(self.tz).strftime("%Y-%m-%d %H:%M:%S")
            logger.info(f"\n{'='*70}")
            logger.info(f"[JOB_START] Inizio update forecast - {run_time}")
            logger.info(f"{'='*70}")
            
            # Step 1: Estrai dati da GA4
            logger.info("[STEP 1/3] Estrazione dati da GA4...")
            ga4_data = self._fetch_ga4_data()
            
            if not ga4_data:
                logger.error("[ERROR] Impossibile estrarre dati da GA4")
                self._send_alert("GA4 Data Fetch Failed", 
                               f"Errore nell'estrazione dati GA4 alle {run_time}")
                return False
            
            logger.info(f"[OK] Estratti {len(ga4_data)} record da GA4")
            
            # Step 2: Elabora dati
            logger.info("[STEP 2/3] Elaborazione dati...")
            forecast_data = self._process_forecast_data(ga4_data)
            
            if not forecast_data:
                logger.error("[ERROR] Impossibile elaborare i dati")
                return False
            
            logger.info(f"[OK] Elaborati dati per forecast")
            
            # Step 3: Salva forecast
            logger.info("[STEP 3/3] Salvataggio forecast...")
            forecast_file = self._save_forecast(forecast_data)
            
            if not forecast_file:
                logger.error("[ERROR] Impossibile salvare il forecast")
                return False
            
            logger.info(f"[OK] Forecast salvato: {forecast_file}")
            
            # Step 4: Log summary
            logger.info(f"\n{'='*70}")
            logger.info(f"[JOB_COMPLETE] Aggiornamento completato con successo")
            logger.info(f"Timestamp: {run_time}")
            logger.info(f"Forecast file: {forecast_file}")
            logger.info(f"{'='*70}\n")
            
            self._send_alert("GA4 Forecast Updated", 
                           f"Forecast aggiornato alle {run_time}\nFile: {forecast_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"[EXCEPTION] Errore nel job: {str(e)}", exc_info=True)
            self._send_alert("GA4 Forecast Error", f"Errore: {str(e)}")
            return False
    
    def _fetch_ga4_data(self):
        """
        Estrae i dati elaborati da GA4 (ultimi 7 giorni).
        Ritenta fino a max_retries volte in caso di errore.
        """
        retry_count = 0
        
        while retry_count < self.config["max_retries"]:
            try:
                # Import dinamico del client GA4
                from ga4_api_client import GA4Client
                
                client = GA4Client(property_id=self.config["property_id"])
                
                # Estrai conversioni ultimi 7 giorni
                data = {
                    "conversions": client.get_conversion_report(days_back=7),
                    "traffic": client.get_traffic_by_source(days_back=7),
                    "segments": client.get_user_segments_data("all"),
                    "timestamp": datetime.now(self.tz).isoformat(),
                }
                
                return data
                
            except Exception as e:
                retry_count += 1
                logger.warning(f"[RETRY {retry_count}/{self.config['max_retries']}] "
                             f"Errore: {str(e)}")
                
                if retry_count < self.config["max_retries"]:
                    import time
                    time.sleep(self.config["retry_delay_seconds"])
                else:
                    logger.error("[FAILED] Max retries raggiunto")
                    return None
    
    def _process_forecast_data(self, ga4_data):
        """
        Processa i dati estratti e genera il forecast.
        Usa logica semplice per calcolare trend per il giorno seguente.
        """
        try:
            conversions = ga4_data.get("conversions", [])
            traffic = ga4_data.get("traffic", [])
            
            # Calcolo media conversioni ultimi 7 giorni
            avg_conversions = (
                sum([c.get("conversions", 0) for c in conversions]) / 
                max(len(conversions), 1)
            )
            
            # Calcolo media traffico
            avg_traffic = (
                sum([t.get("sessions", 0) for t in traffic]) / 
                max(len(traffic), 1)
            )
            
            tomorrow = (datetime.now(self.tz) + timedelta(days=1)).date()
            
            forecast = {
                "forecast_date": str(tomorrow),
                "predicted_conversions": round(avg_conversions, 2),
                "predicted_sessions": round(avg_traffic, 2),
                "confidence_level": "MEDIUM",  # Medium confidence da dati 7gg
                "data_points_used": len(conversions),
                "generated_at": datetime.now(self.tz).isoformat(),
            }
            
            return forecast
            
        except Exception as e:
            logger.error(f"[ERROR] Errore nel processing: {str(e)}")
            return None
    
    def _save_forecast(self, forecast_data):
        """
        Salva il forecast in JSON con timestamp.
        """
        try:
            timestamp = datetime.now(self.tz).strftime("%Y-%m-%d_%H-%M-%S")
            filename = self.forecast_dir / f"forecast_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(forecast_data, f, indent=2, ensure_ascii=False)
            
            # Mantieni solo gli ultimi 30 forecast
            self._cleanup_old_forecasts()
            
            return str(filename)
            
        except Exception as e:
            logger.error(f"[ERROR] Errore nel salvataggio: {str(e)}")
            return None
    
    def _cleanup_old_forecasts(self):
        """
        Mantiene solo gli ultimi 30 file di forecast.
        """
        try:
            forecasts = sorted(self.forecast_dir.glob("forecast_*.json"))
            
            if len(forecasts) > 30:
                for old_file in forecasts[:-30]:
                    old_file.unlink()
                    logger.info(f"[CLEANUP] Rimosso forecast vecchio: {old_file.name}")
                    
        except Exception as e:
            logger.warning(f"[CLEANUP] Errore nella pulizia: {str(e)}")
    
    def _send_alert(self, subject, message):
        """
        Invia alert via email (opzionale - implementa il tuo servizio)
        """
        try:
            logger.info(f"[ALERT] {subject}: {message}")
            # TODO: Integrare con EmailService
            
        except Exception as e:
            logger.warning(f"[ALERT_FAILED] Errore invio alert: {str(e)}")
    
    def start(self):
        """
        Avvia lo scheduler in background.
        """
        try:
            # Aggiungi il job schedulato a 17:30 ogni giorno
            self.scheduler.add_job(
                self.forecast_update_job,
                CronTrigger(hour=17, minute=30, timezone=self.tz),
                id='ga4_forecast_daily',
                name='GA4 Daily Forecast Update',
                replace_existing=True,
            )
            
            # Aggiungi anche un job di test all'avvio
            logger.info("[STARTUP] Esecuzione forecast di test...")
            self.forecast_update_job()
            
            # Avvia lo scheduler
            self.scheduler.start()
            logger.info("[SCHEDULER_STARTED] Scheduler avviato")
            logger.info(f"[NEXT_RUN] Prossimo aggiornamento previsto alle 17:30")
            
            return True
            
        except Exception as e:
            logger.error(f"[FATAL] Errore nell'avvio dello scheduler: {str(e)}", 
                        exc_info=True)
            return False
    
    def stop(self):
        """
        Arresta lo scheduler.
        """
        try:
            self.scheduler.shutdown()
            logger.info("[SCHEDULER_STOPPED] Scheduler fermato")
        except Exception as e:
            logger.error(f"[ERROR] Errore nell'arresto: {str(e)}")
    
    def get_status(self):
        """
        Ritorna lo stato dello scheduler.
        """
        jobs = self.scheduler.get_jobs()
        status = {
            "running": self.scheduler.running,
            "jobs_count": len(jobs),
            "jobs": [{
                "id": job.id,
                "name": job.name,
                "next_run_time": str(job.next_run_time),
            } for job in jobs]
        }
        return status

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    logger.info("\n" + "="*70)
    logger.info("GA4 FORECAST SCHEDULER - Startup")
    logger.info("="*70)
    logger.info(f"Config: {json.dumps(CONFIG, indent=2)}")
    logger.info("="*70 + "\n")
    
    # Crea lo scheduler
    scheduler = GA4ForecastScheduler(CONFIG)
    
    # Avvia
    if scheduler.start():
        logger.info("\n[SUCCESS] Scheduler pronto. Premi CTRL+C per fermare.\n")
        
        try:
            # Mantieni il processo attivo
            import time
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("\n[INTERRUPT] Arresto scheduler...")
            scheduler.stop()
            logger.info("[DONE] Scheduler fermato.\n")
    else:
        logger.error("[FAILED] Impossibile avviare lo scheduler")
        sys.exit(1)
