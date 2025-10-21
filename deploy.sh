#!/bin/bash

# Yeshua X Bot - Fly.io Deployment Script
# Run this to deploy your bot to the cloud

set -e  # Exit on error

echo "=========================================="
echo "  Yeshua X Bot - Fly.io Deployment"
echo "=========================================="
echo ""

# Check if fly CLI is installed
if ! command -v fly &> /dev/null; then
    echo "❌ Fly CLI not found!"
    echo ""
    echo "Install it first:"
    echo "  Windows: iwr https://fly.io/install.ps1 -useb | iex"
    echo "  Mac/Linux: curl -L https://fly.io/install.sh | sh"
    exit 1
fi

echo "✅ Fly CLI found"
echo ""

# Check if logged in
if ! fly auth whoami &> /dev/null; then
    echo "❌ Not logged in to Fly.io"
    echo ""
    echo "Please run: fly auth login"
    exit 1
fi

echo "✅ Logged in to Fly.io"
echo ""

# Check if secrets are set
echo "Checking required secrets..."
REQUIRED_SECRETS=(
    "TWITTER_API_KEY"
    "TWITTER_API_SECRET"
    "TWITTER_ACCESS_TOKEN"
    "TWITTER_ACCESS_TOKEN_SECRET"
    "TWITTER_BEARER_TOKEN"
    "NEWS_API_KEY"
    "GROQ_API_KEY"
)

MISSING_SECRETS=()

for secret in "${REQUIRED_SECRETS[@]}"; do
    if ! fly secrets list 2>/dev/null | grep -q "$secret"; then
        MISSING_SECRETS+=("$secret")
    fi
done

if [ ${#MISSING_SECRETS[@]} -ne 0 ]; then
    echo "❌ Missing secrets:"
    for secret in "${MISSING_SECRETS[@]}"; do
        echo "  - $secret"
    done
    echo ""
    echo "Set them with:"
    echo "  fly secrets set TWITTER_API_KEY=\"your_key\""
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ All secrets configured"
    echo ""
fi

# Deploy
echo "=========================================="
echo "  Deploying to Fly.io..."
echo "=========================================="
echo ""

fly deploy --ha=false

echo ""
echo "=========================================="
echo "  Deployment Complete! ✅"
echo "=========================================="
echo ""
echo "Your bot is now running in the cloud!"
echo ""
echo "Useful commands:"
echo "  fly status          - Check if bot is running"
echo "  fly logs            - View real-time logs"
echo "  fly ssh console     - SSH into container"
echo ""
echo "The bot will start posting tomorrow at:"
echo "  - 7:00 AM Texas time (Bible Verse)"
echo "  - 8:00 AM Texas time (US Markets)"
echo "  - 9:00 AM Texas time (AI News)"
echo "  - 7:00 AM Beijing time (圣经经文)"
echo "  - 8:00 AM Beijing time (中国市场)"
echo "  - 9:00 AM Beijing time (AI突破)"
echo ""
echo "Total: 15 tweets/day = 450 tweets/month"
echo ""

