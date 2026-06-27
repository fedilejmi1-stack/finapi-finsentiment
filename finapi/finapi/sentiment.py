"""Sentiment analysis using FinBERT."""

from transformers import pipeline

_classifier = pipeline(
    "sentiment-analysis",
    model="ProsusAI/finbert",
)


def analyze_sentiment(text: str) -> dict:
    result = _classifier(text[:512])[0]

    return {
        "label": result["label"].lower(),
        "score": round(float(result["score"]), 4),
    }


def analyze_batch(texts: list[str]) -> list[dict]:
    clean_texts = [text[:512] for text in texts if text and text.strip()]
    results = _classifier(clean_texts, batch_size=16)

    return [
        {
            "label": result["label"].lower(),
            "score": round(float(result["score"]), 4),
            "text_preview": text[:80],
        }
        for text, result in zip(clean_texts, results)
    ]