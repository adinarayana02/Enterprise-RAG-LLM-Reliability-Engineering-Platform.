"""
utils/token_counter.py
-----------------------
Approximate token counting and cost estimation.

Gemini does not use the same tokenizer as OpenAI, so tiktoken is only an
approximation (~4 characters per token is the industry-standard heuristic
used here as a fallback if tiktoken isn't available). This powers the
"Token Usage Dashboard" / "Cost Estimation" bonus features.
"""

from typing import Optional

try:
    import tiktoken
    _ENCODER = tiktoken.get_encoding("cl100k_base")
except Exception:  # pragma: no cover - fallback if tiktoken/model not available
    _ENCODER = None

# Rough public pricing reference for Gemini 1.5 Flash (USD per 1K tokens).
# These are estimates only, meant for a rough in-app cost dashboard.
PRICE_PER_1K_INPUT = 0.000075
PRICE_PER_1K_OUTPUT = 0.0003


def count_tokens(text: str) -> int:
    """Estimate the number of tokens in a string of text."""
    if not text:
        return 0
    if _ENCODER is not None:
        try:
            return len(_ENCODER.encode(text))
        except Exception:
            pass
    # Fallback heuristic: ~4 characters per token.
    return max(1, len(text) // 4)


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    """Rough USD cost estimate for a single request."""
    return round(
        (input_tokens / 1000) * PRICE_PER_1K_INPUT
        + (output_tokens / 1000) * PRICE_PER_1K_OUTPUT,
        6,
    )


class UsageTracker:
    """
    In-memory running total of token usage for the session.

    A simple singleton-style tracker used to power the token usage dashboard.
    Not persisted across restarts by design (keeps things simple/stateless).
    """

    def __init__(self) -> None:
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_requests = 0

    def record(self, input_tokens: int, output_tokens: int) -> None:
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_requests += 1

    def summary(self) -> dict:
        cost = estimate_cost(self.total_input_tokens, self.total_output_tokens)
        return {
            "total_requests": self.total_requests,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "estimated_cost_usd": cost,
        }


# Shared instance imported by services/routes.
usage_tracker = UsageTracker()
