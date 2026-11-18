# API Reference: Endpoint, Autentikasi, dan Limit API AI Gratis Enrai

**← Kembali ke [README](../../README.id.md)** · [Getting started](getting-started.md) ·
[API reference](api-reference.md) · [Model](models.md) · [FAQ](faq.md) ·
[English](../api-reference.md)

Terakhir diperbarui: **17 November 2026** · Dokumentasi resmi: <https://enrai.web.id/docs> ·
Harga & limit: <https://enrai.web.id/pricing>

Referensi ringkas untuk **REST API** Enrai yang **kompatibel OpenAI**. Semua contoh memakai base URL
produksi `https://enrai.web.id/v1`.

Dokumentasi resmi dan terbaru: <https://enrai.web.id/docs> · Limit & harga:
<https://enrai.web.id/pricing>

## Base URL

```
https://enrai.web.id/v1
```

## Autentikasi

Setiap request wajib menyertakan header berikut:

```
Authorization: Bearer <key>
Content-Type: application/json
```

API key dibuat di **Dashboard → API Keys** dan hanya ditampilkan **sekali** saat dibuat. Simpan di
environment variable; jangan pernah menaruhnya di kode, repo, atau issue publik.

| Status | Arti |
|---|---|
| `401` | Key tidak ada atau tidak valid |

## Endpoint

| Method | Path | Deskripsi |
|---|---|---|
| `POST` | `/v1/chat/completions` | Membuat chat completion (format OpenAI) |
| `GET` | `/v1/models` | Menampilkan model combo yang sedang aktif |

### POST /v1/chat/completions

```bash
curl https://enrai.web.id/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Chatgpt",
    "messages": [
      { "role": "system", "content": "Anda asisten yang ringkas." },
      { "role": "user", "content": "Apa itu API yang kompatibel OpenAI?" }
    ]
  }'
```

Field utama:

| Field | Tipe | Wajib | Keterangan |
|---|---|---|---|
| `model` | string | Ya | Nama model/alias combo, mis. `Chatgpt` (lihat [models.md](models.md)) |
| `messages` | array | Ya | Daftar pesan dengan `role` dan `content` |
| `stream` | boolean | Tidak | `true` untuk Server-Sent Events |

Response mengikuti bentuk OpenAI: teks jawaban ada di `choices[0].message.content`, dan pemakaian
token di objek `usage`.

### GET /v1/models

```bash
curl https://enrai.web.id/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Mengembalikan **hanya model combo yang aktif**. Panggil sekali saat aplikasi start lalu cache
hasilnya.

## Streaming

Tambahkan `"stream": true` dan baca response sebagai Server-Sent Events:

```bash
curl -N https://enrai.web.id/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"model":"Chatgpt","stream":true,"messages":[{"role":"user","content":"Halo"}]}'
```

Aturan yang perlu dipegang di sisi klien:

1. Setiap potongan datang sebagai baris `data: {...}` dengan delta di `choices[].delta`.
2. Stream diakhiri dengan `data: [DONE]` — jangan menunggu JSON body tambahan.
3. Baris yang tidak diawali `data:` adalah komentar SSE; abaikan, jangan di-parse sebagai JSON.

Contoh klien: [`../../examples/python/stream.py`](../../examples/python/stream.py),
[`../../examples/curl/stream.sh`](../../examples/curl/stream.sh).

## Rate limit

| Endpoint | Limit |
|---|---|
| `POST /v1/chat/completions` | 20 request/menit per key (burst 5) |
| `GET /v1/models` | 60 request/menit per key |

Angka ini berasal dari halaman [pricing](https://enrai.web.id/pricing) dan
[docs](https://enrai.web.id/docs) per 17 November 2026.

## Error

Error dikembalikan sebagai JSON dengan field `error.message`.

| Status | Arti | Tindakan yang disarankan |
|---|---|---|
| `401` | Unauthorized — key hilang/tidak valid | Periksa header `Authorization: Bearer <key>` |
| `429` | Rate limit tercapai | Exponential backoff dengan jitter, kurangi konkurensi |
| `502` | Provider upstream gagal | Coba lagi setelah jeda; bukan kesalahan payload |
| `500` | Server error | Coba lagi; laporkan bila berulang |

**Perhatikan:** response `200` dengan `choices` kosong harus diperlakukan sebagai kegagalan. Enrai
sudah mencoba ulang ke anggota combo lain lebih dulu, dan bila semuanya kosong server membalas
`502`.

## Praktik integrasi yang aman

- Simpan base URL, nama model, dan key sebagai konfigurasi (`ENRAI_BASE_URL`, `ENRAI_MODEL`,
  `ENRAI_API_KEY`).
- Cache daftar model; jangan panggil `/v1/models` di jalur request.
- Batasi retry (maksimal 3 kali) dan pakai backoff, bukan loop cepat.
- Log status + `error.message`, jangan log API key.

---

Kembali ke [README](../../README.id.md) · [Getting started](getting-started.md) ·
[Model](models.md) · [FAQ](faq.md) · Situs resmi: <https://enrai.web.id>
