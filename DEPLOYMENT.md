# Deployment  
## Yeshua X Bot · Tremayne Timms

This project can be deployed to various platforms. Use the guides below.

## Quick links

- **[DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md)** – Overview and Fly.io quick deploy
- **[DEPLOY_NOW.md](DEPLOY_NOW.md)** – Short Fly.io quick start
- **[FLY_DEPLOYMENT.md](FLY_DEPLOYMENT.md)** – Detailed Fly.io deployment guide

## Options

- **Fly.io** – `fly deploy` (see `fly.toml` and the guides above)
- **Railway** – `railway up` (see `railway.json`)
- **Render** – Connect repo and set env vars (see `render.yaml`)
- **Docker** – `docker build -t yeshua-x-bot .` then run with `--env-file .env`

Set all required environment variables (see [.env.example](.env.example)) as secrets or env vars on your platform.
