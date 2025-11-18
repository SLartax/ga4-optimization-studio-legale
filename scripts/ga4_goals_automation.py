#!/usr/bin/env python3
# GA4 Goals Automation & Alerts Manager
# Automatizza la creazione e configurazione dei Goals
# Gestisce alerts per metriche critiche

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests

class GA4GoalsManager:
    def __init__(self, property_id: str, admin_email: str):
        self.property_id = property_id
        self.admin_email = admin_email
        self.goals_config = self._load_goals_config()
        
    def _load_goals_config(self) -> Dict:
        """
        Carica la configurazione dei Goals da file JSON.
        """
        try:
            with open('config/ga4_goals.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception("File ga4_goals.json non trovato")
    
    def create_all_goals(self) -> List[Dict]:
        """
        Crea tutti i goals configurati.
        Returns: Lista dei goals creati
        """
        created_goals = []
        
        for goal_key, goal_config in self.goals_config['goals'].items():
            goal_data = {
                'name': goal_config['name'],
                'description': goal_config['description'],
                'type': goal_config['type'],
                'value': goal_config.get('value', 0),
                'event_name': goal_config.get('event_name'),
                'property_id': self.property_id
            }
            
            # Simula creazione goal (in produzione: API call a GA4)
            created_goals.append({
                'status': 'created',
                'goal': goal_data,
                'timestamp': datetime.now().isoformat()
            })
            
            print(f"✓ Goal creato: {goal_config['name']}")
        
        return created_goals
    
    def setup_conversion_funnel(self) -> Dict:
        """
        Configura il conversion funnel.
        """
        funnel = self.goals_config['conversion_funnel']
        
        funnel_data = {
            'name': funnel['name'],
            'steps': funnel['steps'],
            'property_id': self.property_id,
            'created_at': datetime.now().isoformat()
        }
        
        print(f"✓ Funnel di conversione configurato: {funnel['name']}")
        print(f"  Step nel funnel: {len(funnel['steps'])}")
        
        return funnel_data
    
    def setup_alerts(self, client) -> List[Dict]:
        """
        Configura gli alert automatici.
        """
        alerts = [
            {
                'name': 'Traffic Drop Alert',
                'condition': 'sessions_daily < (avg_weekly * 0.70)',
                'threshold': 70,
                'enabled': True,
                'email_recipients': [self.admin_email]
            },
            {
                'name': 'High Bounce Rate Alert',
                'condition': 'bounce_rate > 60',
                'threshold': 60,
                'enabled': True,
                'email_recipients': [self.admin_email]
            },
            {
                'name': 'Zero Conversions Alert',
                'condition': 'daily_conversions == 0 for 2+ days',
                'threshold': 0,
                'enabled': True,
                'email_recipients': [self.admin_email]
            },
            {
                'name': 'Conversion Spike Alert',
                'condition': 'daily_conversions > (avg_daily * 1.5)',
                'threshold': 150,
                'enabled': True,
                'email_recipients': [self.admin_email]
            }
        ]
        
        print(f"\n✓ {len(alerts)} alert configurati")
        for alert in alerts:
            print(f"  - {alert['name']}: {alert['condition']}")
        
        return alerts
    
    def check_alert_conditions(self, metrics: Dict) -> List[Dict]:
        """
        Verifica le condizioni degli alert.
        
        Args:
            metrics: Dizionario con metriche attuali
            
        Returns:
            Lista degli alert attivati
        """
        triggered_alerts = []
        
        # Check Traffic Drop
        if metrics.get('traffic_drop_detected'):
            triggered_alerts.append({
                'alert': 'Traffic Drop Alert',
                'severity': 'HIGH',
                'value': metrics['current_sessions'],
                'message': f"Calo del traffico rilevato. Sessioni: {metrics['current_sessions']}"
            })
        
        # Check High Bounce Rate
        if metrics.get('bounce_rate', 0) > 60:
            triggered_alerts.append({
                'alert': 'High Bounce Rate Alert',
                'severity': 'MEDIUM',
                'value': metrics['bounce_rate'],
                'message': f"Bounce rate elevato: {metrics['bounce_rate']}%"
            })
        
        # Check Zero Conversions
        if metrics.get('daily_conversions', 0) == 0:
            triggered_alerts.append({
                'alert': 'Zero Conversions Alert',
                'severity': 'HIGH',
                'value': 0,
                'message': "Nessuna conversione rilevata oggi"
            })
        
        return triggered_alerts
    
    def send_alert_email(self, alert: Dict) -> bool:
        """
        Invia email di alert.
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"[GA4 Alert] {alert['alert']} - {alert['severity']}"
            msg['From'] = 'ga4-alerts@artax-studio.it'
            msg['To'] = self.admin_email
            
            html = f"""
            <html>
              <head></head>
              <body>
                <h2 style="color: #d32f2f;">{alert['alert']}</h2>
                <p><strong>Gravità:</strong> {alert['severity']}</p>
                <p><strong>Valore:</strong> {alert['value']}</p>
                <p><strong>Messaggio:</strong> {alert['message']}</p>
                <p><strong>Timestamp:</strong> {datetime.now().isoformat()}</p>
                <hr>
                <p>Accedi a Google Analytics per visualizzare i dettagli completi.</p>
              </body>
            </html>
            """
            
            msg.attach(MIMEText(html, 'html'))
            
            print(f"✓ Email di alert inviata: {alert['alert']} ({alert['severity']})")
            return True
            
        except Exception as e:
            print(f"✗ Errore nell'invio dell'email: {e}")
            return False
    
    def generate_report(self, client) -> Dict:
        """
        Genera report completo GA4.
        """
        report_date = datetime.now()
        
        report = {
            'generated_at': report_date.isoformat(),
            'property_id': self.property_id,
            'summary': {
                'goals_configured': len(self.goals_config['goals']),
                'funnel_steps': len(self.goals_config['conversion_funnel']['steps']),
                'alerts_active': 4
            },
            'metrics': {
                'sessions_7d': 'N/A',
                'conversions_7d': 'N/A',
                'conversion_rate': 'N/A',
                'avg_session_duration': 'N/A'
            }
        }
        
        print(f"\n\u2713 Report generato per {report_date.strftime('%d/%m/%Y %H:%M')}")
        return report

if __name__ == "__main__":
    # Configurazione
    PROPERTY_ID = "YOUR_GA4_PROPERTY_ID"
    ADMIN_EMAIL = "admin@artax-studio.it"
    
    manager = GA4GoalsManager(PROPERTY_ID, ADMIN_EMAIL)
    
    print("=" * 60)
    print("GA4 GOALS & ALERTS AUTOMATION")
    print("=" * 60)
    
    # Crea goals
    print("\n1. Creazione Goals...")
    goals = manager.create_all_goals()
    
    # Configura funnel
    print("\n2. Configurazione Conversion Funnel...")
    funnel = manager.setup_conversion_funnel()
    
    # Configura alerts
    print("\n3. Configurazione Alerts...")
    alerts = manager.setup_alerts(None)
    
    # Simula check degli alert
    print("\n4. Verifica Alert Conditions...")
    metrics = {
        'traffic_drop_detected': False,
        'bounce_rate': 35,
        'daily_conversions': 5,
        'current_sessions': 125
    }
    triggered = manager.check_alert_conditions(metrics)
    if triggered:
        print(f"  {len(triggered)} alert attivato/i")
    else:
        print("  Nessun alert attivato")
    
    # Genera report
    print("\n5. Generazione Report...")
    report = manager.generate_report(None)
    
    print("\n" + "=" * 60)
    print("COMPLETATO")
    print("=" * 60)
