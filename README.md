# The Miner Was Replaced

Kumpulan kode saya untuk **The Miner Was Replaced**, DLC dari game pemrograman [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/).

Repo ini bukan proyek resmi dan tidak berafiliasi dengan pengembang game.

## Isi repo

- `scripts/`: kode dari save `MinerRun`
- `sync.ps1`: skrip untuk menyalin kode dari save game ke `scripts/`

## Cara memperbarui

1. Salin kode terbaru dari save game:

   ```powershell
   powershell -ExecutionPolicy Bypass -File sync.ps1
   ```

2. Simpan dan unggah perubahannya:

   ```powershell
   git add .
   git commit -m "Update kode"
   git push
   ```

Untuk menyalin dari save lain, tambahkan `-SaveName NamaSave` di akhir perintah pertama.
