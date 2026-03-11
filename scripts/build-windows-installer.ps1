$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$outputDir = Join-Path $projectRoot "dist-windows"

if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

$dockerOs = docker version --format '{{.Server.Os}}' 2>$null
if ($LASTEXITCODE -ne 0) {
    throw "Docker não está disponível. Instale e inicie o Docker Desktop antes de continuar."
}

if ($dockerOs.Trim().ToLower() -ne 'windows') {
    throw "O Docker está em modo Linux containers. No Docker Desktop, use 'Switch to Windows containers...' e execute novamente."
}

Set-Location $projectRoot

docker build -f Dockerfile.windows -t saciar-installer-win .
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao criar a imagem Docker para o instalador Windows."
}

docker run --rm -v "${outputDir}:C:\out" saciar-installer-win
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao gerar o instalador Windows dentro do container."
}

Write-Host "Instalador gerado em: $outputDir"