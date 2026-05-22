[CmdletBinding()]
param(
    [switch]$IncludeUploads,
    [switch]$IncludeContentData
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$outFile = "web_server_vps_$stamp.zip"

$includeRootNames = @(
    'app.py',
    'passenger_wsgi.py',
    'requirements.txt',
    'templates',
    'static',
    'deploy'
)

$includeRootPatterns = @(
)

$mutableContentFiles = @(
    'announcements_data.json',
    'custom_pages_data.json',
    'events_data.json',
    'gallery_data.json',
    'home_ministry_images.json',
    'prayer_requests_data.json',
    'sermons_data.json',
    'songs_data.json',
    'users_data.json',
    'volunteers_data.json',
    'worship_settings.json'
)

$excludeDirNames = @(
    'Lib',
    'Include',
    'Scripts',
    '.venv',
    'venv',
    '__pycache__',
    '.git',
    'var',
    '.dist',
    '.pytest_cache',
    '.mypy_cache'
)

$excludeFilePatterns = @(
    '*.zip',
    '.env',
    '*.log'
)

$excludeRelativePrefixes = @(
    'static/images/tmp/'
)

if (-not $IncludeUploads) {
    $excludeRelativePrefixes += @(
        'static/images/gallery/',
        'static/images/events/'
    )
}

function Get-RelativeZipPath {
    param(
        [string]$FullPath,
        [string]$RootPath
    )

    $normalizedFullPath = [System.IO.Path]::GetFullPath($FullPath)
    $normalizedRootPath = ([System.IO.Path]::GetFullPath($RootPath)).TrimEnd('\') + '\'

    if ($normalizedFullPath.StartsWith($normalizedRootPath, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $normalizedFullPath.Substring($normalizedRootPath.Length).Replace('\', '/')
    }

    return [System.IO.Path]::GetFileName($normalizedFullPath)
}

function Test-RootItemIncluded {
    param(
        [System.IO.FileSystemInfo]$Item
    )

    if ($excludeDirNames -contains $Item.Name) {
        return $false
    }

    if ((-not $IncludeContentData) -and ($mutableContentFiles -contains $Item.Name)) {
        return $false
    }

    if ($IncludeContentData -and ($mutableContentFiles -contains $Item.Name)) {
        return $true
    }

    if ($includeRootNames -contains $Item.Name) {
        return $true
    }

    foreach ($pattern in $includeRootPatterns) {
        if ($Item.Name -like $pattern) {
            return $true
        }
    }

    return $false
}

function Test-PathExcluded {
    param(
        [string]$FullPath,
        [string]$RootPath
    )

    $relativePath = Get-RelativeZipPath -FullPath $FullPath -RootPath $RootPath
    $fileName = [System.IO.Path]::GetFileName($relativePath)

    foreach ($pattern in $excludeFilePatterns) {
        if ($fileName -like $pattern) {
            return $true
        }
    }

    foreach ($prefix in $excludeRelativePrefixes) {
        if ($relativePath.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
            return $true
        }
    }

    $segments = $relativePath -split '/'
    if ($segments.Length -gt 1) {
        foreach ($segment in $segments[0..($segments.Length - 2)]) {
            if ($excludeDirNames -contains $segment) {
                return $true
            }
        }
    }

    return $false
}

$projectRoot = (Get-Location).Path
$items = Get-ChildItem -Force | Where-Object { Test-RootItemIncluded $_ }

if (Test-Path $outFile) {
    Remove-Item $outFile -Force
}

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$zipArchive = [System.IO.Compression.ZipFile]::Open($outFile, [System.IO.Compression.ZipArchiveMode]::Create)
$filesAdded = 0

try {
    foreach ($item in $items) {
        if ($item.PSIsContainer) {
            Get-ChildItem -Path $item.FullName -Recurse -Force -File | ForEach-Object {
                if (Test-PathExcluded -FullPath $_.FullName -RootPath $projectRoot) {
                    return
                }

                $relativePath = Get-RelativeZipPath -FullPath $_.FullName -RootPath $projectRoot
                [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                    $zipArchive,
                    $_.FullName,
                    $relativePath,
                    [System.IO.Compression.CompressionLevel]::Optimal
                ) | Out-Null
                $filesAdded++
            }
        }
        else {
            if (Test-PathExcluded -FullPath $item.FullName -RootPath $projectRoot) {
                continue
            }

            $relativePath = Get-RelativeZipPath -FullPath $item.FullName -RootPath $projectRoot
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                $zipArchive,
                $item.FullName,
                $relativePath,
                [System.IO.Compression.CompressionLevel]::Optimal
            ) | Out-Null
            $filesAdded++
        }
    }
}
finally {
    $zipArchive.Dispose()
}

Write-Host "Created package: $outFile"
Write-Host "Files packed: $filesAdded"

if ($IncludeUploads) {
    Write-Host 'Included gallery/event upload folders for a full media sync.' -ForegroundColor Yellow
}
else {
    Write-Host 'Fast deploy mode: skipped gallery/event upload folders to keep VPS uploads quick.' -ForegroundColor Cyan
}

if ($IncludeContentData) {
    Write-Host 'Included editable JSON content files and settings from this PC.' -ForegroundColor Yellow
}
else {
    Write-Host 'Preserving live JSON content data on the server by excluding editable data files from this package.' -ForegroundColor Cyan
}
