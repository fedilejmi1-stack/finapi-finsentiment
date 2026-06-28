"""Access to market data via yfinance."""

from dataclasses import dataclass
from datetime import date

import yfinance as yf


class TickerNotFoundError(Exception):
    """Raised when no data is found for a ticker."""


@dataclass
class LatestPrice:
    ticker: str
    date: date
    close: float
    currency: str


def get_latest_price(ticker: str) -> LatestPrice:
    """Return the latest closing price."""

    yf_ticker = yf.Ticker(ticker)
    history = yf_ticker.history(period="5d", auto_adjust=False)

    if history.empty:
        raise TickerNotFoundError(f"Ticker '{ticker}' introuvable")

    last_row = history.iloc[-1]
    last_date = history.index[-1].date()

    try:
        currency = yf_ticker.info.get("currency", "USD") or "USD"
    except Exception:
        currency = "USD"

    return LatestPrice(
        ticker=ticker.upper(),
        date=last_date,
        close=round(float(last_row["Close"]), 2),
        currency=currency.upper(),
    )


@dataclass
class PricePoint:
    date: date
    close: float


def get_history(ticker: str, days: int) -> list[PricePoint]:
    period = f"{max(days, 1)}d"
    history = yf.Ticker(ticker).history(period=period, auto_adjust=False)

    if history.empty:
        raise TickerNotFoundError(f"Ticker '{ticker}' introuvable")

    history = history.dropna(subset=["Close"])

    return [
        PricePoint(date=ts.date(), close=round(float(close), 2))
        for ts, close in history["Close"].items()
    ]
