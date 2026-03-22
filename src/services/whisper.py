from pathlib import Path
from typing import Any

import logging

import openai

logger = logging.getLogger(__name__)


async def transcribe_with_whisper(
    audio_path: Path,
    api_key: str,
    language: str | None = None,
) -> list[dict]:
    """Transcribe audio using OpenAI Whisper API.

    Returns list of segments: [{"start": float, "end": float, "text": str}, ...]
    """
    client = openai.AsyncOpenAI(api_key=api_key)

    kwargs: dict[str, Any] = {
        "model": "whisper-1",
        "response_format": "verbose_json",
        "timestamp_granularities": ["segment"],
    }
    if language:
        kwargs["language"] = language

    with open(audio_path, "rb") as f:
        kwargs["file"] = f
        response = await client.audio.transcriptions.create(**kwargs)

    segments = []
    raw_segments = getattr(response, "segments", None)
    logger.debug("Whisper response type: %s, segments type: %s", type(response).__name__, type(raw_segments).__name__ if raw_segments else "None")
    for seg in (raw_segments or []):
        logger.debug("Segment type: %s, value: %s", type(seg).__name__, repr(seg)[:200])
        if isinstance(seg, dict):
            segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip(),
            })
        else:
            segments.append({
                "start": seg.start,
                "end": seg.end,
                "text": seg.text.strip(),
            })

    return segments
