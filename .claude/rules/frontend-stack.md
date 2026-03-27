---
description: Frontend uses HTMX + Alpine.js + Jinja2 + Tailwind CDN. Do not introduce React, Vue, or other SPA frameworks.
---

# Frontend Stack Rule

## Stack
- **Templates**: Jinja2 (server-rendered)
- **Interactivity**: HTMX 2.x for server-driven updates, Alpine.js 3.x for client-side state
- **Styling**: Tailwind CSS via CDN
- **i18n**: JSON-based (en.json, ja.json), Jinja filter `t('key.subkey')`, fallback to English

## HTMX patterns
- Polling: `hx-trigger="every 3s"` for job status
- Delete: `hx-delete` + `hx-confirm` + `hx-target` + `hx-swap="delete"`
- AJAX detection: global HTMX header set in base.html

## Alpine.js patterns
- Form state: `x-data="formName()"` with function defined in `<script>` block
- Conditional UI: `x-show`, two-way binding: `x-model`
- Events: `@submit.prevent`, `@click`, `@change`

## Do NOT
- Add npm/yarn dependencies or build steps
- Use JSX, TypeScript, or module bundlers
- Import JS frameworks via npm — CDN only
