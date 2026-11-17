# Daftar Model API AI Gratis Enrai (Chatgpt, Deepseek, GLM)

**← Kembali ke [README](../README.md)** · [Getting started](getting-started.md) · [API reference](api-reference.md) · [Model](models.md) · [FAQ](faq.md)

Terakhir diperbarui: **17 November 2026** · Dokumentasi resmi: <https://enrai.web.id/docs> · Harga & limit: <https://enrai.web.id/pricing>

Halaman ini menjelaskan model apa saja yang bisa dipanggil lewat **API AI gratis** Enrai, bagaimana nama model bekerja, dan cara mengecek model yang sedang aktif sebelum aplikasi berjalan.

Base URL: `https://enrai.web.id/v1` · Dokumentasi resmi: <https://enrai.web.id/docs> · Status model live: <https://enrai.web.id/#model>

## Daftar model (per 17 November 2026)

| Model | Kapabilitas | Streaming | Status |
|---|---|---|---|
| `Chatgpt` | Chat completion | Ya | Online |
| `Deepseek` | Chat completion | Ya | Online |
| `GLM` | Chat completion | Ya | Online |

Daftar ini diambil dari beranda `enrai.web.id`. Daftar otoritatif selalu `GET https://enrai.web.id/v1/models`.

## Nama model adalah alias, bukan nama vendor

`Chatgpt`, `Deepseek`, dan `GLM` adalah **alias combo**: satu nama bisa dilayani beberapa provider di belakangnya. Provider dikelola otomatis, sehingga:

- string model di kode Anda tidak perlu berubah saat provider berganti;
- jika satu provider gagal atau mengembalikan jawaban kosong, permintaan diulang ke anggota combo lain;
- kalau semua anggota gagal, API membalas `502` — bukan jawaban kosong dengan status `200`.

Karena itu, jangan menyamakan `Chatgpt` dengan versi model tertentu dari vendor mana pun. Perlakukan sebagai nama layanan.

## Cara mengecek model yang aktif

```bash
curl https://enrai.web.id/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Praktik yang disarankan:

1. Panggil saat aplikasi start, simpan hasilnya di cache/memori.
2. Refresh berkala (mis. sekali per jam), jangan per request — limit endpoint ini 60 request/menit per key.
3. Jika model yang Anda pakai hilang dari daftar, fallback ke model lain yang tersedia dan log peringatan.

## Kapabilitas

| Kapabilitas | Status |
|---|---|
| Chat completion | Tersedia untuk ketiga model |
| Streaming (SSE) | Tersedia |
| Daftar model dinamis | Tersedia (`GET /v1/models`) |
| Context window per model | Belum dipublikasikan |
| Batas token output per model | Belum dipublikasikan |
| Vision / image input | Belum dipublikasikan |
| Function calling / tools | Belum dipublikasikan |

Jangan mengandalkan kemampuan yang belum tercantum di <https://enrai.web.id/docs>.

## Memilih model

- **`Chatgpt`** — pilihan default untuk percakapan umum; dipakai di seluruh contoh dokumentasi ini.
- **`Deepseek`** — alternatif untuk tugas teks/penalaran; cocok dibandingkan langsung dengan model lain karena format request identik.
- **`GLM`** — alternatif ketiga; berguna saat ingin membandingkan gaya jawaban tanpa mengubah kode.

Karena ketiganya memakai format request yang sama, mengganti model cukup mengganti satu string:

```python
response = client.chat.completions.create(
    model="Deepseek",  # sebelumnya "Chatgpt"
    messages=[{"role": "user", "content": "Halo"}],
)
```

---

Kembali ke [README](../README.md) · [Getting started](getting-started.md) · [API reference](api-reference.md) · [FAQ](faq.md)
