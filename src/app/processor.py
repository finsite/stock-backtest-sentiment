"""
Processor module for stock-backtest-sentiment signal generation.

Validates incoming messages and computes a sentiment-based trading signal.
Sentiment may come from news, social media, or NLP scores.
"""

from typing import Any

from app.utils.setup_logger import setup_logger
from app.utils.types import ValidatedMessage
from app.utils.validate_data import validate_message_schema

logger = setup_logger(__name__)


def validate_input_message(message: dict[str, Any]) -> ValidatedMessage:
    """
    Validate the incoming raw message against the expected schema.

    Args:
        message (dict[str, Any]): Raw input message.

    Returns:
        ValidatedMessage: A validated message object.

    Raises:
        ValueError: If the input format is invalid.
    """
    logger.debug("🔍 Validating message schema...")
    if not validate_message_schema(message):
        logger.error("❌ Invalid message schema: %s", message)
        raise ValueError("Invalid message format")
    return message  # type: ignore[return-value]


def compute_sentiment_signal(message: ValidatedMessage) -> dict[str, Any]:
    """
    Compute a sentiment-based signal using a placeholder sentiment score.

    Args:
        message (ValidatedMessage): The validated input data.

    Returns:
        dict[str, Any]: Enriched message with sentiment score and signal.
    """
    symbol = message.get("symbol", "UNKNOWN")
    sentiment_score = float(message.get("sentiment_score", 0.0))  # Typically -1.0 to +1.0

    logger.info("🗣️ Computing sentiment signal for %s", symbol)

    if sentiment_score >= 0.3:
        signal = "BUY"
    elif sentiment_score <= -0.3:
        signal = "SELL"
    else:
        signal = "HOLD"

    result = {
        "sentiment_signal": signal,
        "sentiment_score": round(sentiment_score, 4),
    }

    logger.debug("🧠 Sentiment result for %s: %s", symbol, result)
    return {**message, **result}
