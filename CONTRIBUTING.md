# Berkontribusi

Terima kasih sudah mau membantu repo **API AI gratis Enrai** — dokumentasi dan contoh kode untuk <https://enrai.web.id>.

## Kontribusi yang paling berguna

- **Koreksi fakta:** situs berubah (limit, model, endpoint) tetapi dokumentasi di sini tertinggal.
- **Contoh kode baru:** PHP, Go, Rust, Java/Kotlin, atau integrasi bot Telegram/WhatsApp.
- **Perbaikan tautan mati dan typo.**

## Aturan

1. **Jangan kirim API key, token, atau file `.env`.** Pakai `YOUR_API_KEY` atau environment variable `ENRAI_API_KEY`.
2. **Jangan mengarang fakta.** Kalau sebuah informasi tidak ada di <https://enrai.web.id/docs>, <https://enrai.web.id/pricing>, atau beranda, tulis **"Belum dipublikasikan"** dan jelaskan di PR. Jangan menebak angka.
3. **Satu perubahan, satu tujuan.** PR kecil lebih cepat ditinjau.
4. **Contoh harus jalan.** Jalankan dulu (lihat di bawah) dan sebutkan perintah yang Anda pakai di deskripsi PR.
5. **Tanpa URL lokal.** Satu-satunya alamat layanan yang boleh muncul adalah `https://enrai.web.id` — tidak ada alamat loopback maupun nomor port.

## Menjalankan contoh

```bash
export ENRAI_API_KEY="YOUR_API_KEY"   # daftar gratis di https://enrai.web.id/register

# Python (SDK openai)
cd examples/python && pip install -r requirements.txt
python chat.py "Halo"

# Node.js (tanpa dependency, Node 18+)
cd examples/nodejs
node chat.mjs "Halo"
node chat.mjs --stream "Hitung 1 sampai 10"

# cURL
cd examples/curl
./models.sh && ./chat.sh "Halo"
```

## Gaya penulisan dokumentasi

- Bahasa Indonesia untuk dokumen utama; README punya ringkasan English di bagian akhir.
- H1 memuat kata kunci alami; satu kalimat pengantar di atas; breadcrumb kembali ke README di setiap file `docs/`.
- Kalimat pendek, tanpa klaim yang tidak bisa dibuktikan ("tercepat", "terbaik", "100% akurat").
- Tabel untuk data berulang (model, limit, kode error); blok `<details>` untuk bagian panjang.
- Setiap contoh kode menyebut cara menjalankan dan cara menangani `401`/`429`/`502`.

## Format commit

[Conventional Commits](https://www.conventionalcommits.org/id/v1.0.0/):

```
docs: jelaskan rate limit per key
docs(readme): tambah contoh streaming Node.js
feat(examples): tambah contoh PHP
ci: tambah pemeriksaan tautan
chore: perbarui Dependabot
```

Satu commit untuk satu kelompok perubahan, pesan dalam bahasa Indonesia atau Inggris (konsisten dalam satu PR).

## Alur kerja

```bash
git clone https://github.com/enraidev/enrai-free-ai-api.git
cd enrai-free-ai-api
git checkout -b docs/perbaikan-singkat
# edit...
git commit -m "docs: perjelas tabel kode error"
git push origin docs/perbaikan-singkat
```

Lalu buka Pull Request menggunakan template yang tersedia. Sertakan sumber fakta untuk setiap perubahan teknis.

## Pemeriksaan otomatis

CI menjalankan markdownlint, pemeriksaan tautan (401 pada `/v1/*` wajar karena butuh API key), cek sintaks Python/Node/bash, dan penjaga URL lokal. Pastikan semua hijau sebelum meminta review.

## Pertanyaan

- Masalah dokumentasi atau bug di repo: buka [issue](https://github.com/enraidev/enrai-free-ai-api/issues) atau [diskusi](https://github.com/enraidev/enrai-free-ai-api/discussions).
- Masalah layanan (akun, key, kuota): gunakan kontak resmi di <https://enrai.web.id>.
- Kerentanan keamanan: ikuti [SECURITY.md](SECURITY.md), jangan buka issue publik.
