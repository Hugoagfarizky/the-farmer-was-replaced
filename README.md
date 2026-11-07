# The Farmer Was Replaced

My code for the programming game [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/) and its DLC, **The Miner Was Replaced**. I started from scratch with farming, then moved on to mining.

This is not an official project and is not affiliated with the game's developers.

## Repository contents

- `farming/`: farming code
- `mining/progress_achievement/`: my mining journey from the first dig to the last achievement, one achievement per file (see [mining/progress_achievement/README.md](mining/progress_achievement/README.md))
- `mining/best/`: the best code for each mining item
- `sync.ps1`: copies code from the `MinerRun` save into the repo

## Farming code

Each script targets one of the game's leaderboards and stops when it reaches the goal. The goal adapts automatically: a 32×32 farm with multiple drones, or an 8×8 farm with a single drone.

| File | Produces | Multi-drone goal | Single-drone goal |
|---|---|---|---|
| `farm_hay` | Hay | 2,000,000,000 | 100,000,000 |
| `farm_wood` | Wood | 10,000,000,000 | 500,000,000 |
| `farm_carrot` | Carrot | 2,000,000,000 | 100,000,000 |
| `farm_pumpkin` | Pumpkin | 200,000,000 | 10,000,000 |
| `farm_cactus` | Cactus | 33,554,432 | 131,072 |
| `farm_sunflower` | Power | 100,000 | 10,000 |
| `farm_maze` | Gold | 9,863,168 | 616,448 |
| `farm_dino` | Bone | 33,488,928 | None |

`farm_weird` has no leaderboard. It collects 2,000,000 Weird Substance for running `farm_maze` on the real farm, or stops when the fertilizer runs out.

## File naming

The game keeps all code in one save folder. A file's prefix decides where it goes in the repo:

| File name in the game | Repo folder |
|---|---|
| `farm_hay` | `farming/` |
| `mine_coal` | `mining/best/` |
| `1_digging_down` | `mining/progress_achievement/` |

Files in `mining/progress_achievement/` are named after their achievement, with their place in the order in front, for example `1_digging_down`. The game cuts file names at 20 characters, so keep names short.

Files without one of these prefixes aren't copied. When using `import`, just write the file name, for example `import farm_hay`.

## Updating

1. Copy the latest code from the game save:

   ```powershell
   powershell -ExecutionPolicy Bypass -File sync.ps1
   ```

2. Commit and upload the changes:

   ```powershell
   git add .
   git commit -m "Update code"
   git push
   ```

To copy from a different save, add `-SaveName SaveName` to the end of the first command.

The script never deletes files from the repo. If a file was deleted in the game, the script only reports it, and you need to delete it from the repo yourself.
