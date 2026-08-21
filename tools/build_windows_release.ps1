[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SourceBin,

    [switch]$AcknowledgeRedistributionRights,

    [string]$OutputDirectory = (Join-Path $PSScriptRoot '..\build')
)

$ErrorActionPreference = 'Stop'
$repository = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$source = (Resolve-Path -LiteralPath $SourceBin).Path
$outputRoot = [System.IO.Path]::GetFullPath($OutputDirectory)
$versionPath = Join-Path $repository 'VERSION'
if (-not (Test-Path -LiteralPath $versionPath -PathType Leaf)) {
    throw "Release VERSION file not found: $versionPath"
}
$releaseVersion = (Get-Content -LiteralPath $versionPath -Raw).Trim()
if ([string]::IsNullOrWhiteSpace($releaseVersion)) {
    throw "Release VERSION file is empty: $versionPath"
}
$stage = Join-Path $outputRoot "pPreProc-v$releaseVersion-win-x64"
$manifestPath = Join-Path $repository 'runtime-manifest.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json

if (-not $AcknowledgeRedistributionRights) {
    throw @'
Binary packaging is disabled until the project owner has reviewed and
acknowledged redistribution rights for the pPreProc and third-party runtime
files. Re-run with -AcknowledgeRedistributionRights only after that review.
'@
}

$releaseLicense = Join-Path $repository 'LICENSE'
$thirdPartyNotices = Join-Path $repository 'third_party\THIRD_PARTY_NOTICES.txt'
$thirdPartyLicenses = Join-Path $repository 'third_party\licenses'
foreach ($requiredEvidence in @($releaseLicense, $thirdPartyNotices, $thirdPartyLicenses)) {
    if (-not (Test-Path -LiteralPath $requiredEvidence)) {
        throw "Release evidence is incomplete: $requiredEvidence"
    }
}
if (-not (Get-ChildItem -LiteralPath $thirdPartyLicenses -Recurse -File | Select-Object -First 1)) {
    throw "No matching third-party license texts were found in $thirdPartyLicenses"
}

$expectedStageRoot = [System.IO.Path]::GetFullPath((Join-Path $repository 'build'))
if (-not $outputRoot.StartsWith($expectedStageRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "OutputDirectory must be inside $expectedStageRoot"
}
if (Test-Path -LiteralPath $stage) {
    $resolvedStage = (Resolve-Path -LiteralPath $stage).Path
    if (-not $resolvedStage.StartsWith($expectedStageRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to replace stage outside $expectedStageRoot"
    }
    Remove-Item -LiteralPath $resolvedStage -Recurse -Force
}

New-Item -ItemType Directory -Path (Join-Path $stage 'runtime') -Force | Out-Null
foreach ($entry in $manifest.entries) {
    $relative = $entry.path -replace '/', '\'
    $sourcePath = Join-Path $source $relative
    if (-not (Test-Path -LiteralPath $sourcePath)) {
        if ($entry.required) { throw "Required runtime entry missing: $relative" }
        Write-Warning "Optional runtime entry missing: $relative"
        continue
    }
    $destination = Join-Path (Join-Path $stage 'runtime') $relative
    $destinationParent = Split-Path -Parent $destination
    New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
    if ($entry.recursive) {
        Copy-Item -LiteralPath $sourcePath -Destination $destination -Recurse
    } else {
        Copy-Item -LiteralPath $sourcePath -Destination $destination
    }
}

Copy-Item -LiteralPath (Join-Path $repository 'ppreproc.ps1') -Destination $stage
Copy-Item -LiteralPath (Join-Path $repository 'ppreproc.cmd') -Destination $stage
Copy-Item -LiteralPath (Join-Path $repository 'README.md') -Destination $stage
Copy-Item -LiteralPath (Join-Path $repository 'CITATION.cff') -Destination $stage
Copy-Item -LiteralPath $versionPath -Destination $stage
Copy-Item -LiteralPath $releaseLicense -Destination $stage
Copy-Item -LiteralPath $thirdPartyNotices -Destination $stage
Copy-Item -LiteralPath $thirdPartyLicenses -Destination (Join-Path $stage 'third_party-licenses') -Recurse
Copy-Item -LiteralPath (Join-Path $repository 'runtime-manifest.json') -Destination $stage
Copy-Item -LiteralPath (Join-Path $repository 'docs') -Destination $stage -Recurse
Copy-Item -LiteralPath (Join-Path $repository 'src') -Destination $stage -Recurse
Copy-Item -LiteralPath (Join-Path $repository 'cpp') -Destination $stage -Recurse

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

$archive = Join-Path $outputRoot "pPreProc-v$releaseVersion-win-x64.zip"
if (Test-Path -LiteralPath $archive) { Remove-Item -LiteralPath $archive -Force }
Compress-Archive -LiteralPath $stage -DestinationPath $archive -CompressionLevel Optimal
Get-FileHash -Algorithm SHA256 -LiteralPath $archive |
    Format-List Algorithm, Hash, Path
