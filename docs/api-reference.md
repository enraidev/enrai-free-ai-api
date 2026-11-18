# API Reference: Endpoints, Authentication and Limits of the Free Enrai AI API

**← Back to [README](../README.md)** · [Getting started](getting-started.md) ·
[API reference](api-reference.md) · [Models](models.md) · [FAQ](faq.md) ·
[Bahasa Indonesia](id/api-reference.md)

Last updated: **17 November 2026** · Official documentation: <https://enrai.web.id/docs> ·
Pricing & limits: <https://enrai.web.id/pricing>

A compact reference for the **OpenAI-compatible** Enrai **REST API**. Every example uses the
production base URL `https://enrai.web.id/v1`.

Official, always-current documentation: <https://enrai.web.id/docs> · Limits & pricing:
<https://enrai.web.id/pricing>

## Base URL

```
https://enrai.web.id/v1
```

## Authentication

Every request must send these headers:

```
Authorization: Bearer <key>
Content-Type: application/json
```

API keys are created in **Dashboard → API Keys** and are shown **once** at creation. Keep the key
in an environment variable; never put it in code, a repository or a public issue.

| Status | Meaning |
|---|---|
| `401` | Key missing or invalid |

## Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/v1/chat/completions` | Create a chat completion (OpenAI format) |
| `GET` | `/v1/models` | List the combo models that are currently live |

### POST /v1/chat/completions

```bash
curl https://enrai.web.id/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Chatgpt",
    "messages": [
      { "role": "system", "content": "You are a concise assistant." },
      { "role": "user", "content": "What is an OpenAI-compatible API?" }
    ]
  }'
```

Main fields:

| Field | Type | Required | Notes |
|---|---|---|---|
| `model` | string | Yes | Model / combo alias name, e.g. `Chatgpt` (see [models.md](models.md)) |
| `messages` | array | Yes | List of messages with `role` and `content` |
| `stream` | boolean | No | `true` for Server-Sent Events |

The response follows the OpenAI shape: the answer text is in `choices[0].message.content`, and
token usage is in the `usage` object.

### GET /v1/models

```bash
curl https://enrai.web.id/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Returns **only the combo models that are currently live**. Call it once at application start and
cache the result.

## Streaming

Add `"stream": true` and read the response as Server-Sent Events:

```bash
curl -N https://enrai.web.id/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"model":"Chatgpt","stream":true,"messages":[{"role":"user","content":"Hello"}]}'
```

Rules to hold on the client side:

1. Each chunk arrives as a `data: {...}` line with the delta in `choices[].delta`.
2. The stream ends with `data: [DONE]` — do not wait for an extra JSON body.
3. Lines that do not start with `data:` are SSE comments; skip them, do not parse them as JSON.

Client examples: [`../examples/python/stream.py`](../examples/python/stream.py),
[`../examples/curl/stream.sh`](../examples/curl/stream.sh).

## Rate limits

| Endpoint | Limit |
|---|---|
| `POST /v1/chat/completions` | 20 requests per minute per key (burst 5) |
| `GET /v1/models` | 60 requests per minute per key |

These numbers come from the [pricing](https://enrai.web.id/pricing) and
[docs](https://enrai.web.id/docs) pages as of 17 November 2026.

## Error

Errors are returned as JSON with an `error.message` field.

| Status | Meaning | Suggested action |
|---|---|---|
| `401` | Unauthorized — key missing or invalid | Check the `Authorization: Bearer <key>` header |
| `429` | Rate limit reached | Exponential backoff with jitter, lower concurrency |
| `502` | Upstream provider failed | Retry after a pause; it is not a payload error |
| `500` | Server error | Retry; report it if it repeats |

**Note:** a `200` response with empty `choices` must be treated as a failure. Enrai already retries
against other members of the combo first, and if all of them come back empty the server answers
with `502`.

## Safe integration practices

- Keep the base URL, model name and key as configuration (`ENRAI_BASE_URL`, `ENRAI_MODEL`,
  `ENRAI_API_KEY`).
- Cache the model list; do not call `/v1/models` in the request path.
- Cap retries (3 at most) and use backoff rather than a tight loop.
- Log status + `error.message`, never the API key.

---

Back to [README](../README.md) · [Getting started](getting-started.md) · [Models](models.md) ·
[FAQ](faq.md) · Official site: <https://enrai.web.id>
