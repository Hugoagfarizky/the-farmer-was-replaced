# Copies your code from the game's save folder into scripts/.
# Only reads the save folder; it never changes anything there.
param(
    [string]$SaveName = "MinerRun"
)

$saveDir = Join-Path $env:USERPROFILE "AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\$SaveName"
$scriptsDir = Join-Path $PSScriptRoot "scripts"

if (-not (Test-Path -LiteralPath $saveDir)) {
    Write-Error "Save '$SaveName' not found at: $saveDir"
    exit 1
}

New-Item -ItemType Directory -Force -Path $scriptsDir | Out-Null

$sourceFiles = @(Get-ChildItem -LiteralPath $saveDir -Filter "*.py" -File |
    Where-Object { $_.Name -ne "__builtins__.py" })

# Safety stop: an empty save would otherwise wipe every script in the repo.
if ($sourceFiles.Count -eq 0) {
    Write-Error "No .py files found in save '$SaveName'. Nothing was changed."
    exit 1
}

foreach ($file in $sourceFiles) {
    Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $scriptsDir $file.Name) -Force
}

# Files deleted in the game are deleted here too, so the repo matches the save.
$sourceNames = $sourceFiles | ForEach-Object { $_.Name }
Get-ChildItem -LiteralPath $scriptsDir -Filter "*.py" -File |
    Where-Object { $sourceNames -notcontains $_.Name } |
    Remove-Item -Force

Write-Output "Synced $($sourceFiles.Count) file(s) from save '$SaveName' to scripts/."
