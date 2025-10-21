# Yeshua X Bot - Fly.io Deployment Script (PowerShell)
# Run this to deploy your bot to the cloud

$ErrorActionPreference = "Stop"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Yeshua X Bot - Fly.io Deployment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if fly CLI is installed
$flyCmd = Get-Command fly -ErrorAction SilentlyContinue
if (-not $flyCmd) {
    Write-Host "❌ Fly CLI not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install it first:"
    Write-Host "  iwr https://fly.io/install.ps1 -useb | iex"
    exit 1
}

Write-Host "✅ Fly CLI found" -ForegroundColor Green
Write-Host ""

# Check if logged in
try {
    fly auth whoami | Out-Null
    Write-Host "✅ Logged in to Fly.io" -ForegroundColor Green
} catch {
    Write-Host "❌ Not logged in to Fly.io" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please run: fly auth login"
    exit 1
}

Write-Host ""

# Check if secrets are set
Write-Host "Checking required secrets..."
$requiredSecrets = @(
    "TWITTER_API_KEY",
    "TWITTER_API_SECRET",
    "TWITTER_ACCESS_TOKEN",
    "TWITTER_ACCESS_TOKEN_SECRET",
    "TWITTER_BEARER_TOKEN",
    "NEWS_API_KEY",
    "GROQ_API_KEY"
)

$missingSecrets = @()
$secretsList = fly secrets list 2>$null | Out-String

foreach ($secret in $requiredSecrets) {
    if ($secretsList -notmatch $secret) {
        $missingSecrets += $secret
    }
}

if ($missingSecrets.Count -gt 0) {
    Write-Host "❌ Missing secrets:" -ForegroundColor Red
    foreach ($secret in $missingSecrets) {
        Write-Host "  - $secret"
    }
    Write-Host ""
    Write-Host "Set them with:"
    Write-Host "  fly secrets set TWITTER_API_KEY=`"your_key`""
    Write-Host ""
    $response = Read-Host "Do you want to continue anyway? (y/n)"
    if ($response -ne "y") {
        exit 1
    }
} else {
    Write-Host "✅ All secrets configured" -ForegroundColor Green
    Write-Host ""
}

# Deploy
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Deploying to Fly.io..." -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

fly deploy --ha=false

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Deployment Complete! ✅" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your bot is now running in the cloud!" -ForegroundColor Green
Write-Host ""
Write-Host "Useful commands:"
Write-Host "  fly status          - Check if bot is running"
Write-Host "  fly logs            - View real-time logs"
Write-Host "  fly ssh console     - SSH into container"
Write-Host ""
Write-Host "The bot will start posting tomorrow at:"
Write-Host "  - 7:00 AM Texas time (Bible Verse)"
Write-Host "  - 8:00 AM Texas time (US Markets)"
Write-Host "  - 9:00 AM Texas time (AI News)"
Write-Host "  - 7:00 AM Beijing time (圣经经文)"
Write-Host "  - 8:00 AM Beijing time (中国市场)"
Write-Host "  - 9:00 AM Beijing time (AI突破)"
Write-Host ""
Write-Host "Total: 15 tweets/day = 450 tweets/month"
Write-Host ""

