#!/usr/bin/env node
/**
 * Chat completion dengan SDK resmi `openai` untuk API AI gratis Enrai.
 *
 * Pemakaian:
 *   export ENRAI_API_KEY="YOUR_API_KEY"
 *   npm install
 *   node chat.mjs "Halo, apa kabar?"
 *   node chat.mjs --stream "Hitung 1 sampai 10."
 *
 * Variabel lingkungan:
 *   ENRAI_API_KEY  wajib, API key dari https://enrai.web.id/register
 *   ENRAI_MODEL    opsional, default Chatgpt (Deepseek, GLM)
 *
 * Dokumentasi: https://enrai.web.id/docs
 */

import OpenAI from "openai";

const BASE_URL = "https://enrai.web.id/v1";
const DEFAULT_MODEL = "Chatgpt";
const DEFAULT_PROMPT = "Halo! Apa itu API yang kompatibel OpenAI?";

const ERROR_HINTS = {
  401: "API key tidak valid atau hilang. Periksa ENRAI_API_KEY.",
  429: "Rate limit tercapai (20 request/menit, burst 5). Tunggu lalu ulangi.",
  500: "Galat server. Ulangi setelah jeda; laporkan bila terus berulang.",
  502: "Seluruh provider di balik combo sedang gagal. Ulangi beberapa saat lagi.",
};

function explain(error) {
  const status = error?.status;
  if (Number.isInteger(status) && ERROR_HINTS[status]) return `[${status}] ${ERROR_HINTS[status]}`;
  if (Number.isInteger(status)) return `[${status}] Permintaan gagal: ${error.message}`;
  return `Permintaan gagal: ${error?.message ?? error}`;
}

const apiKey = process.env.ENRAI_API_KEY;
if (!apiKey) {
  console.error("ENRAI_API_KEY belum di-set. Jalankan: export ENRAI_API_KEY='YOUR_API_KEY'");
  console.error("Belum punya key? Daftar gratis di https://enrai.web.id/register");
  process.exit(2);
}

const args = process.argv.slice(2);
const useStream = args.includes("--stream");
const prompt = args.filter((a) => a !== "--stream").join(" ") || DEFAULT_PROMPT;
const model = process.env.ENRAI_MODEL || DEFAULT_MODEL;

const client = new OpenAI({ baseURL: BASE_URL, apiKey });
const messages = [{ role: "user", content: prompt }];

if (useStream) {
  let gotText = false;
  try {
    const stream = await client.chat.completions.create({ model, messages, stream: true });
    for await (const chunk of stream) {
      const piece = chunk?.choices?.[0]?.delta?.content;
      if (piece) {
        gotText = true;
        process.stdout.write(piece);
      }
    }
  } catch (error) {
    console.error(`\n${explain(error)}`);
    process.exit(1);
  }

  process.stdout.write("\n");
  if (!gotText) {
    console.error("Stream selesai tanpa teks \u2014 perlakukan sebagai kegagalan.");
    process.exit(1);
  }
  process.exit(0);
}

let response;
try {
  response = await client.chat.completions.create({ model, messages });
} catch (error) {
  console.error(explain(error));
  process.exit(1);
}

const content = (response?.choices?.[0]?.message?.content ?? "").trim();
if (!content) {
  // 200 dengan isi kosong tetap dianggap gagal.
  console.error("Jawaban kosong dari upstream \u2014 perlakukan sebagai kegagalan.");
  process.exit(1);
}

console.log(content);
if (response.usage) {
  const { prompt_tokens: p, completion_tokens: c } = response.usage;
  console.error(`\n[model=${model} prompt_tokens=${p} completion_tokens=${c}]`);
}
