# Gerar o instalador `.exe` no Windows com Docker

## Requisito

No Docker Desktop, troque para `Windows containers` antes de executar o processo.

## Passos no PC do cliente

Abra o PowerShell na raiz do projeto clonado e execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-windows-installer.ps1
```

## Resultado

O arquivo `.exe` será gerado na pasta `dist-windows`.

Nome esperado do instalador:

`Instalador - Sistema de gerenciamento saciar.exe`

O atalho criado pelo instalador terá o nome:

`Sistema de gerenciamento Saciar`