---
description: API keys and secrets must be stored encrypted in DB via crypto.py. Never store plaintext secrets.
---

# Encrypted Settings Rule

## Pattern
1. User enters API key in Settings page
2. Backend encrypts with `crypto.encrypt()` (Fernet) before DB write
3. On use, decrypt with `crypto.decrypt()` just before API call
4. Never log or return decrypted keys in responses

## Key management
- `ENCRYPTION_KEY` env var is the only secret in `.env`
- All other secrets go through the Settings → encrypted DB flow

## When adding new API integrations
- Store credentials via the existing `Setting` model (key-value, encrypted)
- Never add new secrets to `.env` or hardcode in source
- Use `services/crypto.py` — do not create alternative encryption
