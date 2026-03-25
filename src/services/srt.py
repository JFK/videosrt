import re
from pathlib import Path


def srt_time_to_seconds(time_str: str) -> float:
    """Convert SRT timestamp (HH:MM:SS,mmm) to seconds."""
    match = re.match(r"(\d+):(\d+):(\d+)[,.](\d+)", time_str.strip())
    if not match:
        raise ValueError(f"Invalid SRT timestamp: {time_str}")
    h, m, s, ms = match.groups()
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def seconds_to_srt_time(seconds: float) -> str:
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = round((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def generate_srt(segments: list[dict]) -> str:
    """Generate SRT content from segments.

    Each segment: {"start": float, "end": float, "text": str}
    """
    lines = []
    idx = 1
    for seg in segments:
        text = seg["text"].strip()
        if not text:
            continue
        start = seconds_to_srt_time(seg["start"])
        end = seconds_to_srt_time(seg["end"])
        lines.append(str(idx))
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")
        idx += 1

    return "\n".join(lines)


def parse_srt(content: str) -> list[dict]:
    """Parse SRT content into segment dicts.

    Returns list of {"start": float, "end": float, "text": str}.
    """
    segments: list[dict] = []
    blocks = re.split(r"\n\s*\n", content.strip())
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 2:
            continue
        # Find the timestamp line (contains " --> ")
        ts_idx = None
        for i, line in enumerate(lines):
            if " --> " in line:
                ts_idx = i
                break
        if ts_idx is None:
            continue
        ts_parts = lines[ts_idx].split(" --> ")
        if len(ts_parts) != 2:
            continue
        try:
            start = srt_time_to_seconds(ts_parts[0])
            end = srt_time_to_seconds(ts_parts[1])
        except ValueError:
            continue
        text = "\n".join(lines[ts_idx + 1:]).strip()
        if text:
            segments.append({"start": start, "end": end, "text": text})
    return segments


def save_srt(content: str, output_path: Path) -> None:
    """Save SRT content to file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
