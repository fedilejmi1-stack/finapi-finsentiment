"""Interactive financial sentiment dashboard."""

import os
from datetime import datetime

import api_client as api
import streamlit as st
from charts import SENT_COLORS, price_line_chart, sentiment_pie_chart

st.set_page_config(
    page_title="FinSentiment Dashboard",
    page_icon="📈",
    layout="wide",
)


with st.sidebar:
    st.title("Controls")
    st.caption("Configure your dashboard view.")

    page = st.radio("Page", ["Dashboard", "About"])

    api_ok = api.get_health()

    if api_ok:
        st.success("API connected")
    else:
        st.error("API unreachable")
        st.info("Start Flask in another terminal: python -m finapi.app")
        st.stop()

    default_tickers = [
        ticker.strip().upper()
        for ticker in os.getenv("TICKERS", "AAPL,MSFT,GOOGL,TSLA").split(",")
        if ticker.strip()
    ]

    db_tickers = api.get_db_stats().get("tickers", [])
    ticker_options = db_tickers or default_tickers

    ticker = st.selectbox("Ticker", ticker_options)

    if st.button("Refresh now"):
        st.cache_data.clear()
        st.rerun()


if page == "About":
    st.title("About FinSentiment")
    st.markdown(
        """
        FinSentiment is a financial sentiment dashboard built across six applied labs.

        It combines:

        - Flask API backend
        - SQLite database
        - yfinance ETL pipeline
        - FinBERT sentiment analysis
        - Streamlit dashboard
        - Pytest, coverage, Ruff, and GitHub Actions CI
        - Public deployment on Hugging Face Spaces

        **GitHub repository:**  
        https://github.com/fedilejmi1-stack/finapi-finsentiment

        **Public Hugging Face Space:**  
        https://huggingface.co/spaces/FediLejmi1/finsentiment
        """
    )
    st.stop()


st.title(f"📈 FinSentiment - {ticker}")
st.caption("Interactive dashboard: prices, financial news, and FinBERT sentiment")


@st.cache_data(ttl=60)
def load_prices(t: str) -> list[dict]:
    """Load stored prices for a ticker."""
    return api.get_db_prices(t)


@st.cache_data(ttl=60)
def load_news(t: str) -> list[dict]:
    """Load stored news for a ticker."""
    return api.get_db_news(t)


@st.cache_data(ttl=60)
def load_summary(t: str) -> dict[str, int]:
    """Load sentiment summary for a ticker."""
    return api.get_sentiment_summary(t)


prices = load_prices(ticker)
news = load_news(ticker)
sentiment = load_summary(ticker)


col1, col2, col3, col4 = st.columns(4)

if prices:
    last = prices[0]
    prev = prices[1] if len(prices) > 1 else last
    delta = last["close"] - prev["close"]

    col1.metric("Last close", f"{last['close']:.2f}", f"{delta:+.2f}")
    col2.metric("Date", last["date"])
else:
    col1.metric("Last close", "N/A")
    col2.metric("Date", "N/A")

col3.metric("Stored news", len(news))

total_sentiment = sum(sentiment.values()) or 1
positive_share = sentiment.get("positive", 0) / total_sentiment * 100
col4.metric("Positive sentiment", f"{positive_share:.0f}%")

st.divider()

chart_col, sentiment_col = st.columns([2, 1])

with chart_col:
    st.subheader("Price evolution")
    st.plotly_chart(price_line_chart(prices), use_container_width=True)

with sentiment_col:
    st.subheader("Sentiment distribution")

    if sentiment:
        st.plotly_chart(sentiment_pie_chart(sentiment), use_container_width=True)
    else:
        st.info("No sentiment available. Run enrich_sentiment.py first.")

st.divider()

st.subheader(f"Latest news - {ticker}")

if not news:
    st.info("No news found in database.")
else:
    for item in news[:15]:
        sent = item.get("sentiment_label") or "neutral"
        color = SENT_COLORS.get(sent, "#94A3B8")

        st.markdown(
            f"""
            <div style="
                border-left: 5px solid {color};
                padding: 10px 14px;
                margin: 8px 0;
                background: #F8FAFC;
                border-radius: 6px;
            ">
                <b>{item.get("title", "")}</b><br>
                <small style="color:#64748B;">
                    {item.get("publisher", "")} |
                    {item.get("published_at", "")[:16]} |
                    <span style="color:{color}; font-weight:bold;">
                        {sent.upper()}
                    </span>
                </small>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()
st.caption(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")