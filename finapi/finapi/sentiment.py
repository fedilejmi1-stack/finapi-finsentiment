"""Sentiment analysis using FinBERT."""

from functools import lru_cache

from transformers import pipeline


@lru_cache(maxsize=1)
def get_classifier():
    """Load the FinBERT model only once."""
    return pipeline(
        "sentiment-analysis",
        model="ProsusAI/finbert",
    )


def analyze_sentiment(text: str) -> dict:
    """Analyze the sentiment of a single text."""
    result = get_classifier()(text[:512])[0]

    return {
        "label": result["label"].lower(),
        "score": round(float(result["score"]), 4),
    }


def analyze_batch(texts: list[str]) -> list[dict]:
    """Analyze the sentiment of multiple texts."""
    clean_texts = [text[:512] for text in texts if text and text.strip()]

    results = get_classifier()(clean_texts, batch_size=16)

    return [
        {
            "label": result["label"].lower(),
            "score": round(float(result["score"]), 4),
            "text_preview": text[:80],
        }
        for text, result in zip(clean_texts, results)
    ]