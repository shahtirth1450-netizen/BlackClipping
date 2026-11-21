# ClipKontrast - one-click start for Windows.
# First run: installs Python and ffmpeg if missing (with winget), sets up a private Python folder (.venv)
# and the packages. Every run: starts ClipKontrast and opens it in your browser.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

function Say($msg, $color = "White") { Write-Host "  $msg" -ForegroundColor $color }
function Fail($msg) { Write-Host ""; Say $msg "Red"; Write-Host ""; exit 1 }
function Refresh-Path {
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
}
function Has-Winget { [bool](Get-Command winget -ErrorAction SilentlyContinue) }

Write-Host ""
Say "=== BlackClipping - 100% Viral AI Clipper ===" "Green"
Write-Host ""

# ---- Long folder paths break the speech model on Windows (260 character limit)
if ($Root.Length -gt 80) {
    Say "This folder's path is long:" "Yellow"
    Say "  $Root" "Yellow"
    Say "If the speech model fails to load, move the folder to C:\ClipKontrast and run this again." "Yellow"
    Write-Host ""
}

# ---- Python 3.10+
function Find-Python {
    foreach ($cand in @("py -3.12", "py -3.11", "py -3.10", "py -3", "python")) {
        $parts = $cand -split " "
        $exe = $parts[0]; $args_ = @($parts | Select-Object -Skip 1)
        if (-not (Get-Command $exe -ErrorAction SilentlyContinue)) { continue }
        try {
            $ok = & $exe @args_ -c "import sys; print(1 if (3,10) <= sys.version_info[:2] < (3,14) else 0)" 2>$null
            if ($LASTEXITCODE -eq 0 -and "$ok".Trim() -eq "1") { return @($exe) + $args_ }
        } catch { }
    }
}

$Py = @(Find-Python)
if ($Py.Count -eq 0) {
    Say "Python 3.10-3.13 not found. Installing Python 3.12..." "Cyan"
    if (-not (Has-Winget)) {
        Start-Process "https://www.python.org/downloads/release/python-3129/"
        Fail "winget is not available. Install Python 3.12 from the page that just opened (tick 'Add python.exe to PATH'), then run this again."
    }
    winget install -e --id Python.Python.3.12 --scope user --accept-package-agreements --accept-source-agreements
    Refresh-Path
    $Py = @(Find-Python)
    if ($Py.Count -eq 0) { Fail "Python was installed but Windows has not picked it up yet. Close this window and double-click Start-ClipKontrast-Windows.bat again." }
}
$PyExe = $Py[0]; $PyArgs = @($Py | Select-Object -Skip 1)
Say ("Python: " + (& $PyExe @PyArgs --version)) "Gray"

# ---- ffmpeg (ClipKontrast also finds winget's install folder by itself, so no PATH refresh is needed)
$haveFfmpeg = [bool](Get-Command ffmpeg -ErrorAction SilentlyContinue) -or
    (Test-Path "$env:LOCALAPPDATA\Microsoft\WinGet\Links\ffmpeg.exe") -or
    [bool](Get-ChildItem "$env:LOCALAPPDATA\Microsoft\WinGet\Packages" -Filter "Gyan.FFmpeg*" -Directory -ErrorAction SilentlyContinue)
if (-not $haveFfmpeg) {
    Say "ffmpeg not found. Installing it..." "Cyan"
    if (Has-Winget) {
        winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements
        Refresh-Path
    } else {
        Say "winget is not available: ClipKontrast will show how to install ffmpeg in the dashboard." "Yellow"
    }
}

# ---- Private Python folder + packages (fast startup: skips pip if packages already work)
$Venv = Join-Path $Root ".venv"
$VPy = Join-Path $Venv "Scripts\python.exe"

$PackagesReady = $false
if (Test-Path $VPy) {
    try {
        $pkCheck = & $VPy -c "import fastapi, uvicorn, sqlalchemy, yt_dlp; print('OK')" 2>$null
        if ($LASTEXITCODE -eq 0 -and "$pkCheck".Trim() -eq "OK") {
            $PackagesReady = $true
        }
    } catch { }
}

if (-not $PackagesReady) {
    # Check if pip works inside .venv; if damaged (e.g. missing pip._vendor.pyparsing), recreate cleanly
    $PipHealthy = $false
    if (Test-Path $VPy) {
        try {
            $testOut = & $VPy -c "import pip._vendor.pyparsing; print('ok')" 2>$null
            if ($LASTEXITCODE -eq 0 -and "$testOut".Trim() -eq "ok") {
                $PipHealthy = $true
            }
        } catch { }
    }

    if (-not $PipHealthy) {
        Say "Setting up fresh isolated Python environment for BlackClipping..." "Cyan"
        if (Test-Path $Venv) {
            Remove-Item -Path $Venv -Recurse -Force -ErrorAction SilentlyContinue
        }
        & $PyExe @PyArgs -m venv $Venv
        if ($LASTEXITCODE -ne 0) { Fail "Could not create Python environment. Please ensure Python 3.10-3.13 is installed." }
    }

    Say "Verifying packages (one time, quick)..." "Cyan"
    & $VPy -m pip install -r requirements.txt --disable-pip-version-check --no-warn-script-location
    if ($LASTEXITCODE -ne 0) {
        Say "Retrying package installation..." "Yellow"
        & $VPy -m pip install -r requirements.txt --no-cache-dir --disable-pip-version-check --no-warn-script-location
        if ($LASTEXITCODE -ne 0) {
            # Direct target install fallback
            $sitePkg = Join-Path $Venv "Lib\site-packages"
            & $PyExe @PyArgs -m pip install --target $sitePkg -r requirements.txt --no-cache-dir
            if ($LASTEXITCODE -ne 0) { Fail "Installing packages failed. Please check internet connection." }
        }
    }
}

# ---- Start
Write-Host ""
Say "Starting BlackClipping Studio..." "Green"
Say "Your browser opens automatically. Keep this window open while using BlackClipping." "Green"
Write-Host ""
$env:CLIPKONTRAST_OPEN_BROWSER = "1"
$env:PYTHONWARNINGS = "ignore::DeprecationWarning"

# ---- Already running? Then just open it. Port taken by another program? Then use the next free one.
function Port-Free($p) {
    if ($p -eq 9012 -or $p -eq 9013 -or $p -eq 8765) { return $false }
    try { $l = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $p); $l.Start(); $l.Stop(); return $true }
    catch { return $false }
}
function Is-BlackClipping($p) {
    if ($p -eq 9012 -or $p -eq 9013 -or $p -eq 8765) { return $false }
    try {
        $r = Invoke-RestMethod -TimeoutSec 2 -Uri "http://127.0.0.1:$p/api/status" -ErrorAction Stop
        return ($r -and $r.user -ne $null)
    } catch { return $false }
}

$Port = 8990
if ($env:BLACKCLIPPING_PORT) { $Port = [int]$env:BLACKCLIPPING_PORT }
elseif ($env:CLIPKONTRAST_PORT) { $Port = [int]$env:CLIPKONTRAST_PORT }

# First check if an existing BlackClipping is already running on any nearby port
for ($p = 8990; $p -le 9005; $p++) {
    if (Is-BlackClipping $p) {
        Say "BlackClipping is already running on port $p. Opening in browser..." "Green"
        Start-Process "http://127.0.0.1:$p/app"
        exit 0
    }
}

# Find the next free port starting from 8990 (never touches 8765 or 9012-9013)
while (-not (Port-Free $Port)) {
    Say "Port $Port is used by another program, trying $($Port + 1)..." "Yellow"
    $Port++
    if ($Port -eq 9012 -or $Port -eq 9013) { $Port = 9014 }
    if ($Port -gt 9100) { Fail "No free port found between 8990 and 9100." }
}

$env:BLACKCLIPPING_PORT = "$Port"
$env:CLIPKONTRAST_PORT = "$Port"
& $VPy -m studio.server
