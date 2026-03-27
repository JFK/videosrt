from src.services.srt import (
    generate_srt,
    generate_vtt,
    parse_srt,
    seconds_to_srt_time,
    seconds_to_vtt_time,
    srt_time_to_seconds,
    srt_to_vtt,
)


def test_seconds_to_srt_time_zero():
    assert seconds_to_srt_time(0.0) == "00:00:00,000"


def test_seconds_to_srt_time_simple():
    assert seconds_to_srt_time(1.5) == "00:00:01,500"


def test_seconds_to_srt_time_minutes():
    assert seconds_to_srt_time(65.123) == "00:01:05,123"


def test_seconds_to_srt_time_hours():
    assert seconds_to_srt_time(3661.999) == "01:01:01,999"


def test_generate_srt(sample_segments):
    result = generate_srt(sample_segments)
    assert "00:00:00,000 --> 00:00:02,500" in result
    assert "00:00:03,000 --> 00:00:05,800" in result
    assert "Hello, welcome to the video." in result
    assert "Today we will discuss Python." in result


def test_generate_srt_skips_empty():
    segments = [
        {"start": 0.0, "end": 1.0, "text": "Hello"},
        {"start": 1.0, "end": 2.0, "text": "  "},
        {"start": 2.0, "end": 3.0, "text": "World"},
    ]
    result = generate_srt(segments)
    assert "1\n" in result
    assert "2\n" in result
    assert "3\n" not in result


def test_generate_srt_no_newlines_in_text():
    """SRT text should be clean single-line for editing software compatibility."""
    segments = [
        {"start": 0.0, "end": 5.0, "text": "This is a long sentence that should remain on one line without wrapping"},
    ]
    result = generate_srt(segments)
    text_line = result.strip().split("\n")[2]
    assert "\n" not in text_line
    assert text_line == "This is a long sentence that should remain on one line without wrapping"


# --- parse_srt tests ---


def test_srt_time_to_seconds():
    assert srt_time_to_seconds("00:00:00,000") == 0.0
    assert srt_time_to_seconds("00:00:01,500") == 1.5
    assert srt_time_to_seconds("01:01:01,999") == 3661.999


def test_srt_time_to_seconds_dot_separator():
    assert srt_time_to_seconds("00:00:01.500") == 1.5


def test_parse_srt_roundtrip():
    """generate_srt -> parse_srt should round-trip."""
    segments = [
        {"start": 0.0, "end": 2.5, "text": "Hello"},
        {"start": 3.0, "end": 5.8, "text": "World"},
    ]
    srt = generate_srt(segments)
    parsed = parse_srt(srt)
    assert len(parsed) == 2
    assert parsed[0]["text"] == "Hello"
    assert parsed[0]["start"] == 0.0
    assert parsed[0]["end"] == 2.5
    assert parsed[1]["text"] == "World"


def test_parse_srt_empty():
    assert parse_srt("") == []
    assert parse_srt("   ") == []


def test_parse_srt_skips_malformed():
    srt = "1\nnot a timestamp\nHello\n"
    result = parse_srt(srt)
    assert result == []


def test_parse_srt_multiline_text():
    srt = "1\n00:00:00,000 --> 00:00:02,000\nLine one\nLine two\n"
    result = parse_srt(srt)
    assert len(result) == 1
    assert result[0]["text"] == "Line one\nLine two"


# --- VTT tests ---


def test_seconds_to_vtt_time():
    assert seconds_to_vtt_time(0.0) == "00:00:00.000"
    assert seconds_to_vtt_time(1.5) == "00:00:01.500"
    assert seconds_to_vtt_time(3661.999) == "01:01:01.999"


def test_generate_vtt():
    segments = [
        {"start": 0.0, "end": 2.5, "text": "Hello"},
        {"start": 3.0, "end": 5.8, "text": "World"},
    ]
    result = generate_vtt(segments)
    assert result.startswith("WEBVTT\n")
    assert "00:00:00.000 --> 00:00:02.500" in result
    assert "00:00:03.000 --> 00:00:05.800" in result
    assert "Hello" in result
    assert "World" in result


def test_generate_vtt_skips_empty():
    segments = [
        {"start": 0.0, "end": 1.0, "text": "Hello"},
        {"start": 1.0, "end": 2.0, "text": "  "},
    ]
    result = generate_vtt(segments)
    assert "Hello" in result
    assert result.count("-->") == 1


def test_srt_to_vtt():
    srt = "1\n00:00:00,000 --> 00:00:02,500\nHello\n\n2\n00:00:03,000 --> 00:00:05,800\nWorld\n"
    result = srt_to_vtt(srt)
    assert result.startswith("WEBVTT\n")
    assert "00:00:00.000 --> 00:00:02.500" in result
    assert "," not in result.split("\n", 1)[1]  # No commas in timestamps
