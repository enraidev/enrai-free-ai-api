# Kebijakan Keamanan (Security Policy)

Repo ini berisi **dokumentasi dan contoh kode** untuk API di <https://enrai.web.id>. Tidak ada kode server produksi di sini.

## Melaporkan kerentanan

**Jangan** membuka issue publik untuk masalah keamanan.

1. **Cara utama — GitHub Security Advisories:** buka tab **Security** repo ini → **Report a vulnerability**. Laporan bersifat privat dan hanya terlihat oleh maintainer.
2. **Alternatif — email:** kirim ke **enraigaming@yahoo.com** dengan subjek `[SECURITY] enrai-free-ai-api`.

Sertakan bila ada: deskripsi masalah, langkah reproduksi, dampak yang Anda perkirakan, dan versi/contoh kode yang terdampak.

## Yang termasuk lingkup

- Kebocoran API key atau data pribadi di dalam repo ini (file, commit, issue, atau PR).
- Contoh kode di `examples/` yang bisa menimbulkan risiko jika disalin apa adanya (mis. mencetak key ke log).
- Tautan yang mengarahkan pengguna ke domain tiruan.

## Di luar lingkup

- Masalah pada layanan API di `enrai.web.id`, akun, kuota, atau tagihan — laporkan lewat kontak resmi di situs.
- Hasil model (jawaban yang tidak akurat) — itu bukan kerentanan keamanan.

## Waktu respons

Laporan diproses sebaik mungkin dalam beberapa hari kerja. Kami akan mengonfirmasi penerimaan, menjelaskan hasil penilaian, dan memberi tahu saat perbaikan dirilis.

## Versi yang didukung

Hanya isi terbaru di branch `main` yang didukung.
