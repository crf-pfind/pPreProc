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

New-Item -ItemType Directory -Path (Join-Path $stage 'runtime') -Force | Out-Null
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
    $destination = Join-Path (Join-Path $stage 'runtime') $relative
    New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force | Out-Null
    if ($entry.recursive) {
        Copy-Item -LiteralPath $sourcePath -Destination $destination -Recurse
    } else {
        Copy-Item -LiteralPath $sourcePath -Destination $destination
    }
}

Copy-Item -LiteralPath (Join-Path $distribution 'ppreproc.ps1') -Destination $stage
Copy-Item -LiteralPath (Join-Path $distribution 'ppreproc.cmd') -Destination $stage
Copy-Item -LiteralPath (Join-Path $distribution 'PACKAGE_README.md') -Destination (Join-Path $stage 'README.md')
$citation = Get-Content -LiteralPath (Join-Path $repository 'CITATION.cff') -Raw
$citation = $citation -replace '(?m)^version:.*$', "version: $Version"
$citation = $citation -replace '(?m)^date-released:.*$', "date-released: $([DateTime]::UtcNow.ToString('yyyy-MM-dd'))"
$citation = $citation -replace '(?m)^license:.*\r?\n', ''
Set-Content -LiteralPath (Join-Path $stage 'CITATION.cff') -Value $citation -Encoding utf8
Copy-Item -LiteralPath (Join-Path $repository 'LICENSE') -Destination (Join-Path $stage 'PUBLIC_COMPONENTS_LICENSE.txt')
Copy-Item -LiteralPath $applicationLicense -Destination $stage
Copy-Item -LiteralPath $thirdPartyNotices -Destination $stage
Copy-Item -LiteralPath $thirdPartyLicenses -Destination (Join-Path $stage 'third-party-licenses') -Recurse
Copy-Item -LiteralPath $manifestPath -Destination $stage
Copy-Item -LiteralPath $runtimeProvenance -Destination $stage
Copy-Item -LiteralPath $thirdPartyComponents -Destination $stage
Set-Content -LiteralPath (Join-Path $stage 'VERSION') -Value $Version -Encoding ascii

$inventory = foreach ($file in Get-ChildItem -LiteralPath (Join-Path $stage 'runtime') -Recurse -File | Sort-Object FullName) {
    $relative = $file.FullName.Substring((Join-Path $stage 'runtime').Length + 1).Replace('\', '/')
    [ordered]@{
        path = $relative
        size_bytes = $file.Length
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash.ToLowerInvariant()
        file_version = $file.VersionInfo.FileVersion
        product_version = $file.VersionInfo.ProductVersion
    }
}
[ordered]@{
    schema_version = 1
    application_version = $Version
    generated_utc = [DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ')
    repository_commit = (& git -C $repository rev-parse HEAD 2>$null)
    files = @($inventory)
} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $stage 'RUNTIME_INVENTORY.json') -Encoding utf8

$checksumPath = Join-Path $stage 'SHA256SUMS.txt'
$stagePrefix = $stage.TrimEnd('\') + '\'
Get-ChildItem -LiteralPath $stage -Recurse -File |
    Where-Object { $_.FullName -ne $checksumPath } |
    Sort-Object FullName |
    ForEach-Object {
        $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName).Hash.ToLowerInvariant()
        $relative = $_.FullName.Substring($stagePrefix.Length).Replace('\', '/')
        "$hash  $relative"
    } | Set-Content -LiteralPath $checksumPath -Encoding ascii

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
