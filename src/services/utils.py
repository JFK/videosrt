import json
import logging

logger = logging.getLogger(__name__)


def strip_markdown_fence(text: str) -> str:
    """Remove markdown code block fences from LLM output."""
    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        # Remove opening fence (with optional language tag)
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        # Remove closing fence
        text = text[:-3].strip()
    return text


def parse_json_response(text: str, context: str = "") -> dict | list:
    """Strip markdown fences and parse JSON from LLM response."""
    cleaned = strip_markdown_fence(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in {context}: {e}. Response: {cleaned[:200]}")


def extract_gemini_tokens(response) -> tuple[int, int]:
    """Extract input/output token counts from Gemini response."""
    input_tokens = 0
    output_tokens = 0
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        input_tokens = getattr(response.usage_metadata, "prompt_token_count", 0) or 0
        output_tokens = getattr(response.usage_metadata, "candidates_token_count", 0) or 0
    return input_tokens, output_tokens
