[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [Alias('Input')]
    [string]$InputPath,

    [string]$Config,

    [string]$RuntimeDir = (Join-Path $PSScriptRoot 'runtime'),

    [switch]$DryRun,

    [switch]$Version
)

$ErrorActionPreference = 'Stop'
$versionPath = Join-Path $PSScriptRoot 'VERSION'
if (-not (Test-Path -LiteralPath $versionPath -PathType Leaf)) {
    throw "Release VERSION file not found: $versionPath"
}
$releaseVersion = (Get-Content -LiteralPath $versionPath -Raw).Trim()
if ([string]::IsNullOrWhiteSpace($releaseVersion)) {
    throw "Release VERSION file is empty: $versionPath"
}

if ($Version) {
    Write-Output "pPreProc $releaseVersion"
    exit 0
}

if ([string]::IsNullOrWhiteSpace($InputPath) -eq [string]::IsNullOrWhiteSpace($Config)) {
    throw 'Specify exactly one of -Input or -Config.'
}

$runtimeRoot = (Resolve-Path -LiteralPath $RuntimeDir -ErrorAction Stop).Path
$executable = Join-Path $runtimeRoot 'pParse2Plus\pParse2Plus.exe'
if (-not (Test-Path -LiteralPath $executable -PathType Leaf)) {
    throw "pParse2+ runtime not found: $executable"
}

$argument = if ($InputPath) {
    $resolved = Resolve-Path -LiteralPath $InputPath -ErrorAction Stop
    $resolved.Path
} else {
    $resolved = Resolve-Path -LiteralPath $Config -ErrorAction Stop
    $resolved.Path
}

$workingDirectory = Split-Path -Parent $executable
if ($DryRun) {
    [pscustomobject]@{
        Version          = $releaseVersion
        Executable       = $executable
        Argument         = $argument
        WorkingDirectory = $workingDirectory
    } | Format-List
    exit 0
}

Push-Location -LiteralPath $workingDirectory
try {
    & $executable $argument
    $exitCode = $LASTEXITCODE
} finally {
    Pop-Location
}
if ($null -eq $exitCode) { $exitCode = 0 }
exit $exitCode
