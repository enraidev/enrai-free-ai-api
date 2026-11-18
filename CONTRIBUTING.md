# Contributing

Thanks for helping with the **free Enrai AI API** repository — documentation and code examples for
<https://enrai.web.id>.

Languages: **English is the primary language** of this repo. Indonesian translations live in
[`README.id.md`](README.id.md) and [`docs/id/`](docs/id/), and are kept in sync with the English
files.

## The most useful contributions

- **Fact corrections:** the site changes (limits, models, endpoints) but this documentation lags
  behind.
- **New code examples:** PHP, Go, Rust, Java/Kotlin, or Telegram/WhatsApp bot integrations.
- **Dead link and typo fixes.**

## Rules

1. **Never send an API key, token or `.env` file.** Use `YOUR_API_KEY` or the `ENRAI_API_KEY`
   environment variable.
2. **Do not invent facts.** If a piece of information is not at <https://enrai.web.id/docs>,
   <https://enrai.web.id/pricing> or the home page, write **"Not published"** and explain it in the
   PR. Do not guess numbers.
3. **One change, one purpose.** Small PRs get reviewed faster.
4. **Examples must run.** Run them first (see below) and mention the command you used in the PR
   description.
5. **No local URLs.** The only service address allowed is `https://enrai.web.id` — no loopback
   address and no port numbers.
6. **Bilingual changes:** when you change a fact, update the English file and the matching file in
   `docs/id/` in the same PR.

## Running the examples

```bash
export ENRAI_API_KEY="YOUR_API_KEY"   # sign up free at https://enrai.web.id/register

# Python (openai SDK)
cd examples/python && pip install -r requirements.txt
python chat.py "Hello"

# Node.js (no dependencies, Node 18+)
cd examples/nodejs
node chat.mjs "Hello"
node chat.mjs --stream "Count from 1 to 10"

# cURL
cd examples/curl
./models.sh && ./chat.sh "Hello"
```

## Documentation style

- English first, Indonesian second. English files are `README.md`, `docs/*.md`; Indonesian files
  are `README.id.md`, `docs/id/*.md`.
- The H1 carries natural keywords; one introductory sentence above it; a breadcrumb back to the
  README in every `docs/` file, plus a link to the other language.
- Short sentences, no unverifiable claims ("fastest", "best", "100% accurate").
- Tables for repeated data (models, limits, error codes); `<details>` blocks for long sections.
- Every code example states how to run it and how to handle `401`/`429`/`502`.

## Commit format

[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
docs: explain the per-key rate limit
docs(readme): add a Node.js streaming example
feat(examples): add a PHP example
ci: add a link check
chore: update Dependabot
```

One commit per group of changes. Messages may be in English or Indonesian — stay consistent inside a
single PR.

## Workflow

```bash
git clone https://github.com/enraidev/enrai-free-ai-api.git
cd enrai-free-ai-api
git checkout -b docs/short-fix
# edit...
git commit -m "docs: clarify the error code table"
git push origin docs/short-fix
```

Then open a Pull Request using the provided template. Include the source of the facts behind every
technical change.

## Automated checks

CI runs markdownlint, a link check (401 on `/v1/*` is expected because an API key is required),
Python/Node/bash syntax checks, and a local-URL guard. Make sure everything is green before asking
for review.

## Questions

- Documentation problems or repo bugs: open an [issue](https://github.com/enraidev/enrai-free-ai-api/issues)
  or start a [discussion](https://github.com/enraidev/enrai-free-ai-api/discussions).
- Service problems (account, key, quota): use the official contact at <https://enrai.web.id>.
- Security vulnerabilities: follow [SECURITY.md](SECURITY.md), do not open a public issue.

## Bahasa Indonesia

Terima kasih sudah mau membantu repo **API AI gratis Enrai**. Ringkasan aturan:

1. **Jangan kirim API key, token, atau file `.env`.**
2. **Jangan mengarang fakta** — kalau tidak ada di situs resmi, tulis "Belum dipublikasikan".
3. **Satu perubahan, satu tujuan**; contoh kode harus jalan dan perintahnya disebutkan di PR.
4. **Tanpa URL lokal** — hanya `https://enrai.web.id`.
5. **Perubahan dua bahasa:** sunting file Inggris dan file padanannya di `docs/id/` dalam PR yang
   sama.

Panduan lengkap dalam bahasa Indonesia ada di [`README.id.md`](README.id.md) dan
[`docs/id/`](docs/id/getting-started.md).
