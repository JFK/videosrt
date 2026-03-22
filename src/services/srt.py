from pathlib import Path


def seconds_to_srt_time(seconds: float) -> str:
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = round((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


MAX_LINE_CHARS = 26


def _wrap_text(text: str, max_chars: int = MAX_LINE_CHARS) -> str:
    """Wrap text into lines of max_chars for subtitle display."""
    if len(text) <= max_chars:
        return text

    lines = []
    current = ""
    for char in text:
        current += char
        if len(current) >= max_chars:
            # Try to break at punctuation or space
            break_pos = -1
            for i in range(len(current) - 1, max(len(current) - 6, -1), -1):
                if current[i] in "、。，．！？ ,. ":
                    break_pos = i + 1
                    break
            if break_pos > 0:
                lines.append(current[:break_pos].rstrip())
                current = current[break_pos:].lstrip()
            else:
                lines.append(current)
                current = ""

    if current.strip():
        lines.append(current.strip())

    return "\n".join(lines)


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
        lines.append(_wrap_text(text))
        lines.append("")
        idx += 1

    return "\n".join(lines)


def save_srt(content: str, output_path: Path) -> None:
    """Save SRT content to file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
