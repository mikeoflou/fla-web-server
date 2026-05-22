[CmdletBinding()]
param(
    [string]$Server = '129.121.84.30',
    [string]$User,
    [string]$RemoteDir = '/var/www/web_server',
    [switch]$IncludeUploads,
    [switch]$IncludeContentData
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if (-not $User) {
    $User = Read-Host 'Enter your Bluehost VPS SSH username'
}

if ([string]::IsNullOrWhiteSpace($User)) {
    throw 'A VPS SSH username is required.'
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)
$packageScript = Join-Path $scriptDir 'package_for_vps.ps1'

foreach ($commandName in @('ssh', 'scp')) {
    if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
        throw "Required command '$commandName' was not found. Install OpenSSH client on Windows first."
    }
}

if (-not (Test-Path $packageScript)) {
    throw "Package script not found: $packageScript"
}

Push-Location $projectRoot
try {
    Write-Host "Creating deploy package from $projectRoot ..." -ForegroundColor Cyan

    $packageArgs = @('-ExecutionPolicy', 'Bypass', '-File', $packageScript)

    if ($IncludeUploads) {
        Write-Host 'Full deploy mode: including gallery/event upload folders.' -ForegroundColor Yellow
        $packageArgs += '-IncludeUploads'
    }
    else {
        Write-Host 'Fast deploy mode: skipping gallery/event upload folders for a much smaller upload.' -ForegroundColor Cyan
    }

    if ($IncludeContentData) {
        Write-Host 'Content sync mode: this will replace live editable JSON data with the files from this PC.' -ForegroundColor Yellow
        $packageArgs += '-IncludeContentData'
    }
    else {
        Write-Host 'Protecting live editable content: JSON data files will stay on the server during this deploy.' -ForegroundColor Cyan
    }

    & powershell @packageArgs

    $package = Get-ChildItem -Path $projectRoot -Filter 'web_server_vps_*.zip' |
        Sort-Object LastWriteTime -Descending |
        Select-Object -First 1

    if (-not $package) {
        throw 'No deploy package was created.'
    }

    $target = "$User@$Server"
    $remoteZip = "/tmp/$($package.Name)"
    $sshOptions = @(
        '-o', 'ServerAliveInterval=15',
        '-o', 'ServerAliveCountMax=4',
        '-o', 'StrictHostKeyChecking=accept-new'
    )

    Write-Host "Uploading $($package.Name) to $target ..." -ForegroundColor Cyan
    & scp @sshOptions $package.FullName "${target}:$remoteZip"
    if ($LASTEXITCODE -ne 0) {
        throw 'SCP upload failed.'
    }

    $remoteCommand = (@"
set -euo pipefail
mkdir -p '$RemoteDir'
status=0
unzip -oq '$remoteZip' -d '$RemoteDir' || status=`$?
if [ "`$status" -gt 1 ]; then
  exit "`$status"
fi
rm -f '$remoteZip'
cd '$RemoteDir'
if [ -f deploy/vps/deploy_update.sh ]; then
  sed -i 's/\r$//' deploy/vps/deploy_update.sh
fi
bash deploy/vps/deploy_update.sh
"@ -replace "`r", "").Trim()

    $remoteCommandBase64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($remoteCommand))

    Write-Host 'Running remote update script on the VPS ...' -ForegroundColor Cyan
    Write-Host 'If prompted, accept the SSH host key and enter your VPS password.' -ForegroundColor DarkYellow
    & ssh '-tt' @sshOptions $target "printf '%s' '$remoteCommandBase64' | base64 -d | bash"
    if ($LASTEXITCODE -ne 0) {
        throw 'Remote deploy command failed.'
    }

    Write-Host ''
    Write-Host 'Deployment finished successfully.' -ForegroundColor Green
    Write-Host 'Open https://ehbcnewsletterjeff.org to verify the update.' -ForegroundColor Green
}
finally {
    Pop-Location
}
