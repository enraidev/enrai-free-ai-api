---
title: "Free OpenAI-Compatible AI APIs: What to Check Before You Commit"
description: "A practical checklist for evaluating a free OpenAI-compatible AI API: model naming, rate limits, empty-response handling, failover and migration cost."
canonical: https://github.com/enraidev/enrai-free-ai-api/blob/main/articles/free-openai-compatible-ai-api.md
lang: en
date: 2026-11-17
author: Enrai Dev
---

# Free OpenAI-Compatible AI APIs: What to Check Before You Commit

*Last updated: 17 November 2026 · 8 min read*

Every few weeks a new "free AI API" appears, and every few weeks developers burn a weekend
integrating one that turns out to be a rate-limited demo, a wrapper around someone else's key,
or a service that disappears with the domain. The appeal is obvious — an OpenAI-compatible
endpoint means you keep your SDK, your prompts and your tests — but compatibility is only the
first checkbox. This guide covers the rest, and it ends with a working quickstart you can run
today.

## Why free tiers exist at all

The economics are not mysterious. An API gateway that fronts several model providers gets
volume-based pricing on the upstream side and can afford to give away a slice of it: small
combo requests cost fractions of a cent, and a free tier is the cheapest marketing a developer
product has. What varies is *how honest* the service is about the arrangement:

- **Who pays for the upstream?** If the answer is "nobody knows", expect sudden 429s when the
  provider's own free quota runs out.
- **What happens on failure?** A single-provider wrapper returns 500 and dies with its provider.
  A gateway routes the request to another member of the combo.
- **Are the limits published?** "Generous limits" is not a number. `20 requests per minute` is.

## The seven-point checklist

Before you write a line of production code against a free endpoint, verify these.

**1. Base URL and endpoint shape.** It must be `/v1/chat/completions` — not
`/api/chat`, not `/chat/completions` with a different auth header. Anything else means a
custom client and a rewrite later.

**2. Auth header.** `Authorization: Bearer <key>` is the convention. Keys should be
per-account, revocable, and shown once at creation rather than emailed back on demand.

**3. Model discovery.** A `GET /v1/models` that returns *only* currently available models
saves you from hardcoding names that stop existing. Cache it at startup; do not call it per
request.

**4. Streaming.** `"stream": true` should produce standard SSE chunks ending in `[DONE]`.
Ask specifically about *heartbeats*: a chat that generates for 40 seconds through a proxy
will otherwise look disconnected.

**5. Failover behaviour.** Ask the question directly: *if the upstream provider returns an
empty response, do I get an error or a blank message?* An empty `choices` array with HTTP 200
is the worst failure mode in this whole space, because your retry logic will never fire.

**6. Documented error codes.** `401`, `429`, `500`, `502` — each with a JSON `error.message`.
Undocumented codes are where debugging time goes to die.

**7. Cost of leaving.** Can you point the same code at another OpenAI-compatible provider by
changing one string? If yes, you are not locked in and the free tier is genuinely low-risk.

## Quickstart against a live, free endpoint

[Enrai Dev](https://enrai.web.id) is one of the services that passes this checklist, and it is
free during its public beta: one key, everything listed below, no card. That makes it a
reasonable place to run the experiment.

```bash
# 1. Create an account and generate a key: https://enrai.web.id/register
export ENRAI_API_KEY="sk-enrai-..."

# 2. Ask which models are live (cache this at startup)
curl -s https://enrai.web.id/v1/models \
  -H "Authorization: Bearer $ENRAI_API_KEY"

# 3. Talk to one of them
curl -s https://enrai.web.id/v1/chat/completions \
  -H "Authorization: Bearer $ENRAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Chatgpt",
    "messages": [{"role": "user", "content": "In one sentence: what is an API gateway?"}]
  }'
```

The response is the OpenAI shape you already know — `choices[0].message.content`, plus
`usage`. Notice that the model name is a *combo alias*, not a vendor string: `Chatgpt`,
`Deepseek` and `GLM` are published names whose upstream providers are rotated server-side. You
get failover without writing failover code, and you keep the same string in your config.

## Rate limits: the part everyone skips

Published limits for the free tier are **20 chat requests per minute (burst 5)** and
**60 model-list requests per minute**, per key. Twenty per minute sounds small until you notice
what actually breaks first: a retry loop.

Two rules that keep you inside the limit without a queueing system:

```js
// 1. Retry with backoff on 429, never in a tight loop.
async function chat(body, attempt = 0) {
  const res = await fetch("https://enrai.web.id/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.ENRAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (res.status === 429 && attempt < 3) {
    await new Promise((r) => setTimeout(r, 800 * 2 ** attempt));
    return chat(body, attempt + 1);
  }
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${(await res.json()).error?.message}`);
  return res.json();
}

// 2. Never put /v1/models inside a request handler.
const models = await fetch("https://enrai.web.id/v1/models", { headers }).then((r) => r.json());
```

A 429 is a signal, not an error to swallow: if you see it regularly, you are either retrying
too aggressively or you need a paid tier — both are better answers than pretending the request
succeeded.

## Handling the empty-answer trap

The failure mode worth defending against explicitly:

```json
{"choices": null, "usage": {"prompt_tokens": 12, "completion_tokens": 0}}
```

That is HTTP 200 with nothing in it. It happens upstream more often than anyone admits — a
content filter, a truncated generation, a provider having a bad minute. Enrai retries the
request against another combo member before you ever see it, and if both attempts are empty you
get a `502` with an error message instead of a silent blank bubble.

In your own code, treat "no content" as a failure even when the status is 200:

```js
const content = data.choices?.[0]?.message?.content?.trim();
if (!content) throw new Error("empty completion — treat as failure");
```

## What free tiers are actually good for

Being precise here saves disappointment. A free, rate-limited endpoint is excellent for:

- prototypes, side projects, internal tools and demos;
- evaluation — comparing models before paying for one;
- background jobs that tolerate a 20/min ceiling;
- teaching, workshops and blog samples that need a live endpoint.

It is not a substitute for a paid SLA. If an outage costs you money, configure a second
provider and a timeout; the fact that both speak the OpenAI format is exactly the point.

## FAQ

**Do I need to install anything?** No. If your language has an OpenAI SDK, or you are willing
to send JSON over HTTP, you are done.

**Can I use it from PHP, Go, Rust?** Yes — any HTTP client. `POST /v1/chat/completions` with a
JSON body is the entire contract.

**Does it support vision or function calling?** Not as a documented, first-class feature today.
Check `GET /v1/models` and the [API documentation](https://enrai.web.id/docs) for the current
list before designing around it.

**What happens when I hit the limit?** `429` with an `error.message`. Back off, then retry.

**How do I leave?** Change `baseURL` and the key. That is the whole migration, in either
direction.

## Try it

- Sign up (no card): **https://enrai.web.id/register**
- Docs: **https://enrai.web.id/docs**
- Pricing: **https://enrai.web.id/pricing**

*Enrai Dev is in public beta. Limits and model names in this article reflect the live
documentation on 17 November 2026.*
