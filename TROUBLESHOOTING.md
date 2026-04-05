# Troubleshooting

Common errors and solutions for VoiceSRT.

## Setup & Startup

### `ENCRYPTION_KEY is not set`

The app requires a Fernet encryption key to store API keys securely.

```bash
# Generate a key
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Add to your `.env` file:

```
ENCRYPTION_KEY=<paste the generated key>
```

If using Docker:

```bash
cp .env.example .env
# Edit .env and paste the key
docker compose up --build
```

### Port already in use

```bash
# Change the port
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001

# Docker
HOST_PORT=8001 docker compose up --build
```

---

## API Keys & Providers

### `API key (api_key.openai) is not configured. Set it in Settings.`

Go to **Settings** page and enter your API key for the provider you want to use:
- **OpenAI**: Requires an API key from [platform.openai.com](https://platform.openai.com)
- **Google Gemini**: Requires an API key from [aistudio.google.com](https://aistudio.google.com)

### API key test fails

When testing a key in Settings, the app makes a small API call to verify it works. Common causes:

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Invalid API key" | Key is wrong or expired | Regenerate the key in provider's dashboard |
| Connection timeout | Network issue or firewall | Check internet access from the server |
| HTTP 429 | Rate limit exceeded | Wait and retry, or check your plan's quota |

### `Cannot connect to Ollama at {url}`

For local Ollama:
1. Ensure Ollama is running: `ollama serve`
2. Verify the base URL in Settings (default: `http://localhost:11434`)
3. In Docker, use `http://host.docker.internal:11434` instead of `localhost`

### `URL must be http:// or https:// with a valid host`

The Ollama base URL must start with `http://` or `https://`. Do not include trailing paths like `/api`.

---

## File Upload

### `Unsupported format`

Supported formats: **MP4, MP3, WAV, MOV, AVI, MKV, M4A, FLAC, OGG, WebM**

If your file has a different extension but is a valid audio/video format, convert it first:

```bash
ffmpeg -i input.aac -c copy output.m4a
```

### `File too large`

Default limit is 10 GB. To change it, update `max_upload_size_gb` in Settings.

### `Upload failed`

Check that the server has enough disk space. Uploaded files are stored in the `uploads/` directory.

---

## FFmpeg Errors

### `ffmpeg command failed`

FFmpeg is required for audio extraction. Install it:

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Verify
ffmpeg -version
```

If using Docker, ffmpeg is included in the container — no action needed.

### `Could not parse audio duration`

The file may be corrupted or in an unsupported codec. Try re-encoding:

```bash
ffmpeg -i input.mp4 -c:a aac -c:v copy output.mp4
```

---

## Transcription

### Job stuck in "processing"

1. Check server logs for errors
2. Gemini transcription has a 10-minute timeout — long files may hit this
3. If the job is stuck, it can be safely deleted and retried

### `Invalid JSON in Gemini transcription`

LLMs occasionally return malformed JSON. VoiceSRT auto-repairs truncated JSON when possible. If it fails:
- Retry the transcription — LLM outputs are non-deterministic
- Try a different model or provider
- For very long files, the response may be truncated by token limits

### Whisper prompt truncated warning

Whisper has an 800-character prompt limit. If your glossary is very long, some terms may be cut. To work around this:
- Put the most important terms first in the glossary
- Use shorter glossary entries
- Consider using Gemini for files with many specialized terms

---

## Refinement & Verification

### `Refinement failed`

Refinement is **non-fatal** — the job continues with the raw transcription. Common causes:
- API rate limits
- Model temporarily unavailable
- Response too large for the model's output limit

The error is shown in the job detail page. You can still edit the SRT manually.

### `Cannot find segments array in response`

The LLM returned JSON in an unexpected format. Retry the job — this is usually a one-time LLM output issue.

### Refine modes

| Mode | Use case |
|------|----------|
| `verbatim` | Keep filler words, stutters — for legal/research transcripts |
| `standard` | Clean up speech naturally — default for most content |
| `caption` | Short, readable segments — for YouTube subtitles |

---

## SRT Editor

### `No SRT file available`

The job must complete transcription before you can edit, generate metadata, or download. Wait for the job to finish.

### `Segment N: start must be before end`

Each segment's start time must be earlier than its end time. Check for typos in the time fields.

### `Segment N: overlaps with previous segment`

Segments must not overlap in time. Adjust the end time of the previous segment or the start time of the current one.

### Glossary too long

Glossary is limited to 5,000 characters. If you need more terms, prioritize the most commonly misrecognized words.

---

## Metadata & Quiz Generation

### Metadata generation failed

Metadata, catchphrase, and quiz generation are **non-fatal** — they don't affect your SRT. Common causes:
- API key quota exhausted
- Model returned unparseable response

Retry from the job detail page, or generate metadata manually.

---

## Docker-Specific Issues

### Container can't reach Ollama

Use `host.docker.internal` instead of `localhost`:

```
Ollama Base URL: http://host.docker.internal:11434
```

On Linux, you may need `--add-host=host.docker.internal:host-gateway` in your Docker command, or add it to `docker-compose.yml`.

### Files persist after container restart?

Uploads and the SQLite database are stored in Docker volumes. To reset:

```bash
docker compose down -v   # Warning: deletes all data
docker compose up --build
```

---

## Getting Help

If your issue isn't listed here:

1. Check the server logs (terminal output or `docker compose logs`)
2. Open an issue on [GitHub](https://github.com/JFK/voicesrt/issues) with:
   - Steps to reproduce
   - Error message (from UI or logs)
   - Provider and model used
   - File format and approximate size
