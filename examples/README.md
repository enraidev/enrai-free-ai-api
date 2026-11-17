# Contoh Kode API AI Gratis Enrai (Python, Node.js, cURL)

Contoh yang bisa langsung dijalankan untuk memanggil **API AI gratis** Enrai, endpoint **kompatibel OpenAI** di `https://enrai.web.id/v1`.

Semua contoh membaca API key dari environment variable `ENRAI_API_KEY` dan menolak jalan tanpa key — tidak ada key asli di repo ini.

```bash
export ENRAI_API_KEY="YOUR_API_KEY"
```

Daftar akun gratis: <https://enrai.web.id/register> · Dokumentasi: <https://enrai.web.id/docs>

## Folder

| Folder | Isi |
|---|---|
| [`python/`](python/chat.py) | `chat.py` (chat completion), `stream.py` (streaming SSE), `requirements.txt` |
| [`nodejs/`](nodejs/chat.mjs) | `chat.mjs` (chat + streaming, tanpa dependency), `package.json` |
| [`curl/`](curl/chat.sh) | `models.sh`, `chat.sh`, `stream.sh` |
| [`openai-sdk/`](openai-sdk/README.md) | Contoh paket resmi `openai` untuk Python dan Node.js |

Model default di semua contoh: `Chatgpt`. Ganti dengan `Deepseek` atau `GLM` (lihat [../docs/models.md](../docs/models.md)).

## Python

```bash
cd python
pip install -r requirements.txt
python chat.py "Jelaskan API kompatibel OpenAI dalam satu paragraf."
python stream.py "Tulis puisi pendek tentang API."
```

## Node.js

Contoh memakai `fetch` bawaan (Node.js 18+), **tanpa dependency**:

```bash
cd nodejs
node chat.mjs "Jelaskan API kompatibel OpenAI dalam satu paragraf."
node chat.mjs --stream "Hitung 1 sampai 10."
```

Kalau lebih suka SDK resmi `openai`, polanya sama seperti contoh Python: ganti `baseURL` menjadi `https://enrai.web.id/v1`.

## cURL

```bash
cd curl
./models.sh
./chat.sh "Halo dari cURL!"
./stream.sh "Hitung 1 sampai 10."
```

## Penanganan error yang dipakai contoh

- `401` — key salah/hilang: periksa `ENRAI_API_KEY`.
- `429` — rate limit (20 request/menit, burst 5): contoh menampilkan pesan dan saran backoff.
- `502` — upstream gagal setelah failover: ulangi setelah jeda.
- Balasan kosong — diperlakukan sebagai kegagalan, bukan sukses.

Referensi lengkap: [../docs/api-reference.md](../docs/api-reference.md).
