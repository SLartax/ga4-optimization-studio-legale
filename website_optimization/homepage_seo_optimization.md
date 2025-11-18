# Ottimizzazione Homepage - Studio Legale Artax

## Analisi Stato Attuale
- **Title Tag**: "Avvocati Tributaristi - Tributi | Studio Legale Artax sta sas" ✓ Buono
- **Meta Description**: NON PRESENTE - PRIORITARIO
- **H1**: "AVVOCATI TRIBUTARISTI" - Troppo generico
- **Contenuti**: Focalizzati su Rottamazione Quinquies, ma mancano keyword target principali
- **Schema Markup**: NON IMPLEMENTATO
- **GA4 Tracking**: NON PRESENTE
- **Internal Linking**: Debole, non ottimizzato per keyword

## Quick Wins da Implementare (0-2 settimane)

### 1. Meta Description (Impatto: ALTO)
**Keyword Target**: Rottamazione Quinquies 2025, Avvocato Tributario Torino
```
<meta name="description" content="Studio Legale Tributario Artax - Rottamazione Quinquies, Cartella Esattoriale, Consulenza Fiscale a Torino. Esperti in diritto tributario e contenzioso esattoriale.">
```
- Length: 155 characters ✓
- Keyword: Rottamazione Quinquies, Avvocato Tributario
- CTA: Implicitamente invita al click

### 2. H1 Tag Ottimizzato
**Attuale**: "AVVOCATI TRIBUTARISTI"
**Ottimizzato**: "Avvocati Tributaristi Esperti in Rottamazione Quinquies e Contenzioso Esattoriale - Torino"
- Include keyword principale (Rottamazione Quinquies)
- Include variante locale (Torino)
- Include servizio principale (Contenzioso Esattoriale)

### 3. Aggiungi H2 con Keyword Long-Tail
```
<h2>Cartella Esattoriale: Come Difendersi e Cosa Fare</h2>
<h2>Rottamazione Quinquies 2025: Guida Completa e Scadenze</h2>
<h2>Avvocato Tributario Torino: Consulenza Fiscale Specializzata</h2>
```

### 4. Alt Text Ottimizzati per Immagini
- Logo/Banner: "Studio Legale Artax - Avvocati Tributaristi Torino"
- Team photo: "Team di Avvocati Tributaristi Esperti - Studio Legale Artax"

### 5. Internal Linking Strategy
```
Homepage -> Cosa Facciamo/Contenzioso Esattoriale (anchor: "cartella esattoriale")
Homepage -> Blog/Rottamazione Quinquies (anchor: "rottamazione quinquies 2025")
Homepage -> Chi Siamo (anchor: "avvocati tributaristi")
Homepage -> Contattaci (anchor: "consulenza fiscale")
```

## Fase 2: Content Enrichment (2-4 settimane)

### 1. Aggiungi FAQ Schema JSON-LD
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Che cos'è la Rottamazione Quinquies?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "La Rottamazione Quinquies è una sanatoria per debiti tributari affidati all'Agenzia delle Entrate Riscossione dal 2000 al 2023, con pagamento in 54 rate bimestrali."
      }
    },
    {
      "@type": "Question",
      "name": "Cosa fare se ricevo una cartella esattoriale?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Contattare immediatamente uno studio legale specializzato. Hai 60 giorni per ricorso. Lo Studio Legale Artax offre consulenza gratuita per cartelle esattoriali."
      }
    }
  ]
}
```

### 2. Aggiungi LocalBusiness Schema JSON-LD
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Studio Legale Artax",
  "description": "Studio legale specializzato in diritto tributario, rottamazione quinquies, contenzioso esattoriale",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Via Botticelli, 80",
    "addressLocality": "Torino",
    "postalCode": "10154",
    "addressCountry": "IT"
  },
  "telephone": "+39 011 24 65 228",
  "email": "studiolegaleartax@gmail.com",
  "priceRange": "$$",
  "sameAs": [
    "https://www.facebook.com/artax.studiolegale",
    "https://twitter.com/StudiolegaleAr1",
    "https://www.linkedin.com/company/studio-legale-artax"
  ]
}
```

### 3. Aggiungi ProfessionalService Schema JSON-LD
```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Consulenza Tributaria - Studio Legale Artax",
  "areaServed": {
    "@type": "City",
    "name": "Torino"
  },
  "availableLanguage": "it",
  "knowsAbout": [
    "Rottamazione Quinquies",
    "Cartella Esattoriale",
    "Contenzioso Tributario",
    "Consulenza Fiscale",
    "Verifiche GDF"
  ]
}
```

## Fase 3: Tracking & Monitoring (Continuo)

### GA4 Events da Implementare
```javascript
// Homepage Click Events
gtag('event', 'click_cosa_facciamo', {
  'event_category': 'engagement',
  'event_label': 'homepage_link'
});

gtag('event', 'click_contattaci', {
  'event_category': 'conversion',
  'event_label': 'contact_intent'
});

gtag('event', 'scroll_depth_50', {
  'event_category': 'engagement',
  'event_label': 'homepage',
  'scroll_depth': '50'
});
```

### UTM Parameters per Campagne
```
Homepage QR Code: ?utm_source=print&utm_medium=qr&utm_campaign=studio_branding
Social Media: ?utm_source=facebook&utm_medium=social&utm_campaign=rottamazione_2025
Email Newsletter: ?utm_source=email&utm_medium=newsletter&utm_campaign=news
```

## Priorità di Implementazione

1. ⚡ **URGENTE** (Settimana 1):
   - Meta Description
   - H1 Tag Ottimizzato
   - H2 Tags con Long-Tail Keywords
   - Internal Linking Strategy

2. 📊 **IMPORTANTE** (Settimana 2-3):
   - Schema Markup JSON-LD (FAQ, LocalBusiness, ProfessionalService)
   - GA4 Event Tracking
   - UTM Parameters Setup

3. 📈 **OTTIMIZZAZIONE** (Settimana 4+):
   - Blog Content Creation per Long-Tail Keywords
   - Backlink Building Strategy
   - Competitor Monitoring

## Expected Results
- **Week 1-2**: Miglioramento CTR da Google SERP (+15-20%)
- **Week 2-4**: Aumento traffico organico (+10-15%)
- **Month 1-2**: Posizionamento Top 10 per keyword "cartella esattoriale cosa fare"
- **Month 3-6**: Top 3 ranking per "rottamazione quinquies 2025"
