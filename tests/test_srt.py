from src.services.srt import _wrap_text, generate_srt, seconds_to_srt_time


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
    assert "Hello" in result
    assert "Python" in result


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


def test_wrap_text_short():
    assert _wrap_text("短いテキスト") == "短いテキスト"


def test_wrap_text_long():
    text = "これは非常に長いテキストで、字幕として表示するには改行が必要です。"
    result = _wrap_text(text)
    lines = result.split("\n")
    assert len(lines) >= 2
    for line in lines:
        assert len(line) <= 30  # some tolerance for break position


def test_wrap_text_exact_limit():
    text = "a" * 26
    assert _wrap_text(text) == text


def test_wrap_text_with_punctuation():
    text = "今日は天気がいいですね、明日も晴れるといいですね。これは長いです。"
    result = _wrap_text(text)
    lines = result.split("\n")
    assert len(lines) >= 2
