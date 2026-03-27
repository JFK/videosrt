import asyncio
import logging
from pathlib import Path

from src.config import settings

logger = logging.getLogger(__name__)


async def _run_ffmpeg(*args: str) -> bytes:
    """Run ffmpeg/ffprobe command and return stderr. Raises on failure."""
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg command failed: {stderr.decode()}")
    return stdout


async def extract_audio(mp4_path: Path, output_path: Path) -> float:
    """Extract audio from MP4 to WAV (16kHz mono). Returns duration in seconds."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    await _run_ffmpeg(
        "ffmpeg",
        "-i",
        str(mp4_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        "-y",
        str(output_path),
    )
    return await get_audio_duration(output_path)


async def extract_audio_mp3(mp4_path: Path, output_path: Path) -> float:
    """Extract audio from MP4 to MP3 (for Gemini). Returns duration in seconds."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    await _run_ffmpeg(
        "ffmpeg",
        "-i",
        str(mp4_path),
        "-vn",
        "-acodec",
        "libmp3lame",
        "-ar",
        "16000",
        "-ac",
        "1",
        "-q:a",
        "4",
        "-y",
        str(output_path),
    )
    return await get_audio_duration(output_path)


async def get_audio_duration(path: Path) -> float:
    """Get audio file duration in seconds."""
    stdout = await _run_ffmpeg(
        "ffprobe",
        "-v",
        "quiet",
        "-show_entries",
        "format=duration",
        "-of",
        "csv=p=0",
        str(path),
    )
    try:
        return float(stdout.decode().strip())
    except ValueError as e:
        raise RuntimeError(f"Could not parse audio duration from ffprobe output: {e}")


async def split_audio(audio_path: Path, chunk_duration_sec: int | None = None) -> list[Path]:
    """Split audio into chunks. Returns list of chunk paths."""
    if chunk_duration_sec is None:
        chunk_duration_sec = settings.whisper_chunk_duration_sec

    duration = await get_audio_duration(audio_path)
    if duration <= chunk_duration_sec:
        return [audio_path]

    chunks = []
    start = 0.0
    idx = 0
    while start < duration:
        chunk_path = audio_path.parent / f"{audio_path.stem}_chunk{idx:03d}{audio_path.suffix}"
        try:
            await _run_ffmpeg(
                "ffmpeg",
                "-i",
                str(audio_path),
                "-ss",
                str(start),
                "-t",
                str(chunk_duration_sec),
                "-y",
                str(chunk_path),
            )
            chunks.append(chunk_path)
        except RuntimeError:
            logger.warning("Failed to create chunk %d, skipping", idx)
        start += chunk_duration_sec
        idx += 1

    return chunks
