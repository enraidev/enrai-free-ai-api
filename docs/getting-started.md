# Getting Started: Sign Up and Use the Free Enrai AI API

**← Back to [README](../README.md)** · [Getting started](getting-started.md) ·
[API reference](api-reference.md) · [Models](models.md) · [FAQ](faq.md) ·
[Bahasa Indonesia](id/getting-started.md)

Last updated: **17 November 2026** · Official documentation: <https://enrai.web.id/docs> ·
Pricing & limits: <https://enrai.web.id/pricing>

This guide takes you from zero to your first request against the **free Enrai AI API** — create an
account, get an API key, and call the **OpenAI-compatible** endpoint. It takes about two minutes.

Official documentation: <https://enrai.web.id/docs> · Sign up: <https://enrai.web.id/register> ·
Limits & pricing: <https://enrai.web.id/pricing>

## Quick reference

| Item | Value |
|---|---|
| Base URL | `https://enrai.web.id/v1` |
| Chat endpoint | `POST https://enrai.web.id/v1/chat/completions` |
| Models endpoint | `GET https://enrai.web.id/v1/models` |
| Authentication | `Authorization: Bearer <key>` header |
| Starting model | `Chatgpt` (see [models.md](models.md)) |
| Cost | Free, no credit card (public beta) |

## 1. Create an account

1. Open <https://enrai.web.id/register>.
2. Enter an email and password, then finish signing up.
3. There is no payment form and no credit card is requested.

Already have an account? Go straight to <https://enrai.web.id/login>.

## 2. Get an API key

1. Sign in to the dashboard.
2. Open **API Keys**.
3. Create a new key and **copy it immediately** — it is shown only once.

Store it as an environment variable, not inside your code:

```bash
export ENRAI_API_KEY="YOUR_API_KEY"
```

If a key leaks, delete or rotate it in the dashboard and create a new one. Never commit a key to
GitHub.

## 3. First request

### cURL

```bash
curl https://enrai.web.id/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Chatgpt",
    "messages": [{"role": "user", "content": "Hello, this is my first request."}]
  }'
```

### Python

```bash
pip install openai
```

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://enrai.web.id/v1",
    api_key=os.environ["ENRAI_API_KEY"],
)

res = client.chat.completions.create(
    model="Chatgpt",
    messages=[{"role": "user", "content": "Hello, this is my first request."}],
)
print(res.choices[0].message.content)
```

### Node.js

```bash
npm install openai
```

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://enrai.web.id/v1",
  apiKey: process.env.ENRAI_API_KEY,
});

const res = await client.chat.completions.create({
  model: "Chatgpt",
  messages: [{ role: "user", content: "Hello, this is my first request." }],
});
console.log(res.choices[0].message.content);
```

If the reply contains text in `choices[0].message.content`, your basic integration is correct.

More complete examples (including streaming) are in [`../examples/`](../examples/README.md).

## 4. Check which models are live

```bash
curl https://enrai.web.id/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Call this once when your application starts, then **cache** the result. Do not call it on every
request — it is limited to 60 requests per minute per key.

## 5. Troubleshooting

| Symptom | Most common cause | Fix |
|---|---|---|
| `401` | Wrong or expired key, or a missing header | Make sure it reads `Authorization: Bearer <key>` with no extra spaces |
| `429` | Over 20 requests/minute (burst 5) | Exponential backoff, lower concurrency, queue requests |
| `502` | Every provider behind the combo failed | Retry in a moment; this is not your payload's fault |
| `500` | Server error | Try again; if it repeats, report it to the service owner |
| Empty reply | Upstream returned an empty answer | Treat it as a failure, retry once, then handle it as an error |

Full error code list: [`api-reference.md`](api-reference.md#error).

## 6. If you need to switch providers

Because this API follows the OpenAI format, moving to another provider means changing two things:
`base_url` and `api_key`. Keep both as configuration, not as constants:

```bash
ENRAI_BASE_URL=https://enrai.web.id/v1
ENRAI_MODEL=Chatgpt
ENRAI_API_KEY=YOUR_API_KEY
```

---

The official site remains the source of truth: <https://enrai.web.id/docs>. Back to
[README](../README.md) · [API reference](api-reference.md) · [Models](models.md) · [FAQ](faq.md)
