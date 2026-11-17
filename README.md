# Enrai Dev — promo kit

Promotional material for **[enrai.web.id](https://enrai.web.id)** — a free, OpenAI-compatible
AI API for developers (public beta).

Everything here is static: no build step, no dependencies, no tracking.

```
.
├── index.html                        # landing page (GitHub Pages ready)
├── articles/
│   ├── free-openai-compatible-ai-api.md   # main SEO article (long-form guide)
│   └── openai-sdk-migration.md            # drop-in migration walkthrough
├── robots.txt
├── .nojekyll
└── LICENSE
```

## What is Enrai Dev

| | |
|---|---|
| **Base URL** | `https://enrai.web.id/v1` |
| **Endpoints** | `POST /v1/chat/completions`, `GET /v1/models` |
| **Compatibility** | OpenAI SDKs and clients (Node, Python, PHP, curl) |
| **Streaming** | Server-Sent Events, `"stream": true` |
| **Models** | `Chatgpt`, `Deepseek`, `GLM` (combo aliases, provider failover) |
| **Rate limits** | 20 chat req/min (burst 5), 60 model-list req/min — per key |
| **Price** | Free during public beta, no credit card |
| **Sign up** | https://enrai.web.id/register |
| **Docs** | https://enrai.web.id/docs |

## Landing page

`index.html` is a single self-contained file (inline CSS + ~10 lines of JS for the code tabs),
targeting the queries "free AI API", "OpenAI-compatible API" and "free LLM API key".

Local preview:

```bash
python -m http.server 8000
# open http://localhost:8000
```

## Articles

Both articles are Markdown, ready to paste into any CMS (WordPress, Ghost, Hashnode, Dev.to,
Medium). They are written to be useful on their own — the product is mentioned where it is
relevant, not on every paragraph.

- `articles/free-openai-compatible-ai-api.md` — what to check in a free AI API, a working
  quickstart, rate-limit and retry handling, and an FAQ.
- `articles/openai-sdk-migration.md` — moving an existing OpenAI-SDK codebase over by changing
  one base URL, with the failure modes that actually bite.

## Publishing checklist

1. Publish `index.html` (GitHub Pages, Netlify, Cloudflare Pages, or your own host).
2. Keep the canonical URL in the `<head>` in sync with wherever it is served from.
3. Paste the articles into the blog at `enrai.web.id/blog` — internal links already point
   to the live docs, pricing and signup pages.
4. Verify every code sample still returns text before publishing: the snippets use the live
   endpoint, not mocks.

## Claims checked against the live site

All product facts in this repo were taken from the live pages on **17 November 2026**:
`enrai.web.id` (home, `/docs`, `/pricing`). If the rate limits, model list or pricing change,
update this table and the "Free tier" wording in `index.html` and both articles.

## License

MIT for the code and page; CC BY 4.0 for the articles. See `LICENSE`.
