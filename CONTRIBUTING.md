# Panduan Kontribusi

Kumpulan kode farming dan mining untuk game The Farmer Was Replaced. Bukan proyek resmi dan tidak berafiliasi dengan pengembang game.

## Menjalankan

```bash
powershell -ExecutionPolicy Bypass -File sync.ps1
```

## Sebelum mengirim perubahan

- Satu file untuk satu leaderboard atau achievement, dan jaga nama file di bawah 20 karakter.
- Jalankan `sync.ps1` sebelum commit supaya isi repo sama dengan save game.
- Jangan commit `.env`, kunci API, atau hasil build.

## Alur kontribusi

1. `git checkout -b fix/nama-singkat`
2. Commit dengan pesan yang jelas.
3. Buka pull request ke `main`, jelaskan **apa** dan **kenapa**.

Untuk masalah keamanan, ikuti `SECURITY.md`, jangan buka issue publik.

## Lisensi

Dengan mengirim pull request, kontribusimu dirilis di bawah [MIT License](LICENSE).