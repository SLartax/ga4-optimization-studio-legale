#!/usr/bin/env python3
# GA4 Analytics API Client
# Interagisce direttamente con l'API di Google Analytics 4

import json
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    Filter,
    FilterExpression,
    OrderBy,
)
from datetime import datetime, timedelta
import pandas as pd

class GA4Client:
    def __init__(self, property_id: str, credentials_path: str = None):
        """
        Inizializza il client GA4.
        
        Args:
            property_id: ID della property GA4
            credentials_path: Path al file JSON di credenziali Google
        """
        self.property_id = property_id
        self.client = BetaAnalyticsDataClient()
        
    def get_conversion_report(self, days_back: int = 7) -> pd.DataFrame:
        """
        Recupera report conversioni dell'ultimo periodo.
        
        Args:
            days_back: Numero di giorni nel passato
            
        Returns:
            DataFrame con dati di conversione
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[
                DateRange(
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat(),
                )
            ],
            dimensions=[Dimension(name="eventName")],
            metrics=[
                Metric(name="eventCount"),
                Metric(name="userCount"),
            ],
            dimension_filter=FilterExpression(
                filter=Filter(
                    field_name="eventName",
                    string_filter={"match_type": 1, "value": "form_contact_submitted"},
                )
            ),
        )
        
        response = self.client.run_report(request)
        return self._convert_to_dataframe(response)
    
    def get_traffic_by_source(self, days_back: int = 7) -> pd.DataFrame:
        """
        Recupera traffico raggruppato per fonte.
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[
                DateRange(
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat(),
                )
            ],
            dimensions=[Dimension(name="source"), Dimension(name="medium")],
            metrics=[Metric(name="sessions"), Metric(name="users")],
            order_bys=[OrderBy(metric={"metric_name": "sessions"})],
        )
        
        response = self.client.run_report(request)
        return self._convert_to_dataframe(response)
    
    def get_user_segments_data(self, segment_name: str, days_back: int = 7) -> pd.DataFrame:
        """
        Recupera dati per un segmento utente specifico.
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        # Mapping segment conditions (semplificato)
        filters = self._get_segment_filter(segment_name)
        
        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            date_ranges=[DateRange(start_date=start_date.isoformat(), end_date=end_date.isoformat())],
            dimensions=[Dimension(name="country"), Dimension(name="city")],
            metrics=[Metric(name="users"), Metric(name="sessions")],
            dimension_filter=filters,
        )
        
        response = self.client.run_report(request)
        return self._convert_to_dataframe(response)
    
    def _get_segment_filter(self, segment_name: str) -> FilterExpression:
        """
        Costruisce il filtro per il segmento.
        """
        filters_map = {
            "high_value_leads": self._high_value_leads_filter(),
            "mobile_users": self._mobile_users_filter(),
            "local_traffic": self._local_traffic_filter(),
        }
        return filters_map.get(segment_name, None)
    
    def _high_value_leads_filter(self) -> FilterExpression:
        return FilterExpression(
            filter=Filter(
                field_name="eventName",
                string_filter={"match_type": 1, "value": "form_contact_submitted"},
            )
        )
    
    def _mobile_users_filter(self) -> FilterExpression:
        return FilterExpression(
            filter=Filter(
                field_name="deviceCategory",
                string_filter={"match_type": 1, "value": "mobile"},
            )
        )
    
    def _local_traffic_filter(self) -> FilterExpression:
        return FilterExpression(
            filter=Filter(
                field_name="country",
                string_filter={"match_type": 1, "value": "Italy"},
            )
        )
    
    def _convert_to_dataframe(self, response) -> pd.DataFrame:
        """
        Converte risposta API in DataFrame.
        """
        data = []
        for row in response.rows:
            row_data = {}
            for i, header in enumerate(response.dimension_headers):
                row_data[header.name] = row.dimension_values[i].value
            for i, header in enumerate(response.metric_headers):
                row_data[header.name] = row.metric_values[i].value
            data.append(row_data)
        return pd.DataFrame(data)

if __name__ == "__main__":
    # Esempio di utilizzo
    PROPERTY_ID = "YOUR_GA4_PROPERTY_ID"
    client = GA4Client(PROPERTY_ID)
    
    # Recupera conversioni
    conversions = client.get_conversion_report(days_back=7)
    print("\nConversioni ultimi 7 giorni:")
    print(conversions)
    
    # Recupera traffico per fonte
    traffic = client.get_traffic_by_source(days_back=7)
    print("\nTraffico per fonte:")
    print(traffic)
