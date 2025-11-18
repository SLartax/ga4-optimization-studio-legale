# GA4 Optimization Studio Legale

Sistema completo di ottimizzazione Google Analytics 4 per studio legale. Include configurazioni avanzate, script Python automatizzati e dashboard personalizzati.

## Caratteristiche

✅ **Custom Events Tracking** - 5 eventi specializzati per studio legale
✅ **Goals Automation** - 6 conversion goals pre-configurati
✅ **Conversion Funnel** - Funnel completo da homepage a conversione
✅ **UTM Parameters** - Sistema standardizzato per campagne
✅ **Custom Segments** - 6 segmenti utente pre-configurati
✅ **Automated Alerts** - 4 alert per metriche critiche
✅ **Python API Integration** - Script per estrarre dati e gestire goals
✅ **Email Notifications** - Alert via email per anomalie

## Struttura del Progetto

```
ga4-optimization-studio-legale/
├── config/
│   ├── ga4_events.json              # Configurazione custom events
│   ├── ga4_goals.json               # Configurazione goals e funnel
│   └── utm_and_segments.json        # UTM parameters e segmenti
├── scripts/
│   ├── ga4_api_client.py            # Client API per estrarre report
│   └── ga4_goals_automation.py      # Automazione goals e alerts
├── README.md                        # Questa documentazione
└── LICENSE
```

## Setup Iniziale

### 1. Prerequisiti

- Python 3.8+
- Google Analytics 4 property
- Google Cloud Project con API abilitate
- Credenziali di servizio (service account)

### 2. Installazione Dipendenze Python

```bash
pip install google-analytics-data pandas requests
```

### 3. Configurare Google Credentials

```bash
# Scarica il file JSON delle credenziali da Google Cloud Console
# Posizionalo nella root del progetto come 'credentials.json'
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```

## Implementazione Veloce

### Passo 1: Custom Events

Il file `config/ga4_events.json` contiene 5 eventi predefiniti:

| Evento | Descrizione | Parametri |
|--------|-------------|----------|
| **form_contact_submitted** | Compilazione form contatti | service_type, user_segment, form_completion_time |
| **phone_call_initiated** | Chiamata telefonica | phone_type, call_source |
| **cta_download** | Download documentazione | document_type, page_type |
| **service_page_view** | Visualizzazione servizio | service_name |
| **blog_engagement** | Lettura articoli | scroll_depth, time_on_page |

**Implementazione in GTM:**
1. Accedi a Google Tag Manager
2. Crea trigger e tag per ogni evento
3. Importa i nomi evento dalla configurazione
4. Configura parametri personalizzati

### Passo 2: Goals & Conversion Funnel

Lancia lo script Python per creare automaticamente i goals:

```bash
python scripts/ga4_goals_automation.py
```

Il script crea:
- 6 Goals (form submission, phone calls, downloads, ecc.)
- 1 Conversion Funnel con 5 step
- 4 Alert automatici

### Passo 3: UTM Parameters

Usa i parametri UTM standardizzati per tutte le campagne:

**LinkedIn:**
```
https://tuo-sito.it?utm_source=linkedin&utm_medium=social&utm_campaign=legal_services_awareness&utm_content=post_novembre
```

**Email Newsletter:**
```
https://tuo-sito.it?utm_source=newsletter&utm_medium=email&utm_campaign=monthly_updates&utm_content=novembre_2025
```

**Partner/Referral:**
```
https://tuo-sito.it?utm_source=[partner_name]&utm_medium=referral&utm_campaign=partnership_2025
```

### Passo 4: Segmenti

I 6 segmenti predefiniti sono già configurati in GA4:

1. **High-Value Legal Leads** - Form submission + scroll>75% + tempo>180s
2. **Service Interested** - Pagina servizi + >3 pagine + CTA clicks
3. **Local Traffic (Nord Italia)** - Torino, Milano, Genova, etc.
4. **Mobile High-Intent** - Dispositivi mobile + phone_call_initiated
5. **Organic Search Quality** - Traffico organico + bounce<40% + >2 pagine
6. **Returning Clients** - Utenti che tornano al sito

## Script Python

### ga4_api_client.py

Estrare dati da GA4 in Python:

```python
from scripts.ga4_api_client import GA4Client

client = GA4Client(property_id='YOUR_GA4_PROPERTY_ID')

# Conversioni ultimi 7 giorni
conversions = client.get_conversion_report(days_back=7)
print(conversions)

# Traffico per fonte
traffic = client.get_traffic_by_source(days_back=7)
print(traffic)

# Dati segmenti
local_traffic = client.get_user_segments_data('local_traffic_north_italy')
print(local_traffic)
```

### ga4_goals_automation.py

Gestire goals e alerts automaticamente:

```python
from scripts.ga4_goals_automation import GA4GoalsManager

manager = GA4GoalsManager(
    property_id='YOUR_GA4_PROPERTY_ID',
    admin_email='admin@artax-studio.it'
)

# Crea tutti i goals
goals = manager.create_all_goals()

# Configura funnel
funnel = manager.setup_conversion_funnel()

# Configura alert
alerts = manager.setup_alerts(client)

# Verifica condizioni alert
metrics = {'bounce_rate': 45, 'daily_conversions': 8}
triggered = manager.check_alert_conditions(metrics)
```

## KPI Chiave da Monitorare

### Dashboard Executive Summary
- Sessioni totali (settimanali)
- Conversioni (form + telefonate)
- Conversion rate %
- Bounce rate per pagina servizi
- Avg. Session Duration
- Users per device

### Dashboard Acquisition
- Traffico per source (organic, direct, social, email)
- Nuovo vs Returning %
- Geographic distribution
- Device breakdown
- Trend mensili

### Dashboard Conversion
- Funnel conversion rate
- Form submissions per service
- Phone calls initiated
- Document downloads
- Time to conversion

## Alert & Monitoring

Gli alert sono configurati per:

| Alert | Condizione | Severity |
|-------|-----------|----------|
| Traffic Drop | Sessions < 70% media settimanale | HIGH |
| High Bounce Rate | Bounce rate > 60% | MEDIUM |
| Zero Conversions | 0 conversioni x 2+ giorni | HIGH |
| Conversion Spike | Conversioni > 150% media | INFO |

## Integrazione Search Console

1. Accedi a **Admin → Product Links → Search Console Links**
2. Collega le properties di Search Console
3. Visualizza query di ricerca, impressioni, CTR in GA4

## Troubleshooting

**Problema:** Events non vengono registrati
- Verifica che il GTM sia implementato correttamente
- Controlla i nomi degli event (case-sensitive)
- Usa il debugger di GA4 per validare

**Problema:** Goals non convertono
- Verifica i trigger del GTM
- Controlla i parametri degli event
- Usa le conversioni in tempo reale per debuggare

**Problema:** Errori negli script Python
- Verifica le credenziali di Google
- Assicurati che l'API sia abilitata
- Controlla il file `credentials.json`

## Prossimi Passi

- [ ] Implementare Event Tracking in GTM
- [ ] Creare Goals in GA4
- [ ] Configurare Segments
- [ ] Lanciare campagne UTM
- [ ] Monitorare Conversion Funnel
- [ ] Analizzare performance per segmento
- [ ] Ottimizzare based on data
- [ ] Creare custom reports

## Supporto

Per domande o problemi:
- 📧 Email: admin@artax-studio.it
- 📊 GA4 Property ID: [INSERT_YOUR_ID]
- 🔐 Repo Private: Si

## License

Private - Studio Legale Artax

---

**Last Updated:** November 18, 2025
**Version:** 1.0.0


## 📊 SEO OPTIMIZATION - DIRITTO TRIBUTARIO

### Overview
Il sistema include un'ottimizzazione SEO completa specializzata per studio legale tributario con focus su Torino e Nord Italia.

### Componenti SEO

#### 1. **Keyword Research** (`seo/seo_tax_law_keywords.json`)

**Keywords Primari (Traffico Alto):**
- `avvocato tributario Torino` (480 ricerche/mese) → Pagina servizi
- `consulenza fiscale aziendale` (640 ricerche/mese) → Alt difficoltà
- `diritto tributario Torino` (320 ricerche/mese) → Homepage
- `controversie tributarie` (210 ricerche/mese) → Servizi specifici

**Long-Tail Keywords (Facili - Content Opportunities):**
- `come calcolare le imposte aziendali` → Blog post
- `riduzione tasse per PMI 2025` → Guida pratica
- `deduzione fiscale spese aziendali` → Guide informative
- `regime forfetario vs regime ordinario` → Confronto post

**Local SEO:**
- Torino: 4 keywords ottimizzati
- Nord Italia: Milano, Genova, Bologna

#### 2. **Schema Markup** (`seo/schema_markup_tax_law.json`)

Implementa 6 tipi di schema JSON-LD:

1. **LegalService Schema** - Informazioni studio
2. **LocalBusiness Schema** - Localizzazione e orari
3. **Professional Schema** - Profili avvocati
4. **Service Schema** - Descrizione servizi
5. **FAQPage Schema** - Domande frequenti
6. **BreadcrumbList Schema** - Navigazione

**Implementazione:**
```html
<!-- Nel <head> di ogni pagina -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LegalService",
  "name": "Studio Legale Tributario Artax",
  "description": "Specializzato in diritto tributario...",
  "areaServed": ["Torino", "Piemonte", "Italia"]
}
</script>
```

#### 3. **SEO Monitoring Script** (`scripts/seo_monitoring.py`)

Automatizza:
- Analisi keyword performance
- Estrazione content opportunities
- Local SEO analysis
- Competitor benchmarking
- Content strategy calculation

**Utilizzo:**
```bash
python scripts/seo_monitoring.py
```

Output:
- Keyword ranking per priorità
- Content calendar con 4+ articoli
- Local SEO oppurtunità
- Strategy export in JSON

### Content Strategy (Auto-Generata)

| Tipo Contenuto | Keyword Focus | Num Articoli | Priorità |
|---|---|---|---|
| Blog Posts | Informational | 3 | HIGH |
| Guides | How-to | 1 | HIGH |
| Comparison | Regime fiscali | 1 | MEDIUM |
| Case Study | Pianificazione | Secondo metriche | MEDIUM |

### Integration con GA4

**Custom Events per SEO Tracking:**
```json
{
  "event_name": "keyword_ranking_tracked",
  "parameters": {
    "keyword": "avvocato tributario Torino",
    "ranking_position": 3,
    "search_volume": 480,
    "keyword_difficulty": "medium"
  }
}
```

**Metriche GA4 da Monitorare:**
- Organic sessions per keyword
- Conversion rate da search
- Bounce rate per landing page
- Time on page per servizio
- Ranking position vs traffico

### Local SEO Optimization

✅ **Torino Focus:**
- Google My Business completato
- Schema markup locale
- Keywords geo-targetizzati
- Citations locali (directory legali)
- Local link building

✅ **Nord Italia Expansion:**
- Milano: `avvocato tributario Milano`
- Genova: `studio legale tributario Genova`
- Bologna: `consulenza fiscale Bologna`

### Implementation Checklist

- [ ] Implementare Schema Markup JSON-LD
- [ ] Aggiungere keywords primari in meta description
- [ ] Creare 4+ articoli blog con long-tail keywords
- [ ] Lanciare seo_monitoring.py per estratto strategy
- [ ] Configurare GA4 event tracking per keywords
- [ ] Aggiornare Google My Business con schema
- [ ] Creare internal linking tra servizi
- [ ] Monitorare ranking keywords mensili
- [ ] A/B test titoli e meta descriptions
- [ ] Implementare sitemap.xml con priorità

### SEO Quick Wins

1. **Title Tags Ottimizzati:**
   - `Avvocato Tributario Torino | Consulenza Fiscale Specializzata | Artax`
   - `Controversie Tributarie | Ricorsi Amministrativi | Diritto Tributario`

2. **Meta Descriptions:**
   - 155-160 caratteri
   - Include keyword primario
   - Call-to-action (Contatta / Scopri)

3. **H1-H3 Structure:**
   - H1: Keyword principale + localizzazione
   - H2: Intent secondari (problemi che risolvi)
   - H3: Long-tail keywords

4. **Internal Linking:**
   - Homepage → Servizi tributari
   - Servizi → Blog correlati
   - Blog → Case study
   - Tutto → Contact CTA

### KPI SEO da Tracciare

| Metrica | Target | Frequenza |
|---------|--------|----------|
| Ranking Position | Top 3 per keyword primari | Settimanale |
| Organic Sessions | +50% MoM | Giornaliera |
| Organic CTR | >3% | Settimanale |
| Average Position | <5 per 10 keyword | Mensile |
| Indexed Pages | >100 | Mensile |

### Tools Consigliati

- **Google Search Console** - Ranking tracking
- **Screaming Frog** - Audit tecnico SEO
- **SEMrush/Ahrefs** - Competitor analysis
- **Google My Business** - Local SEO
- **Semrush Academy** - Learning

---

**SEO System Version:** 1.0
**Last Updated:** 2025-11-18
**Specialization:** Diritto Tributario IT
