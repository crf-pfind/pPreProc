[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$')]
    [string]$Version,

    [Parameter(Mandatory = $true)]
    [string]$SourceBin,

    [Parameter(Mandatory = $true)]
    [string]$VCRuntimeDirectory,

    [switch]$AcknowledgeRedistributionRights,

    [string]$OutputDirectory = (Join-Path $PSScriptRoot '..\build')
)

$ErrorActionPreference = 'Stop'
$repository = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$distribution = Join-Path $repository 'distribution\windows'
$source = (Resolve-Path -LiteralPath $SourceBin).Path
$vcRuntime = (Resolve-Path -LiteralPath $VCRuntimeDirectory).Path
$outputRoot = [System.IO.Path]::GetFullPath($OutputDirectory)
$expectedOutputRoot = [System.IO.Path]::GetFullPath((Join-Path $repository 'build'))
$expectedOutputPrefix = $expectedOutputRoot.TrimEnd('\') + '\'

if ($outputRoot -ne $expectedOutputRoot -and
    -not $outputRoot.StartsWith($expectedOutputPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "OutputDirectory must be inside $expectedOutputRoot"
}

if (-not $AcknowledgeRedistributionRights) {
    throw @'
Binary packaging is disabled until the project owner has reviewed and
acknowledged redistribution rights for every application and runtime file.
'@
}

$applicationLicense = Join-Path $distribution 'APPLICATION_LICENSE.txt'
$runtimeProvenance = Join-Path $distribution 'runtime-provenance.json'
$thirdPartyRoot = Join-Path $distribution 'third-party'
$thirdPartyNotices = Join-Path $thirdPartyRoot 'THIRD_PARTY_NOTICES.txt'
$thirdPartyComponents = Join-Path $thirdPartyRoot 'third-party-components.json'
$thirdPartyLicenses = Join-Path $thirdPartyRoot 'licenses'
foreach ($requiredEvidence in @($applicationLicense, $runtimeProvenance, $thirdPartyNotices, $thirdPartyComponents, $thirdPartyLicenses)) {
    if (-not (Test-Path -LiteralPath $requiredEvidence)) {
        throw "Release evidence is incomplete: $requiredEvidence"
    }
}
if (-not (Get-ChildItem -LiteralPath $thirdPartyLicenses -Recurse -File | Select-Object -First 1)) {
    throw "No matching third-party license texts were found in $thirdPartyLicenses"
}

$manifestPath = Join-Path $distribution 'runtime-manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
$stage = Join-Path $outputRoot "pPreProc-$Version-windows-x64"

if (Test-Path -LiteralPath $stage) {
    $resolvedStage = (Resolve-Path -LiteralPath $stage).Path
    if (-not $resolvedStage.StartsWith($expectedOutputPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to replace stage outside $expectedOutputRoot"
    }
    Remove-Item -LiteralPath $resolvedStage -Recurse -Force
}

New-Item -ItemType Directory -Path (Join-Path $stage 'bin') -Force | Out-Null
foreach ($entry in $manifest.entries) {
    $relative = $entry.path -replace '/', '\'
    $sourceRoot = if ($entry.source_root -eq 'microsoft_vc') { $vcRuntime } else { $source }
    $sourceRelative = if ($entry.source_path) { $entry.source_path -replace '/', '\' } else { $relative }
    $sourcePath = Join-Path $sourceRoot $sourceRelative
    if (-not (Test-Path -LiteralPath $sourcePath)) {
        if ($entry.required) { throw "Required runtime entry missing: $relative" }
        Write-Warning "Optional runtime entry missing: $relative"
        continue
    }
    $destination = Join-Path (Join-Path $stage 'bin') $relative
    New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
    if ($entry.recursive) {
        Copy-Item -LiteralPath $sourcePath -Destination $destination -Recurse
    } else {
        Copy-Item -LiteralPath $sourcePath -Destination $destination
    }
}

Copy-Item -LiteralPath (Join-Path $distribution 'ppreproc.cmd') -Destination (Join-Path $stage 'pPreProc.cmd')
Copy-Item -LiteralPath (Join-Path $distribution 'PACKAGE_README.txt') -Destination (Join-Path $stage 'README.txt')
Copy-Item -LiteralPath $applicationLicense -Destination (Join-Path $stage 'LICENSE.txt')

$noticeOutput = Join-Path $stage 'THIRD_PARTY_NOTICES.txt'
$noticeParts = @(
    $thirdPartyNotices,
    (Join-Path $thirdPartyLicenses 'Open-Source-Attributions.txt'),
    (Join-Path $thirdPartyLicenses 'Apache-2.0.txt'),
    (Join-Path $thirdPartyLicenses 'BSD-3-Clause.txt'),
    (Join-Path $thirdPartyLicenses 'Microsoft-Public-License.txt'),
    (Join-Path $thirdPartyLicenses 'MIT.txt'),
    (Join-Path $thirdPartyLicenses 'PSF-2.0.txt'),
    (Join-Path $thirdPartyLicenses 'SQLite-Public-Domain.txt'),
    (Join-Path $thirdPartyLicenses 'Zlib.txt')
)
$noticeSections = foreach ($part in $noticeParts) {
    if (-not (Test-Path -LiteralPath $part -PathType Leaf)) {
        throw "Required notice file is missing: $part"
    }
    $label = [System.IO.Path]::GetFileNameWithoutExtension($part)
    "`r`n===== $label =====`r`n`r`n$((Get-Content -LiteralPath $part -Raw).Trim())"
}
($noticeSections -join "`r`n") + "`r`n" |
    Set-Content -LiteralPath $noticeOutput -Encoding utf8

$archive = Join-Path $outputRoot "pPreProc-$Version-windows-x64.zip"
$archiveChecksum = "$archive.sha256"
if (Test-Path -LiteralPath $archive) {
    Remove-Item -LiteralPath $archive -Force
}
if (Test-Path -LiteralPath $archiveChecksum) {
    Remove-Item -LiteralPath $archiveChecksum -Force
}
Compress-Archive -LiteralPath $stage -DestinationPath $archive -CompressionLevel Optimal
$archiveHash = Get-FileHash -Algorithm SHA256 -LiteralPath $archive
"$($archiveHash.Hash.ToLowerInvariant())  $([System.IO.Path]::GetFileName($archive))" |
    Set-Content -LiteralPath $archiveChecksum -Encoding ascii
$archiveHash | Format-List Algorithm, Hash, Path
Write-Output "Checksum: $archiveChecksum"
