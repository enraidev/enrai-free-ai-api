#!/usr/bin/env node
/**
 * Chat completion + streaming dengan API AI gratis Enrai (kompatibel OpenAI).
 * Tanpa dependency: memakai fetch bawaan Node.js 18+.
 *
 * Pemakaian:
 *   export ENRAI_API_KEY="YOUR_API_KEY"
 *   node chat.mjs "Halo, apa kabar?"
 *   node chat.mjs --stream "Hitung 1 sampai 10."
 *
 * Dokumentasi: https://enrai.web.id/docs
 */

const BASE_URL = "https://enrai.web.id/v1";
const MODEL = process.env.ENRAI_MODEL || "Chatgpt";

const apiKey = process.env.ENRAI_API_KEY;
if (!apiKey) {
  console.error("ENRAI_API_KEY belum di-set. Jalankan: export ENRAI_API_KEY='YOUR_API_KEY'");
  console.error("Belum punya key? Daftar gratis di https://enrai.web.id/register");
  process.exit(2);
}

const args = process.argv.slice(2);
const useStream = args.includes("--stream");
const prompt = args.filter((a) => a !== "--stream").join(" ") || "Halo! Apa itu API yang kompatibel OpenAI?";

const headers = {
  Authorization: `Bearer ${apiKey}`,
  "Content-Type": "application/json",
};

function explain(status, message) {
  if (status === 401) return "API key tidak valid. Periksa ENRAI_API_KEY.";
  if (status === 429) return "Rate limit tercapai (20 request/menit). Tunggu lalu ulangi.";
  if (status === 502) return "Provider upstream gagal setelah failover. Ulangi setelah beberapa saat.";
  if (status === 500) return "Server error. Coba lagi; laporkan bila berulang.";
  return message || "Permintaan gagal.";
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
    console.error("Jawaban kosong dari upstream — perlakukan sebagai kegagalan.");
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
      if (!trimmed.startsWith("data:")) continue; // abaikan komentar/heartbeat SSE
      const payload = trimmed.slice(5).trim();
      if (payload === "[DONE]") {
        process.stdout.write("\n");
        if (!gotText) {
          console.error("Stream selesai tanpa teks — perlakukan sebagai kegagalan.");
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
        // potongan JSON tidak lengkap: abaikan, buffer sudah menahan sisanya
      }
    }
  }
}

await (useStream ? stream() : once());
