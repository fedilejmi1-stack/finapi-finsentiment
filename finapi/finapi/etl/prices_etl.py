"""ETL des prix : Extract via yfinance, Load dans SQLite."""

import logging

import yfinance as yf
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from finapi.db import SessionLocal
from finapi.models import PriceRecord

log = logging.getLogger(__name__)


def ingest_prices(ticker: str, period: str = "1mo") -> int:
    """Télécharge et stocke les prix. Idempotent."""
    log.info("ETL prices: fetching %s (period=%s)", ticker, period)

    data = yf.Ticker(ticker).history(period=period)

    if data.empty:
        log.warning("ETL prices: no data for %s", ticker)
        return 0

    rows = []

    for index, row in data.iterrows():
        close = row.get("Close")

        if close is None:
            continue

        rows.append(
            {
                "ticker": ticker.upper(),
                "date": index.date(),
                "close": float(close),
                "currency": "USD",
            }
        )

    if not rows:
        return 0

    with SessionLocal() as session:
        stmt = sqlite_insert(PriceRecord).values(rows)

        stmt = stmt.on_conflict_do_nothing(
            index_elements=["ticker", "date"],
        )

        result = session.execute(stmt)
        session.commit()

        inserted = result.rowcount or 0

    log.info("ETL prices: %s lignes insérées pour %s", inserted, ticker.upper())

    return inserted
