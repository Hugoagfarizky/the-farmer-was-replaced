# The Farmer Was Replaced

Kumpulan kode saya untuk game pemrograman [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/) dan DLC-nya, **The Miner Was Replaced**. Saya mulai dari nol, dari farming lalu lanjut ke mining.

Repo ini bukan proyek resmi dan tidak berafiliasi dengan pengembang game.

## Isi repo

- `farming/`: kode untuk farming
- `mining/`: kode untuk mining
- `sync.ps1`: skrip untuk menyalin kode dari save `MinerRun` ke repo

## Kode farming

Setiap kode ditulis untuk leaderboard game dan berhenti sendiri saat target tercapai. Target otomatis menyesuaikan: farm 32×32 dengan banyak drone, atau farm 8×8 dengan satu drone.

| File | Hasil | Target banyak drone | Target satu drone |
|---|---|---|---|
| `farm_hay` | Hay | 2.000.000.000 | 100.000.000 |
| `farm_wood` | Wood | 10.000.000.000 | 500.000.000 |
| `farm_carrot` | Carrot | 2.000.000.000 | 100.000.000 |
| `farm_pumpkin` | Pumpkin | 200.000.000 | 10.000.000 |
| `farm_cactus` | Cactus | 33.554.432 | 131.072 |
| `farm_sunflower` | Power | 100.000 | 10.000 |
| `farm_maze` | Gold | 9.863.168 | 616.448 |
| `farm_dino` | Bone | 33.488.928 | Tidak ada |

`farm_weird` tidak punya leaderboard. Kode ini mengumpulkan 2.000.000 Weird Substance untuk `farm_maze` di farm asli, atau berhenti saat fertilizer habis.

## Penamaan file

Di dalam game, semua kode disimpan di satu folder save. Awalan nama file menentukan folder tujuannya di repo:

| Nama file di game | Folder di repo |
|---|---|
| `farm_hay` | `farming/` |
| `mine_coal` | `mining/` |

File tanpa awalan tersebut tidak ikut disalin. Saat memakai `import`, cukup tulis nama filenya, misalnya `import farm_hay`.

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

Skrip ini tidak pernah menghapus file di repo. Kalau ada file yang sudah dihapus di game, skrip hanya melaporkannya, dan file itu perlu dihapus sendiri dari repo.
