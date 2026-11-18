# Examples with the official OpenAI SDK

Two examples that use the official `openai` package instead of `fetch` or `curl`. Their purpose: to
prove your integration works with the client most likely already installed in your project.

The difference from the examples in `../python` and `../nodejs`: this folder follows the latest SDK
versions (Python ≥ 3.50, Node.js ≥ 7), supports the `--stream` flag, and maps HTTP error codes to
messages you can act on immediately.

| Folder | Contents | Requirements |
|---|---|---|
| [`python/`](python/chat.py) | `chat.py` (chat + `--stream`), `requirements.txt` | Python ≥ 3.10 |
| [`nodejs/`](nodejs/chat.mjs) | `chat.mjs` (chat + `--stream`), `package.json` | Node.js ≥ 22 |

Every example reads the API key from the `ENRAI_API_KEY` environment variable and exits when it is
empty — there is no real key in this repository.

```bash
export ENRAI_API_KEY="YOUR_API_KEY"   # https://enrai.web.id/register
```

## Python

```bash
cd python
pip install -r requirements.txt
python chat.py "Explain an OpenAI-compatible API in one paragraph."
python chat.py --stream "Count from 1 to 10."
```

## Node.js

```bash
cd nodejs
npm install
node chat.mjs "Explain an OpenAI-compatible API in one paragraph."
node chat.mjs --stream "Count from 1 to 10."
```

## Things to note

- Base URL used: `https://enrai.web.id/v1` (the SDK appends `/chat/completions` itself).
