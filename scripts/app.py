#!/usr/bin/env python3
"""Entry point for Streamlit trading dashboard"""

import os
import sys

# Aggiungi il path dello script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importa e avvia trading_dashboard
if __name__ == '__main__':
    from trading_dashboard import *
