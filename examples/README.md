# Enrai Free AI API Code Examples (Python, Node.js, cURL)

Ready-to-run examples that call the **free Enrai AI API**, an **OpenAI-compatible** endpoint at
`https://enrai.web.id/v1`.

Every example reads the API key from the `ENRAI_API_KEY` environment variable and refuses to run
without one — there is no real key in this repository.

```bash
export ENRAI_API_KEY="YOUR_API_KEY"
```

Free sign-up: <https://enrai.web.id/register> · Documentation: <https://enrai.web.id/docs>

## Folders

| Folder | Contents |
|---|---|
| [`python/`](python/chat.py) | `chat.py` (chat completion), `stream.py` (SSE streaming), `requirements.txt` |
| [`nodejs/`](nodejs/chat.mjs) | `chat.mjs` (chat + streaming, no dependencies), `package.json` |
| [`curl/`](curl/chat.sh) | `models.sh`, `chat.sh`, `stream.sh` |
| [`openai-sdk/`](openai-sdk/README.md) | Examples using the official `openai` package for Python and Node.js |

The default model in every example is `Chatgpt`. Switch to `Deepseek` or `GLM` (see
[`../docs/models.md`](../docs/models.md)).

## Python

```bash
cd python
pip install -r requirements.txt
python chat.py "Explain an OpenAI-compatible API in one paragraph."
python stream.py "Write a short poem about APIs."
```

## Node.js

The example uses the built-in `fetch` (Node.js 18+), **no dependencies**:

```bash
cd nodejs
node chat.mjs "Explain an OpenAI-compatible API in one paragraph."
node chat.mjs --stream "Count from 1 to 10."
```

If you prefer the official `openai` SDK, the pattern is the same as the Python example: point
`baseURL` at `https://enrai.web.id/v1`.

## cURL

```bash
cd curl
./models.sh
./chat.sh "Hello from cURL!"
./stream.sh "Count from 1 to 10."
```

## Error handling used by the examples

- `401` — wrong/missing key: check `ENRAI_API_KEY`.
- `429` — rate limit (20 requests/minute, burst 5): the examples print a message and suggest
  backoff.
- `502` — upstream failed after failover: retry later.
- Empty reply — treated as a failure, not a success.

Full reference: [`../docs/api-reference.md`](../docs/api-reference.md).
