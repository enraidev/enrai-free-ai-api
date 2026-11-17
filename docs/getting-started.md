# Getting Started: Cara Daftar dan Memakai API AI Gratis Enrai

**← Kembali ke [README](../README.md)** · [Getting started](getting-started.md) · [API reference](api-reference.md) · [Model](models.md) · [FAQ](faq.md)

Terakhir diperbarui: **17 November 2026** · Dokumentasi resmi: <https://enrai.web.id/docs> · Harga & limit: <https://enrai.web.id/pricing>

Panduan ini menuntun Anda dari nol sampai request pertama ke **API AI gratis** Enrai — daftar akun, mengambil API key, dan memanggil endpoint yang **kompatibel OpenAI**. Waktu tempuh sekitar dua menit.

Dokumentasi resmi: <https://enrai.web.id/docs> · Daftar: <https://enrai.web.id/register> · Limit & harga: <https://enrai.web.id/pricing>

## Ringkasan cepat

| Item | Nilai |
|---|---|
| Base URL | `https://enrai.web.id/v1` |
| Endpoint chat | `POST https://enrai.web.id/v1/chat/completions` |
| Endpoint model | `GET https://enrai.web.id/v1/models` |
| Autentikasi | Header `Authorization: Bearer <API_KEY>` |
| Model awal | `Chatgpt` (lihat [models.md](models.md)) |
| Biaya | Gratis, tanpa kartu kredit (public beta) |

## 1. Buat akun

1. Buka <https://enrai.web.id/register>.
2. Isi email dan password, lalu selesaikan pendaftaran.
3. Tidak ada form pembayaran dan tidak ada kartu kredit yang diminta.

Sudah punya akun? Langsung ke <https://enrai.web.id/login>.

## 2. Ambil API key

1. Masuk ke dashboard.
2. Buka **API Keys**.
3. Klik buat key baru, lalu **salin segera** — key hanya ditampilkan sekali.

Simpan sebagai environment variable, bukan di dalam kode:

```bash
export ENRAI_API_KEY="YOUR_API_KEY"
```

Jika key bocor, hapus/rotasi dari dashboard dan buat yang baru. Jangan pernah commit key ke GitHub.

## 3. Request pertama

### cURL

```bash
curl https://enrai.web.id/v1/chat/completions \
  -H "Authorization: Bearer $ENRAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Chatgpt",
    "messages": [{"role": "user", "content": "Halo, ini request pertama saya."}]
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
    api_key=os.environ["ENRAI_API_KEY"],
)

res = client.chat.completions.create(
    model="Chatgpt",
    messages=[{"role": "user", "content": "Halo, ini request pertama saya."}],
)
print(res.choices[0].message.content)
```

### Node.js

```bash
npm install openai
```

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://enrai.web.id/v1",
  apiKey: process.env.ENRAI_API_KEY,
});

const res = await client.chat.completions.create({
  model: "Chatgpt",
  messages: [{ role: "user", content: "Halo, ini request pertama saya." }],
});
console.log(res.choices[0].message.content);
```

Kalau balasan berisi teks di `choices[0].message.content`, integrasi dasar Anda sudah benar.

Contoh yang lebih lengkap (termasuk streaming) ada di [`../examples/`](../examples/README.md).

## 4. Cek model yang aktif

```bash
curl https://enrai.web.id/v1/models \
  -H "Authorization: Bearer $ENRAI_API_KEY"
```

Panggil sekali saat aplikasi start, lalu **cache** hasilnya. Jangan memanggil endpoint ini di setiap request — limit-nya 60 request/menit per key.

## 5. Troubleshooting

| Gejala | Penyebab paling sering | Solusi |
|---|---|---|
| `401` | Key salah, kedaluwarsa, atau header kurang | Pastikan formatnya `Authorization: Bearer <key>` tanpa spasi tambahan |
| `429` | Melewati 20 request/menit (burst 5) | Backoff eksponensial, kurangi konkurensi, antrekan request |
| `502` | Semua provider di balik combo gagal | Ulangi beberapa saat lagi; ini bukan kesalahan payload Anda |
| `500` | Galat server | Coba lagi; kalau berulang, laporkan ke pemilik layanan |
| Balasan kosong | Upstream mengembalikan jawaban kosong | Perlakukan sebagai kegagalan, retry sekali, lalu tangani sebagai error |

Daftar kode error lengkap: [`api-reference.md`](api-reference.md#error).

## 6. Kalau butuh mengganti provider

Karena API ini mengikuti format OpenAI, pindah provider berarti mengganti dua hal: `base_url` dan `api_key`. Simpan keduanya sebagai konfigurasi, bukan konstanta:

```bash
ENRAI_BASE_URL=https://enrai.web.id/v1
ENRAI_MODEL=Chatgpt
ENRAI_API_KEY=YOUR_API_KEY
```

---

Sumber kebenaran tetap situs resmi: <https://enrai.web.id/docs>. Kembali ke [README](../README.md) · [API reference](api-reference.md) · [Model](models.md) · [FAQ](faq.md)
