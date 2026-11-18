#!/usr/bin/env node
/**
 * Chat completion + streaming with the free Enrai AI API (OpenAI-compatible).
 * No dependencies: uses the built-in fetch from Node.js 18+.
 *
 * Usage:
 *   export ENRAI_API_KEY="YOUR_API_KEY"
 *   node chat.mjs "Hello, how are you?"
 *   node chat.mjs --stream "Count from 1 to 10."
 *
 * Documentation: https://enrai.web.id/docs
 */

const BASE_URL = "https://enrai.web.id/v1";
const MODEL = process.env.ENRAI_MODEL || "Chatgpt";

const apiKey = process.env.ENRAI_API_KEY;
if (!apiKey) {
  console.error("ENRAI_API_KEY is not set. Run: export ENRAI_API_KEY='YOUR_API_KEY'");
  console.error("No key yet? Sign up free at https://enrai.web.id/register");
  process.exit(2);
}

const args = process.argv.slice(2);
const useStream = args.includes("--stream");
const prompt = args.filter((a) => a !== "--stream").join(" ") || "Hello! What is an OpenAI-compatible API?";

const headers = {
  Authorization: `Bearer ${apiKey}`,
  "Content-Type": "application/json",
};

function explain(status, message) {
  if (status === 401) return "Invalid API key. Check ENRAI_API_KEY.";
  if (status === 429) return "Rate limit reached (20 requests/minute). Wait and retry.";
  if (status === 502) return "Upstream provider failed after failover. Retry after a short pause.";
  if (status === 500) return "Server error. Retry; report it if it keeps happening.";
  return message || "Request failed.";
}

async function once() {
  const res = await fetch(`${BASE_URL}/chat/completions`, {
    method: "POST",
    headers,
    body: JSON.stringify({ model: MODEL, messages: [{ role: "user", content: prompt }] }),
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    console.error(`[${res.status}] ${explain(res.status, body?.error?.message)}`);
    process.exit(1);
  }

  const data = await res.json();
  const content = (data?.choices?.[0]?.message?.content || "").trim();
  if (!content) {
    console.error("Empty answer from upstream - treat it as a failure.");
    process.exit(1);
  }
  console.log(content);
  if (data.usage) {
    console.error(`\n[model=${MODEL} prompt_tokens=${data.usage.prompt_tokens} completion_tokens=${data.usage.completion_tokens}]`);
  }
}

async function stream() {
  const res = await fetch(`${BASE_URL}/chat/completions`, {
    method: "POST",
    headers: { ...headers, Accept: "text/event-stream" },
    body: JSON.stringify({
      model: MODEL,
      stream: true,
      messages: [{ role: "user", content: prompt }],
    }),
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    console.error(`[${res.status}] ${explain(res.status, body?.error?.message)}`);
    process.exit(1);
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let gotText = false;

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed.startsWith("data:")) continue; // skip SSE comments/heartbeats
      const payload = trimmed.slice(5).trim();
      if (payload === "[DONE]") {
        process.stdout.write("\n");
        if (!gotText) {
          console.error("Stream finished without text - treat it as a failure.");
          process.exit(1);
        }
        return;
      }
      try {
        const json = JSON.parse(payload);
        const piece = json?.choices?.[0]?.delta?.content;
        if (piece) {
          gotText = true;
          process.stdout.write(piece);
        }
      } catch {
        // incomplete JSON fragment: ignore it, the buffer already holds the rest
      }
    }
  }
}

await (useStream ? stream() : once());
