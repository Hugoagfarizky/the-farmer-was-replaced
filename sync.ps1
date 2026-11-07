# Copies your code from the game's save folder into the repo, sorted by file name:
#   farm_*.py goes to farming/, mine_*.py goes to mining/best/,
#   and mp##_*.py goes to mining/progress/.
# Only reads the save folder, and never deletes anything from the repo.
param(
    [string]$SaveName = "MinerRun"
)

$saveDir = Join-Path $env:USERPROFILE "AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\$SaveName"
$targets = [ordered]@{ "farm_*.py" = "farming"; "mine_*.py" = "mining\best"; "mp[0-9][0-9]_*.py" = "mining\progress" }

if (-not (Test-Path -LiteralPath $saveDir)) {
    Write-Error "Save '$SaveName' not found at: $saveDir"
    exit 1
}

$sourceFiles = @(Get-ChildItem -LiteralPath $saveDir -Filter "*.py" -File |
    Where-Object { $_.Name -ne "__builtins__.py" })

foreach ($pattern in $targets.Keys) {
    $targetDir = Join-Path $PSScriptRoot $targets[$pattern]
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null

    $matched = @($sourceFiles | Where-Object { $_.Name -like $pattern })
    foreach ($file in $matched) {
        Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $targetDir $file.Name) -Force
    }
    Write-Output "$($targets[$pattern])/: copied $($matched.Count) file(s)."

    # Files missing from the save may be new or deleted, so they are only reported.
    $savedNames = $matched | ForEach-Object { $_.Name }
    Get-ChildItem -LiteralPath $targetDir -Filter "*.py" -File |
        Where-Object { $savedNames -notcontains $_.Name } |
        ForEach-Object { Write-Output "  Not in save, kept in repo: $($_.Name)" }
}

$skipped = @($sourceFiles | Where-Object { $_.Name -notlike "farm_*.py" -and $_.Name -notlike "mine_*.py" -and $_.Name -notlike "mp[0-9][0-9]_*.py" })
foreach ($file in $skipped) {
    Write-Output "Skipped, needs a farm_, mine_, or mp##_ prefix: $($file.Name)"
}
