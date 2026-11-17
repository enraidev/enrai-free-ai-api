# Enrai: Free AI API Gratis untuk Developer (OpenAI-Compatible)

**Enrai** adalah **API AI gratis** untuk developer: satu API key untuk beberapa model LLM, diakses lewat REST API yang **kompatibel OpenAI** (`/v1/chat/completions`, `/v1/models`) dengan dukungan streaming. Cocok untuk prototipe, chatbot, otomasi, dan aplikasi yang butuh **LLM API** tanpa biaya awal — tanpa kartu kredit.

Alih-alih mendaftar ke banyak provider, Anda memakai satu base URL (`https://enrai.web.id/v1`) dan satu key; permintaan diteruskan ke provider yang sedang sehat, sehingga aplikasi tetap jalan saat satu upstream bermasalah. Kalau nanti butuh pindah, cukup ganti base URL di SDK OpenAI — kode aplikasi tidak berubah.

[![Website](https://img.shields.io/badge/website-enrai.web.id-4f46e5)](https://enrai.web.id)
[![Free Tier](https://img.shields.io/badge/harga-gratis%20%240-22c55e)](https://enrai.web.id/pricing)
[![OpenAI Compatible](https://img.shields.io/badge/API-OpenAI--compatible-8b5cf6)](https://enrai.web.id/docs)
[![Streaming](https://img.shields.io/badge/streaming-SSE-0ea5e9)](https://enrai.web.id/docs#streaming)
[![Public Beta](https://img.shields.io/badge/status-public%20beta-f59e0b)](https://enrai.web.id)

**Mulai di sini:** [Daftar gratis](https://enrai.web.id/register) · [Dokumentasi API](https://enrai.web.id/docs) · [Harga & limit](https://enrai.web.id/pricing) · [Blog](https://enrai.web.id/blog)

---

## Daftar isi

- [Fitur utama](#fitur-utama)
- [Model yang tersedia](#model-yang-tersedia)
- [Batas pemakaian (rate limit)](#batas-pemakaian-rate-limit)
- [Quick start: 3 langkah](#quick-start-3-langkah)
- [Contoh kode](#contoh-kode)
- [Use case](#use-case)
- [FAQ](#faq)
- [Dokumentasi lengkap](#dokumentasi-lengkap)
- [Berkontribusi](#berkontribusi)
- [English summary](#english-summary)

---

## Fitur utama

- **Endpoint kompatibel OpenAI** — `POST /v1/chat/completions` dan `GET /v1/models`, sehingga SDK OpenAI (Node, Python), Postman, dan tools lain bisa dipakai hanya dengan mengganti base URL.
- **Satu key untuk semua model** — API key dibuat sekali di dashboard, berlaku untuk seluruh model yang tersedia.
- **Gratis tanpa kartu kredit** — tier gratis dengan limit yang dipublikasikan, tidak ada tagihan tersembunyi saat mulai.
- **Streaming SSE** — kirim `"stream": true` dan baca potongan jawaban secara real-time, diakhiri `[DONE]`.
- **Failover antar provider** — setiap nama model adalah *combo* yang dikelola server; jika satu provider gagal, permintaan diarahkan ke anggota combo lain.
- **Daftar model dinamis** — `GET /v1/models` mengembalikan model yang benar-benar aktif, jadi aplikasi tidak perlu menghafal nama model.
- **Format error yang jelas** — `401`, `429`, `500`, `502` dengan pesan di `error.message`.

## Model yang tersedia

Daftar di bawah mengikuti beranda `enrai.web.id` per **17 November 2026**. Untuk status terbaru, buka [bagian model di beranda](https://enrai.web.id/#model) atau panggil `GET https://enrai.web.id/v1/models` (cache hasilnya, jangan dipanggil tiap request).

| Model | Kapabilitas | Streaming | Status |
|---|---|---|---|
| `Chatgpt` | Chat completion | Ya | Online |
| `Deepseek` | Chat completion | Ya | Online |
| `GLM` | Chat completion | Ya | Online |

Detail per model: [`docs/models.md`](docs/models.md).

> Nama model di atas adalah **alias combo**, bukan nama vendor. Provider di baliknya dikelola otomatis, jadi string yang sama tetap bekerja meski satu provider sedang gangguan.

## Batas pemakaian (rate limit)

| Endpoint | Limit per API key |
|---|---|
| `POST /v1/chat/completions` | 20 request/menit (burst 5) |
| `GET /v1/models` | 60 request/menit |

Limit di atas adalah yang dipublikasikan di [halaman pricing](https://enrai.web.id/pricing) dan [dokumentasi API](https://enrai.web.id/docs) pada 17 November 2026. Jika berubah, sumber kebenaran tetap halaman situs.

## Quick start: 3 langkah

1. **Daftar gratis** — buat akun di [enrai.web.id/register](https://enrai.web.id/register). Tidak perlu kartu kredit.
2. **Ambil API key** — buka **Dashboard → API Keys**, buat key baru. Key hanya ditampilkan **sekali**; simpan di environment variable, jangan di kode.
3. **Kirim request pertama** — pakai salah satu contoh di bawah dengan base URL `https://enrai.web.id/v1`.

## Contoh kode

Placeholder `YOUR_API_KEY` diganti dengan key Anda (lebih aman: simpan di environment variable `ENRAI_API_KEY`).

### cURL

```bash
curl https://enrai.web.id/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Chatgpt",
    "messages": [
      { "role": "user", "content": "Halo! Jelaskan API AI gratis dalam satu paragraf." }
    ]
  }'
```

### Python

```bash
pip install openai
```

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://enrai.web.id/v1",
    api_key=os.environ.get("ENRAI_API_KEY", "YOUR_API_KEY"),
)

response = client.chat.completions.create(
    model="Chatgpt",
    messages=[{"role": "user", "content": "Halo! Apa itu API yang kompatibel OpenAI?"}],
)

print(response.choices[0].message.content)
```

### JavaScript / Node.js

```bash
npm install openai
```

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://enrai.web.id/v1",
  apiKey: process.env.ENRAI_API_KEY || "YOUR_API_KEY",
});

const response = await client.chat.completions.create({
  model: "Chatgpt",
  messages: [{ role: "user", content: "Halo! Apa itu API yang kompatibel OpenAI?" }],
});

console.log(response.choices[0].message.content);
```

Contoh runnable (termasuk streaming) ada di [`examples/`](examples/README.md): [`python/`](examples/python), [`nodejs/`](examples/nodejs), [`curl/`](examples/curl).

## Use case

- **Chatbot & asisten** — chatbot web, asisten internal, atau customer support sederhana.
- **Otomasi & tooling** — merangkum dokumen, mengekstrak data dari teks, membuat draft konten.
- **Aplikasi mobile & web** — backend aplikasi Android/Web yang butuh LLM tanpa biaya per token di tahap awal.
- **Bot Telegram / WhatsApp** — jembatani pesan masuk ke `/v1/chat/completions` dengan streaming.
- **Belajar & eksperimen** — membandingkan beberapa model dengan satu key dan satu format request.
- **Prototipe cepat** — validasi ide sebelum memutuskan provider berbayar mana yang dipakai.

## FAQ

**Apakah API AI Enrai benar-benar gratis?**
Ya. Ada tier gratis tanpa kartu kredit selama masa **public beta**, dengan limit yang dipublikasikan di halaman [pricing](https://enrai.web.id/pricing). Paket berbayar dikelola dari panel admin bila Anda butuh kapasitas lebih.

**Apakah kompatibel dengan OpenAI SDK?**
Ya. Ganti `baseURL` menjadi `https://enrai.web.id/v1` dan pakai API key Enrai; bentuk request dan response mengikuti format OpenAI.

**Model apa saja yang tersedia?**
Saat ini `Chatgpt`, `Deepseek`, dan `GLM` (lihat [tabel model](#model-yang-tersedia)). `GET /v1/models` selalu menjadi daftar terbaru.

**Berapa rate limit-nya?**
20 request/menit untuk chat completion (burst 5) dan 60 request/menit untuk daftar model, per API key.

**Apakah streaming didukung?**
Ya. Kirim `"stream": true`, baca Server-Sent Events, diakhiri `[DONE]`.

**Apakah ada batas context window per model?**
Angka context window tidak dipublikasikan di situs; lihat [`docs/models.md`](docs/models.md) untuk catatan dan placeholder yang masih kosong.

**Apa yang terjadi kalau saya kena limit?**
Server membalas `429` dengan `error.message`. Terapkan retry dengan exponential backoff, maksimal beberapa kali.

**Bisakah dipakai untuk produksi?**
Ini **public beta**. Cocok untuk prototipe dan tools internal; untuk layanan kritis, siapkan provider kedua sebagai fallback.

Pertanyaan lain: [`docs/faq.md`](docs/faq.md).

## Dokumentasi lengkap

| Dokumen | Isi |
|---|---|
| [docs/getting-started.md](docs/getting-started.md) | Daftar, ambil key, request pertama, troubleshooting |
| [docs/api-reference.md](docs/api-reference.md) | Endpoint, autentikasi, streaming, error, rate limit |
| [docs/models.md](docs/models.md) | Daftar model, alias combo, cara cek model aktif |
| [docs/faq.md](docs/faq.md) | Pertanyaan yang sering muncul |

Referensi resmi: [enrai.web.id/docs](https://enrai.web.id/docs) · Limit & harga: [enrai.web.id/pricing](https://enrai.web.id/pricing) · Artikel: [enrai.web.id/blog](https://enrai.web.id/blog)

**Status layanan:** [ISI: URL halaman status/uptime — belum ada di situs; status model terlihat di beranda bagian Models]

## Berkontribusi

Koreksi dokumentasi, contoh kode baru, atau perbaikan typo sangat diterima — lihat [`CONTRIBUTING.md`](CONTRIBUTING.md). Jangan pernah menaruh API key di issue, PR, atau commit.

## Lisensi

Contoh kode: **MIT**. Dokumentasi dan artikel: **CC BY 4.0**. Lihat [`LICENSE`](LICENSE).

---

## English summary

**Enrai** is a **free AI API for developers**: one API key, several LLM models, exposed through an **OpenAI-compatible** REST API (`POST /v1/chat/completions`, `GET /v1/models`) with SSE streaming and automatic provider failover. Point your existing OpenAI SDK at `https://enrai.web.id/v1`, use the model names `Chatgpt`, `Deepseek` or `GLM`, and keep the rest of your code unchanged.

- Free tier, no credit card, public beta — [sign up](https://enrai.web.id/register)
- Rate limits: 20 chat requests/min (burst 5) and 60 model-list requests/min per key
- Docs: [enrai.web.id/docs](https://enrai.web.id/docs) · Pricing: [enrai.web.id/pricing](https://enrai.web.id/pricing)
- Examples: [Python](examples/python), [Node.js](examples/nodejs), [cURL](examples/curl)
- Status page: [ISI: status page URL — none published yet]
