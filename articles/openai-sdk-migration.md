---
title: "Moving an Existing OpenAI Codebase to an OpenAI-Compatible Gateway"
description: "How to migrate an existing OpenAI SDK codebase to an OpenAI-compatible gateway: base URL change, model aliases, streaming, retries and rollback plan."
canonical: https://github.com/enraidev/enrai-free-ai-api/blob/main/articles/openai-sdk-migration.md
lang: en
date: 2026-11-17
author: Enrai Dev
---

# Moving an Existing OpenAI Codebase to an OpenAI-Compatible Gateway

*Last updated: 17 November 2026 · 5 min read*

The pitch for "OpenAI-compatible" is that migration is a one-line change. Most of the time it
is. The other times are spent on the details nobody documents: hardcoded model names, proxy
environment variables, streaming parsers that assume a specific chunk shape, and the retry
logic that was written for an API with different limits.

This is the checklist we use when pointing an existing codebase at
[Enrai Dev](https://enrai.web.id) — a free, OpenAI-compatible endpoint — and it applies to any
compatible gateway.

## Step 1: change one string, then look for the others

```diff
 const client = new OpenAI({
-  baseURL: "https://api.openai.com/v1",
+  baseURL: "https://enrai.web.id/v1",
   apiKey: process.env.ENRAI_API_KEY,
 });
```

Then search the repo — this is where migrations actually go wrong:

```bash
grep -rn --include=*.{js,ts,py,php,go,rb,java,kt} \
  -e "api.openai.com" -e "https://api\.openai" \
  -e "OPENAI_BASE_URL" -e "AZURE_OPENAI"
```

Every hit is a client you have not migrated yet. SDKs read `OPENAI_BASE_URL` from the
environment, so setting it in one place is often enough — until a script or a Jupyter notebook
overrides it.

## Step 2: replace vendor model names with combo aliases

Gateway model names are *aliases*, not vendor SKUs. On Enrai they are `Chatgpt`, `Deepseek` and
`GLM`; the providers behind each alias rotate server-side. That is what buys you failover
without writing failover code.

```bash
curl -s https://enrai.web.id/v1/models -H "Authorization: Bearer $ENRAI_API_KEY" | jq -r '.data[].id'
```

Do this once at startup and cache it. Hardcoding `gpt-4o-2024-08-06` or `deepseek-chat` against
a gateway is the single most common cause of "it worked yesterday".

## Step 3: confirm streaming rather than assuming it

Most SDK streaming works unchanged, but if you parse SSE by hand, check three things:

```
data: {"choices":[{"delta":{"content":"Hello"}}]}

data: [DONE]
```

1. Chunks arrive in the OpenAI `choices[].delta` shape.
2. The stream ends with `[DONE]` — do not wait for a JSON body that never comes.
3. The connection stays alive during long generations (heartbeat comments are legal SSE and
   must not be parsed as data).

If your parser crashes on a line that does not start with `data:`, it will crash on a real
stream eventually.

## Step 4: rewrite retries for the new limits

The free tier publishes its limits: **20 chat requests per minute with a burst of 5**, and
**60 model-list requests per minute** per key. Whatever retry policy you had for the previous
provider, verify it against those numbers — a three-attempt retry with no jitter will turn one
slow minute into sixty 429s.

- Back off exponentially with jitter, cap at 3 attempts.
- Treat `502` as "upstream failed after failover" and surface it, do not hide it.
- Treat a `200` with an empty `choices` array as a failure too. It is the one bug that makes
  your UI show a blank bubble while your logs show success.

## Step 5: keep the exit cheap

Write the base URL and model names as configuration, not constants:

```env
AI_BASE_URL=https://enrai.web.id/v1
AI_MODEL=Chatgpt
AI_API_KEY=sk-enrai-...
```

Compatibility is the feature that makes a free tier safe to try: the same code runs against any
OpenAI-shaped provider, so leaving costs the same one-line diff as arriving did.

## Where to start

1. Get a key — **https://enrai.web.id/register** (free, no card).
2. Read the limits — **https://enrai.web.id/docs**.
3. Point `AI_BASE_URL` at `https://enrai.web.id/v1` and make one request.

If `choices[0].message.content` has text in it, the migration is done. Everything after that is
your application, unchanged.
