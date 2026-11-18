#!/usr/bin/env node
/**
 * Chat completion with the official `openai` SDK against the free Enrai AI API.
 *
 * Usage:
 *   export ENRAI_API_KEY="YOUR_API_KEY"
 *   npm install
 *   node chat.mjs "Hello, how are you?"
 *   node chat.mjs --stream "Count from 1 to 10."
 *
 * Environment variables:
 *   ENRAI_API_KEY  required, API key from https://enrai.web.id/register
 *   ENRAI_MODEL    optional, defaults to Chatgpt (Deepseek, GLM)
 *
 * Documentation: https://enrai.web.id/docs
 */

import OpenAI from "openai";

const BASE_URL = "https://enrai.web.id/v1";
const DEFAULT_MODEL = "Chatgpt";
const DEFAULT_PROMPT = "Hello! What is an OpenAI-compatible API?";

const ERROR_HINTS = {
  401: "Invalid or missing API key. Check ENRAI_API_KEY.",
  429: "Rate limit reached (20 requests/minute, burst 5). Wait and retry.",
  500: "Server error. Retry after a pause; report it if it keeps happening.",
  502: "Every provider behind the combo is failing. Retry in a moment.",
};

function explain(error) {
  const status = error?.status;
  if (Number.isInteger(status) && ERROR_HINTS[status]) return `[${status}] ${ERROR_HINTS[status]}`;
  if (Number.isInteger(status)) return `[${status}] Request failed: ${error.message}`;
  return `Request failed: ${error?.message ?? error}`;
}

const apiKey = process.env.ENRAI_API_KEY;
if (!apiKey) {
  console.error("ENRAI_API_KEY is not set. Run: export ENRAI_API_KEY='YOUR_API_KEY'");
  console.error("No key yet? Sign up free at https://enrai.web.id/register");
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
    console.error("Stream finished without text \u2014 treat it as a failure.");
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
  // A 200 with an empty body is still a failure.
  console.error("Empty answer from upstream \u2014 treat it as a failure.");
  process.exit(1);
}

console.log(content);
if (response.usage) {
  const { prompt_tokens: p, completion_tokens: c } = response.usage;
  console.error(`\n[model=${model} prompt_tokens=${p} completion_tokens=${c}]`);
}
