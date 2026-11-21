<#
  Installe ce qu'il faut et affiche le portfolio (Windows, PowerShell 5.1 ou plus récent).

  Utilisation (dans le dossier du portfolio) :
    powershell -ExecutionPolicy Bypass -File install.ps1               installe uv si besoin, génère le site, l'ouvre
    powershell -ExecutionPolicy Bypass -File install.ps1 preview       idem, puis sert docs/ sur http://localhost:8000
    powershell -ExecutionPolicy Bypass -File install.ps1 preview-all   les 3 modèles côte à côte sur http://localhost:8000

  Options : -Port 8080 (autre port), -NoOpen (ne pas ouvrir le navigateur), -NoServe (pas de serveur local).
  Le script peut être relancé autant de fois que nécessaire : il ne réinstalle rien d'inutile.
#>
param(
    [ValidateSet("build", "preview", "preview-all")]
    [string]$Action = "build",
    [int]$Port = 8000,
    [switch]$NoOpen,
    [switch]$NoServe
)

$ErrorActionPreference = "Stop"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }
$env:PYTHONIOENCODING = "utf-8"
Set-Location -LiteralPath $PSScriptRoot

function Write-Step([string]$Message) { Write-Host "==> $Message" -ForegroundColor Cyan }
function Write-Ok([string]$Message) { Write-Host "    $Message" -ForegroundColor Green }
function Stop-WithError([string]$Message) {
    Write-Host ""
    Write-Host "Erreur : $Message" -ForegroundColor Red
    exit 1
}

function Find-Uv {
    $command = Get-Command uv -ErrorAction SilentlyContinue
    if ($command) { return $command.Source }
    $candidates = @(
        (Join-Path $env:USERPROFILE ".local\bin\uv.exe"),
        (Join-Path $env:USERPROFILE ".cargo\bin\uv.exe"),
        (Join-Path $env:LOCALAPPDATA "Programs\uv\uv.exe")
    )
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate) { return $candidate }
    }
    return $null
}

function Invoke-Uv {
    # Lance uv sans que PowerShell 5.1 transforme ses messages de progression en erreurs.
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & $script:Uv @args | Out-Host
    $code = $LASTEXITCODE
    $ErrorActionPreference = $previous
    return $code
}

Write-Host ""
Write-Host "Portfolio Markdown : installation et aperçu" -ForegroundColor White
Write-Host ""

if (-not (Test-Path -LiteralPath "build.py")) {
    Stop-WithError "build.py est introuvable. Lancez ce script depuis le dossier du portfolio."
}

# 1. uv
Write-Step "Recherche de uv (gestionnaire Python)"
$script:Uv = Find-Uv
if ($script:Uv) {
    Write-Ok "uv est déjà installé : $script:Uv"
} else {
    Write-Step "uv absent : installation avec l'installateur officiel (astral.sh)"
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
        Invoke-RestMethod -Uri "https://astral.sh/uv/install.ps1" | Invoke-Expression
    } catch {
        Stop-WithError "l'installation de uv a échoué ($($_.Exception.Message)). Vérifiez la connexion Internet, ou installez uv à la main : https://docs.astral.sh/uv/"
    }
    $env:Path = (Join-Path $env:USERPROFILE ".local\bin") + ";" + $env:Path
    $script:Uv = Find-Uv
    if (-not $script:Uv) {
        Stop-WithError "uv semble installé mais reste introuvable. Fermez puis rouvrez PowerShell et relancez ce script."
    }
    Write-Ok "uv installé : $script:Uv"
}
$version = & $script:Uv --version
Write-Ok "Version : $version"

# 2. Aperçu des trois modèles
if ($Action -eq "preview-all") {
    Write-Step "Génération des trois modèles dans previews\"
    $extra = @("--port", "$Port")
    if ($NoOpen) { $extra += "--no-open" }
    if ($NoServe) { $extra += "--no-serve" }
    $code = Invoke-Uv run build.py --preview-all @extra
    if ($code -ne 0) { Stop-WithError "la génération des aperçus a échoué (voir les messages ci-dessus)." }
    exit 0
}

# 3. Génération du site
Write-Step "Génération du site (content\ vers docs\)"
$code = Invoke-Uv run build.py
if ($code -ne 0) {
    Stop-WithError "le site n'a pas été généré. Corrigez les points indiqués ci-dessus puis relancez le script."
}
$index = Join-Path $PSScriptRoot "docs\index.html"
Write-Ok "Site prêt : $index"

# 4. Ouverture
if ($Action -eq "build") {
    if (-not $NoOpen) {
        Write-Step "Ouverture dans le navigateur"
        Start-Process $index
    }
    Write-Host ""
    Write-Host "Terminé. Après chaque modification de content\, relancez ce script (ou : uv run build.py)." -ForegroundColor White
    exit 0
}

if ($NoServe) { exit 0 }
Write-Step "Aperçu local (serveur http.server de Python, Ctrl+C pour arrêter)"
# build.py choisit le port suivant si $Port est déjà pris par un autre programme.
$serveArgs = @("run", "build.py", "--serve", "--port", "$Port")
if ($NoOpen) { $serveArgs += "--no-open" }
$code = Invoke-Uv @serveArgs
if ($code -ne 0) {
    Stop-WithError "le serveur local n'a pas pu démarrer (port $Port déjà utilisé ?). Essayez : install.ps1 preview -Port 8080"
}
