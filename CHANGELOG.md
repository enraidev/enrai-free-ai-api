# Changelog

Semua perubahan penting pada repo ini dicatat di sini. Format mengikuti [Keep a Changelog](https://keepachangelog.com/id/1.1.0/), dan versi mengikuti [Semantic Versioning](https://semver.org/lang/id/).

## [Unreleased]

## [1.0.0] - 2026-11-17

### Added

- README berbahasa Indonesia dengan ringkasan English, banner, diagram arsitektur, tabel model, tabel rate limit, contoh cURL/Python/Node.js, dan FAQ.
- `docs/getting-started.md`, `docs/api-reference.md`, `docs/models.md`, `docs/faq.md`.
- Contoh runnable: `examples/python` (SDK OpenAI), `examples/nodejs` (fetch tanpa dependensi), `examples/curl`.
- `examples/openai-sdk` untuk Python dan Node.js dengan paket resmi `openai`.
- File komunitas: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, template issue dan pull request, `CODEOWNERS`.
- Workflow CI (markdownlint, pemeriksaan tautan, cek sintaks contoh, penjaga URL lokal) dan konfigurasi Dependabot.
- Aset merek: `assets/banner.svg` dan `assets/social-preview.png` (dibuat oleh `scripts/generate_assets.py`).
- Halaman `index.html` dengan metadata SEO, JSON-LD, `sitemap.xml`, dan `llms.txt`.

### Changed

- Repo berganti nama dari `enrai-promo` menjadi `enrai-free-ai-api`; alamat lama tetap mengarah ke repo baru.
- README lama diganti dokumentasi lengkap; referensi URL lokal dihapus.
- Lisensi dipisah: MIT untuk kode contoh, CC BY 4.0 untuk dokumentasi.

[Unreleased]: https://github.com/enraidev/enrai-free-ai-api/commits/main
[1.0.0]: https://github.com/enraidev/enrai-free-ai-api/releases
