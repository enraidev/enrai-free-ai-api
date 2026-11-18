# Enrai Free AI API FAQ: Frequently Asked Questions

**← Back to [README](../README.md)** · [Getting started](getting-started.md) ·
[API reference](api-reference.md) · [Models](models.md) · [FAQ](faq.md) ·
[Bahasa Indonesia](id/faq.md)

Last updated: **17 November 2026** · Official documentation: <https://enrai.web.id/docs> ·
Pricing & limits: <https://enrai.web.id/pricing>

Short answers to the most common questions about the **free Enrai AI API** — an **LLM API** service
with **OpenAI-compatible** endpoints. Every answer refers to the official site
<https://enrai.web.id> as of 17 November 2026.

## Is the Enrai AI API really free?

Yes. During **public beta**, Enrai provides a free tier with published limits, and signing up does
not ask for a credit card. Pricing details are at <https://enrai.web.id/pricing>.

## Is Enrai compatible with the OpenAI SDK?

Yes. The endpoints follow the OpenAI format: `POST /v1/chat/completions` and `GET /v1/models`. You
only need to change `baseURL` to `https://enrai.web.id/v1` and use an Enrai API key; the request,
response and streaming structures do not change.

## How do I get an API key?

1. Sign up at <https://enrai.web.id/register>.
2. Sign in to the dashboard and open **API Keys**.
3. Create a new key and copy it immediately — it is shown only **once**.

Step-by-step guide: [getting-started.md](getting-started.md).

## Which models are available?

`Chatgpt`, `Deepseek` and `GLM` — see [models.md](models.md). The current list is always available
through `GET https://enrai.web.id/v1/models`.

## What are the rate limits?

| Endpoint | Limit |
|---|---|
| `POST /v1/chat/completions` | 20 requests per minute (burst 5) |
| `GET /v1/models` | 60 requests per minute |

Limits apply per API key. If you exceed them, the server answers `429`.

## Is streaming supported?

Yes. Send `"stream": true`; the response is delivered as Server-Sent Events and ends with
`[DONE]`. Details: [api-reference.md](api-reference.md#streaming).

## Which languages can I use?

Any language with an HTTP client: Python, JavaScript/Node.js, PHP, Go, Rust, Java, Kotlin and so
on. If that language has an OpenAI SDK, the SDK works directly with the Enrai base URL.

## Is vision or function calling supported?

There is no official documentation for it on the site yet. Do not design features that depend on
those capabilities until you confirm at <https://enrai.web.id/docs>. The status is stated plainly
in [models.md](models.md): not published.

## Is it production-ready?

The API is in **public beta**. It is suitable for prototypes, internal tools and experiments. For
services that must not fail, keep a second provider as a fallback — because the format is OpenAI's,
switching providers only changes the base URL and the key.

## What should I do when I receive a `502`?

`502` means the upstream provider failed after failover was attempted. Retry the request after a
short pause; your payload is usually not at fault. If it keeps happening, check the site for model
status.

## Is there a service status page?

Not published yet. Model status and the current list are visible on the home page Models section
(<https://enrai.web.id/#model>) and at `GET https://enrai.web.id/v1/models`.

## Where do I report a bug or ask a question?

An official community channel (chat group) is not published yet. For account, key or quota
questions, use the contact listed at <https://enrai.web.id>. For documentation issues in this
repository, open a GitHub issue; see [CONTRIBUTING.md](../CONTRIBUTING.md).

## Where is the full documentation?

- Official documentation: <https://enrai.web.id/docs>
- Pricing & limits: <https://enrai.web.id/pricing>
- In this repository: [getting-started.md](getting-started.md) ·
  [api-reference.md](api-reference.md) · [models.md](models.md)

---

Back to [README](../README.md) · Official site: <https://enrai.web.id>
