# Install the yt-* skills for Google Antigravity on Windows.
#   .\install.ps1               global      -> $HOME\.gemini\config\skills
#   .\install.ps1 -Workspace    this folder -> .\.agents\skills
param([switch]$Workspace)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($Workspace) {
  $dest  = Join-Path (Get-Location) ".agents\skills"
  $voice = Join-Path (Get-Location) ".agents\youtube"
} else {
  $dest  = Join-Path $HOME ".gemini\config\skills"
  $voice = Join-Path $HOME ".gemini\config\youtube"
}
New-Item -ItemType Directory -Force -Path $dest, $voice | Out-Null
Copy-Item -Recurse -Force (Join-Path $here "skills\yt-*") $dest
Get-ChildItem -Path $dest -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
$v = Join-Path $voice "voice.md"
if (-not (Test-Path $v)) { Copy-Item (Join-Path $here "templates\voice.md") $v }
Write-Host "Installed 11 skills to $dest"
Write-Host "Fill in your voice profile: $v"
