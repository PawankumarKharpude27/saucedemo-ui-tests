# Windows equivalent of run_tests.sh
#   .\run_tests.ps1 -Marker smoke -Browser firefox
param(
    [string]$Browser = $(if ($env:BROWSER) { $env:BROWSER } else { "chromium" }),
    [string]$Workers = $(if ($env:WORKERS) { $env:WORKERS } else { "auto" }),
    [string]$Marker  = $env:MARKER,
    [string]$ReportDir = $(if ($env:REPORT_DIR) { $env:REPORT_DIR } else { "reports" }),
    [Parameter(ValueFromRemainingArguments = $true)] $Extra
)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force -Path $ReportDir, "test-results" | Out-Null

$pytestArgs = @(
    "--browser", $Browser, "-n", $Workers,
    "--output", "test-results/$Browser",
    "--junitxml=$ReportDir/junit-$Browser.xml",
    "--html=$ReportDir/report-$Browser.html", "--self-contained-html"
)
if ($Marker) { $pytestArgs += @("-m", $Marker) }
python -m pytest @pytestArgs @Extra
exit $LASTEXITCODE
