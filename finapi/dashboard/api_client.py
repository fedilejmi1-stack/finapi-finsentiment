"""Client HTTP for the Flask FinAPI."""

from typing import Any

import requests

API_BASE = "http://127.0.0.1:5000"


class APIError(Exception):
    """Custom error for API calls."""
    pass


def _get(path: str, **params) -> dict[str, Any]:
    try:
        response = requests.get(
            f"{API_BASE}{path}",
            params=params,
            timeout=10,
        )
    except requests.RequestException as e:
        raise APIError(f"API unreachable: {e}") from e

    if response.status_code != 200:
        raise APIError(f"{response.status_code}: {response.text[:200]}")

    return response.json()


def get_health() -> bool:
    try:
        return _get("/health").get("status") == "ok"
    except APIError:
        return False


def get_db_prices(ticker: str) -> list[dict]:
    return _get(f"/db/prices/{ticker}").get("prices", [])


def get_db_news(ticker: str) -> list[dict]:
    return _get(f"/db/news/{ticker}").get("news", [])


def get_sentiment_summary(ticker: str) -> dict[str, int]:
    return _get(f"/db/sentiment-summary/{ticker}").get("summary", {})