# Contributing

Terima kasih sudah mau membantu repo **API AI gratis Enrai** ini (dokumentasi + contoh kode untuk <https://enrai.web.id>).

## Yang paling berguna

- Koreksi fakta: kalau situs `enrai.web.id` berubah (limit, model, endpoint) dan dokumentasi di sini tertinggal.
- Contoh kode baru: PHP, Go, Rust, Java/Kotlin, atau integrasi bot Telegram/WhatsApp.
- Perbaikan typo dan tautan mati.

## Aturan

1. **Jangan kirim API key, token, atau file `.env`.** Pakai `YOUR_API_KEY` atau environment variable.
2. **Jangan mengarang fakta.** Kalau informasi tidak ada di <https://enrai.web.id/docs>, <https://enrai.web.id/pricing>, atau beranda, tandai dengan placeholder `[ISI: ...]` dan jelaskan di PR.
3. **Satu perubahan, satu tujuan.** PR kecil lebih cepat ditinjau daripada PR besar campuran.
4. **Contoh harus jalan.** Jalankan dulu sebelum mengirim; sebutkan perintah yang Anda pakai di deskripsi PR.
5. **Tanpa URL lokal.** Hanya `https://enrai.web.id` yang boleh muncul sebagai alamat layanan.

## Alur

```bash
git clone https://github.com/enraidev/enrai-free-ai-api.git
cd enrai-free-ai-api
git checkout -b docs/perbaikan-singkat
# edit...
git commit -m "docs: jelaskan rate limit per key"
git push origin docs/perbaikan-singkat
```

Lalu buka Pull Request dan jelaskan apa yang berubah beserta sumber faktanya.

## Gaya penulisan

- Bahasa Indonesia untuk dokumen utama; ringkasan Inggris untuk README.
- Kalimat pendek, tanpa klaim berlebihan ("tercepat", "terbaik") yang tidak bisa dibuktikan.
- Kode: sertakan cara menjalankan dan penanganan error yang realistis.

## Pertanyaan

Buka issue di repo ini. Masalah layanan (akun, key, kuota) bukan urusan repo — gunakan kanal resmi di <https://enrai.web.id>.
