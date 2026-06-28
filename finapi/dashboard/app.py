"""Interactive financial sentiment dashboard."""

from datetime import datetime

import streamlit as st

import api_client as api
from charts import SENT_COLORS, price_line_chart, sentiment_pie_chart


st.set_page_config(
    page_title="FinSentiment Dashboard",
    page_icon="📈",
    layout="wide",
)


with st.sidebar:
    st.title("Controls")
    st.caption("Configure your dashboard view.")

    api_ok = api.get_health()

    if api_ok:
        st.success("API connected")
    else:
        st.error("API unreachable")
        st.info("Start Flask in another terminal: python -m finapi.app")
        st.stop()

    ticker = st.selectbox(
        "Ticker",
        ["AAPL", "MSFT", "GOOGL"],
    )

    if st.button("Refresh now"):
        st.cache_data.clear()
        st.rerun()


st.title(f"📈 FinSentiment - {ticker}")
st.caption("Interactive dashboard: prices, financial news, and FinBERT sentiment")


@st.cache_data(ttl=60)
def load_prices(t: str):
    return api.get_db_prices(t)


@st.cache_data(ttl=60)
def load_news(t: str):
    return api.get_db_news(t)


@st.cache_data(ttl=60)
def load_summary(t: str):
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