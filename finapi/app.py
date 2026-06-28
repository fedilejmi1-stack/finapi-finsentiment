"""Hugging Face Spaces entrypoint for FinSentiment.

This app bootstraps the database when needed and then runs the Streamlit
dashboard in embedded mode.
"""

import os
import runpy
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DASHBOARD_DIR = ROOT_DIR / "dashboard"

sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(DASHBOARD_DIR))


def bootstrap_data() -> None:
    """Populate the database with sample data if it is empty."""
    from finapi.db import SessionLocal, init_db
    from finapi.etl.news_etl import ingest_news
    from finapi.etl.prices_etl import ingest_prices
    from finapi.models import PriceRecord
    from scripts.enrich_sentiment import main as enrich_sentiment

    init_db()

    with SessionLocal() as session:
        if session.query(PriceRecord).count() > 0:
            print("Database already populated. Skipping bootstrap.")
            return

    print("Database empty. Starting bootstrap ETL...")

    tickers = os.getenv("TICKERS", "AAPL,MSFT,GOOGL,TSLA").split(",")

    for ticker in tickers:
        clean_ticker = ticker.strip().upper()

        if not clean_ticker:
            continue

        print(f"Bootstrapping {clean_ticker}...")
        ingest_prices(clean_ticker, period="1mo")
        ingest_news(clean_ticker)

    enrich_sentiment()
    print("Bootstrap completed.")


if os.getenv("BOOTSTRAP", "1") == "1":
    bootstrap_data()


runpy.run_path(str(DASHBOARD_DIR / "app.py"))