# PowerShell deployment script for Windows

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Deploying Disaster Truth Platform to Sui" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Check if Sui CLI is installed
if (-not (Get-Command sui -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Sui CLI not found. Please install it first." -ForegroundColor Red
    Write-Host "Visit: https://docs.sui.io/build/install" -ForegroundColor Yellow
    exit 1
}

# Build the package
Write-Host "Building Move package..." -ForegroundColor Yellow
sui move build

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

# Publish to network
Write-Host "Publishing package..." -ForegroundColor Yellow
sui client publish --gas-budget 100000000

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Save the following object IDs for later use:" -ForegroundColor Yellow
Write-Host "1. Package ID"
Write-Host "2. TreasuryCap object ID (for TRUTH_TOKEN)"
Write-Host "3. ReportRegistry object ID"
Write-Host ""
Write-Host "You can find these in the transaction output above."
