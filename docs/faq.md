# FAQ API AI Gratis Enrai: Pertanyaan yang Sering Ditanyakan

**← Kembali ke [README](../README.md)** · [Getting started](getting-started.md) · [API reference](api-reference.md) · [Model](models.md) · [FAQ](faq.md)

Terakhir diperbarui: **17 November 2026** · Dokumentasi resmi: <https://enrai.web.id/docs> · Harga & limit: <https://enrai.web.id/pricing>

Jawaban singkat untuk pertanyaan paling umum tentang **API AI gratis** Enrai — layanan **LLM API** dengan endpoint **kompatibel OpenAI**. Semua jawaban mengacu ke situs resmi <https://enrai.web.id> per 17 November 2026.

## Apakah API AI Enrai benar-benar gratis?

Ya. Selama masa **public beta**, Enrai menyediakan tier gratis dengan limit yang dipublikasikan, dan pendaftaran tidak meminta kartu kredit. Rincian harga ada di <https://enrai.web.id/pricing>.

## Apakah Enrai kompatibel dengan OpenAI SDK?

Ya. Endpoint-nya mengikuti format OpenAI: `POST /v1/chat/completions` dan `GET /v1/models`. Anda hanya perlu mengganti `baseURL` menjadi `https://enrai.web.id/v1` dan memakai API key Enrai; struktur request, response, dan streaming tidak berubah.

## Bagaimana cara mendapatkan API key?

1. Daftar di <https://enrai.web.id/register>.
2. Masuk dashboard, buka **API Keys**.
3. Buat key baru dan salin segera — key hanya ditampilkan **sekali**.

Panduan langkah demi langkah: [getting-started.md](getting-started.md).

## Model apa saja yang tersedia?

`Chatgpt`, `Deepseek`, dan `GLM` — lihat [models.md](models.md). Daftar terbaru selalu bisa dicek lewat `GET https://enrai.web.id/v1/models`.

## Berapa rate limit-nya?

| Endpoint | Limit |
|---|---|
| `POST /v1/chat/completions` | 20 request/menit (burst 5) |
| `GET /v1/models` | 60 request/menit |

Berlaku per API key. Jika terlampaui, server membalas `429`.

## Apakah streaming didukung?

Ya. Kirim `"stream": true`; response dikirim sebagai Server-Sent Events dan diakhiri `[DONE]`. Detail: [api-reference.md](api-reference.md#streaming).

## Bahasa apa yang bisa dipakai?

Bahasa apa pun yang punya HTTP client: Python, JavaScript/Node.js, PHP, Go, Rust, Java, Kotlin, dan sebagainya. Kalau bahasa tersebut punya SDK OpenAI, SDK itu bisa dipakai langsung dengan base URL Enrai.

## Apakah ada dukungan vision atau function calling?

Belum ada dokumentasi resminya di situs. Jangan merancang fitur yang bergantung pada kemampuan ini sebelum memastikan di <https://enrai.web.id/docs>. Statusnya ditulis apa adanya di [models.md](models.md): belum dipublikasikan.

## Apakah aman untuk produksi?

API ini berstatus **public beta**. Cocok untuk prototipe, tools internal, dan eksperimen. Untuk layanan yang tidak boleh gagal, siapkan provider kedua sebagai fallback — karena formatnya OpenAI, berpindah provider hanya mengganti base URL dan key.

## Apa yang harus dilakukan saat menerima `502`?

`502` berarti provider upstream gagal setelah failover dicoba. Ulangi permintaan setelah jeda singkat; payload Anda biasanya tidak salah. Kalau berulang dalam waktu lama, cek beranda untuk status model.

## Apakah ada halaman status layanan?

Belum dipublikasikan. Status model dan daftar yang sedang aktif terlihat di beranda bagian Models (<https://enrai.web.id/#model>) dan di `GET https://enrai.web.id/v1/models`.

## Ke mana harus melaporkan bug atau bertanya?

Kanal komunitas resmi (grup chat) belum dipublikasikan. Untuk pertanyaan akun, key, atau kuota, gunakan kontak yang tercantum di <https://enrai.web.id>. Untuk masalah dokumentasi di repo ini, buka issue di GitHub; lihat [CONTRIBUTING.md](../CONTRIBUTING.md).

## Di mana dokumentasi lengkapnya?

- Dokumentasi resmi: <https://enrai.web.id/docs>
- Harga & limit: <https://enrai.web.id/pricing>
- Di repo ini: [getting-started.md](getting-started.md) · [api-reference.md](api-reference.md) · [models.md](models.md)

---

Kembali ke [README](../README.md) · Situs resmi: <https://enrai.web.id>
