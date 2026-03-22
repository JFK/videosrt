# VoiceSRT

Generate SRT subtitle files from video/audio using AI transcription.

動画・音声ファイルからAI文字起こしでSRT字幕ファイルを生成するWebアプリケーション。

## Features

- **AI Transcription**: High-accuracy speech recognition via OpenAI Whisper API / Google Gemini API
- **Multi-format Support**: MP4, MP3, WAV, MOV, AVI, MKV, M4A, FLAC, OGG, WebM
- **SRT Generation**: Auto-generate timestamped SRT subtitle files
- **LLM Post-processing**: Fix proper nouns, punctuation, fillers with glossary support
- **YouTube Metadata**: Auto-generate title, description (with chapter index), and tags
- **YouTube Quiz**: Auto-generate quiz questions from video content
- **Cost Dashboard**: Track API costs by provider, month, and operation
- **Web UI Settings**: Manage API keys, LLM models, and glossary from the browser

## Quick Start

### With Claude Code (Recommended)

```bash
git clone https://github.com/JFK/voicesrt.git
cd voicesrt
claude
# Then tell Claude: "Set up this project"
```

Claude Code will read `CLAUDE.md` and handle the full setup automatically.

### Manual Setup

```bash
# Prerequisites: Python 3.11+, ffmpeg

pip install -e ".[dev]"

# Generate encryption key and create .env
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
cp .env.example .env
# Set ENCRYPTION_KEY in .env

uvicorn src.main:app --reload --port 8000
# Open http://localhost:8000 → Settings → Configure API keys
```

### Docker

```bash
cp .env.example .env
# Set ENCRYPTION_KEY in .env
docker compose up --build
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


## Provider Comparison

| | OpenAI Whisper | Google Gemini |
|---|---|---|
| Accuracy | High (dedicated ASR model) | High (multimodal LLM) |
| Timestamps | Precise (ASR-based) | Approximate (LLM-estimated) |
| Cost | $0.006/min | ~$0.0005/min (3.1 Flash Lite) |
| File Limit | 25MB (auto-chunking) | 9.5 hours |

## License

MIT License
