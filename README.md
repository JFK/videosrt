# VideoSRT

Generate SRT subtitle files from MP4 videos using AI transcription.

MP4動画からAI文字起こしでSRT字幕ファイルを生成するWebアプリケーション。

## Features

- **AI Transcription**: High-accuracy speech recognition via OpenAI Whisper API / Google Gemini API
- **SRT Generation**: Auto-generate timestamped SRT subtitle files
- **YouTube Metadata**: Auto-generate title, description (with chapter index), and tags
- **Video Editing**: Embed subtitles (with translucent highlight background) and logo overlay
- **Cost Dashboard**: Track API costs by provider, month, and operation
- **Web UI Settings**: Manage API keys and LLM models from the browser

## Quick Start

### Docker (Recommended)

```bash
# 1. Generate encryption key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# 2. Create .env file
cp .env.example .env
# Set ENCRYPTION_KEY with the generated key

# 3. Start
docker compose up --build

# 4. Open http://localhost:8000
# 5. Configure API keys in Settings
# 6. Upload an MP4 and generate subtitles
```

### Local Development

```bash
# Prerequisites: Python 3.11+, ffmpeg installed

pip install -e ".[dev]"

# Set up .env (see above)

uvicorn src.main:app --reload --port 8000
```

## Usage

### 1. Configure API Keys
Go to the Settings page and enter your OpenAI / Google API keys.

### 2. Upload MP4
On the Upload page, drag & drop or select an MP4 file. Choose a provider (Whisper/Gemini) and language, then upload.

### 3. Download SRT
On the History page, click the "SRT" button on completed jobs to download.

### 4. YouTube Metadata
Check "Generate YouTube metadata" during upload. View and copy the generated title, description (with chapter index), and tags from the "Meta" button on the History page.

### 5. Embed Subtitles
Click the "Embed" button on the History page to burn subtitles and/or a logo into the video.

## Provider Comparison

| | OpenAI Whisper | Google Gemini |
|---|---|---|
| Accuracy | High (dedicated ASR model) | High (multimodal LLM) |
| Timestamps | Precise (ASR-based) | Approximate (LLM-estimated) |
| Cost | $0.006/min | ~$0.002/min (2.5 Flash) |
| File Limit | 25MB (auto-chunking) | 9.5 hours |

## License

MIT License
