$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

if (-not (Test-Path "dist-windows")) {
    New-Item -ItemType Directory -Path "dist-windows" | Out-Null
}

jpackage `
  --type exe `
  --input target `
  --name "Sistema de gerenciamento Saciar" `
  --main-jar saciar-sistema-1.0.0.jar `
  --main-class com.saciar.SaciarApplication `
  --icon src\assets\icone.ico `
  --win-shortcut `
  --win-menu `
  --win-menu-group "Saciar" `
  --app-version 1.0.0 `
  --vendor "Saciar" `
  --dest dist-windows

Write-Host "Instalador gerado em dist-windows"