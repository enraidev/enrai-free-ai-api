# Contoh dengan OpenAI SDK resmi

Dua contoh yang memakai paket resmi `openai`, bukan `fetch` atau `curl`. Gunanya: memastikan integrasi Anda bekerja dengan klien yang paling mungkin sudah ada di proyek Anda.

Bedanya dengan contoh di `../python` dan `../nodejs`: folder ini mengikuti versi SDK terbaru (Python ≥ 3.50, Node.js ≥ 7), mendukung flag `--stream`, dan memetakan kode error HTTP ke pesan yang bisa langsung ditindaklanjuti.

| Folder | Isi | Prasyarat |
|---|---|---|
| [`python/`](python/chat.py) | `chat.py` (chat + `--stream`), `requirements.txt` | Python ≥ 3.10 |
| [`nodejs/`](nodejs/chat.mjs) | `chat.mjs` (chat + `--stream`), `package.json` | Node.js ≥ 22 |

Semua contoh membaca API key dari environment variable `ENRAI_API_KEY` dan berhenti bila variabel itu kosong — tidak ada key asli di repo ini.

```bash
export ENRAI_API_KEY="YOUR_API_KEY"   # https://enrai.web.id/register
```

## Python

```bash
cd python
pip install -r requirements.txt
python chat.py "Jelaskan API kompatibel OpenAI dalam satu paragraf."
python chat.py --stream "Hitung 1 sampai 10."
```

## Node.js

```bash
cd nodejs
npm install
node chat.mjs "Jelaskan API kompatibel OpenAI dalam satu paragraf."
node chat.mjs --stream "Hitung 1 sampai 10."
```

## Yang perlu diperhatikan

- Base URL yang dipakai: `https://enrai.web.id/v1` (SDK menambahkan `/chat/completions` sendiri).
- Model default `Chatgpt`; ganti lewat `ENRAI_MODEL=Deepseek` atau `ENRAI_MODEL=GLM`.
- `401` berarti key salah, `429` berarti rate limit (20 request/menit, burst 5), `502` berarti seluruh provider di balik combo sedang gagal.
- Jawaban `200` dengan isi kosong diperlakukan sebagai kegagalan di kedua contoh.

Referensi: [../docs/api-reference.md](../../docs/api-reference.md) · [../docs/models.md](../../docs/models.md)
