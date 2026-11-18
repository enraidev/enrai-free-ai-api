# Free Enrai AI API Models (Chatgpt, Deepseek, GLM)

**← Back to [README](../README.md)** · [Getting started](getting-started.md) ·
[API reference](api-reference.md) · [Models](models.md) · [FAQ](faq.md) ·
[Bahasa Indonesia](id/models.md)

Last updated: **17 November 2026** · Official documentation: <https://enrai.web.id/docs> ·
Pricing & limits: <https://enrai.web.id/pricing>

This page explains which models you can call through the **free Enrai AI API**, how model names
work, and how to check which models are live before your application starts.

Base URL: `https://enrai.web.id/v1` · Official documentation: <https://enrai.web.id/docs> · Live
model status: <https://enrai.web.id/#model>

## Model list (as of 17 November 2026)

| Model | Capability | Streaming | Status |
|---|---|---|---|
| `Chatgpt` | Chat completion | Yes | Online |
| `Deepseek` | Chat completion | Yes | Online |
| `GLM` | Chat completion | Yes | Online |

This list is taken from the `enrai.web.id` home page. The authoritative list is always
`GET https://enrai.web.id/v1/models`.

## Model names are aliases, not vendor names

`Chatgpt`, `Deepseek` and `GLM` are **combo aliases**: one name can be served by several providers
behind it. Providers are managed automatically, so:

- the model string in your code does not have to change when a provider changes;
- if one provider fails or returns an empty answer, the request is retried against another member
  of the combo;
- if every member fails, the API answers `502` — not an empty answer with status `200`.

Because of that, do not equate `Chatgpt` with a specific vendor model version. Treat it as a
service name.

## How to check which models are live

```bash
curl https://enrai.web.id/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Recommended practice:

1. Call it when the application starts and keep the result in a cache or in memory.
2. Refresh periodically (for example once an hour), not per request — this endpoint is limited to
   60 requests per minute per key.
3. If a model you use disappears from the list, fall back to another available model and log a
   warning.

## Capabilities

| Capability | Status |
|---|---|
| Chat completion | Available for all three models |
| Streaming (SSE) | Available |
| Dynamic model list | Available (`GET /v1/models`) |
| Context window per model | Not published |
| Output token limit per model | Not published |
| Vision / image input | Not published |
| Function calling / tools | Not published |

Do not rely on capabilities that are not listed at <https://enrai.web.id/docs>.

## Choosing a model

- **`Chatgpt`** — the default choice for general conversation; used throughout this documentation.
- **`Deepseek`** — an alternative for text/reasoning tasks; easy to compare directly with another
  model because the request format is identical.
- **`GLM`** — the third alternative; useful when comparing answer styles without changing code.

Because all three use the same request format, switching models means changing one string:

```python
response = client.chat.completions.create(
    model="Deepseek",  # previously "Chatgpt"
    messages=[{"role": "user", "content": "Hello"}],
)
```

---

Back to [README](../README.md) · [Getting started](getting-started.md) ·
[API reference](api-reference.md) · [FAQ](faq.md)
