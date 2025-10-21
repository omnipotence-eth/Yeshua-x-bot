# 🚀 Fly.io Deployment Guide
## Yeshua X Bot

---

## 📋 **Prerequisites**

1. **Fly.io Account**: Sign up at [fly.io](https://fly.io)
2. **Fly CLI Installed**: 
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Mac/Linux
   curl -L https://fly.io/install.sh | sh
   ```
3. **API Keys Ready**: X API, NewsAPI, Groq AI keys

---

## 🔑 **Step 1: Set Up Secrets**

Your bot needs these environment variables. **Never commit these to git!**

```bash
# Navigate to your bot directory
cd "C:\Users\ttimm\Desktop\Yeshua X Bot"

# Log in to Fly.io
fly auth login

# Set secrets (one by one)
fly secrets set TWITTER_API_KEY="your_twitter_api_key"
fly secrets set TWITTER_API_SECRET="your_twitter_api_secret"
fly secrets set TWITTER_ACCESS_TOKEN="your_access_token"
fly secrets set TWITTER_ACCESS_TOKEN_SECRET="your_access_token_secret"
fly secrets set TWITTER_BEARER_TOKEN="your_bearer_token"
fly secrets set NEWS_API_KEY="your_news_api_key"
fly secrets set GROQ_API_KEY="your_groq_api_key"
```

**Important:** Replace `"your_..."` with your actual keys!

---

## 📦 **Step 2: Deploy Your Bot**

### **Option A: Fresh Deployment (First Time)**

```bash
# Launch the app
fly launch --no-deploy

# It will ask:
# "Would you like to copy its configuration to the new app?" → Yes
# "App Name" → Press Enter (use yeshua-x-bot)
# "Choose a region" → Dallas (dfw) - closest to Texas
# "Would you like to set up a PostgreSQL database?" → No
# "Would you like to set up an Upstash Redis database?" → No

# Now deploy
fly deploy
```

### **Option B: Update Existing Deployment**

```bash
# Just deploy the latest changes
fly deploy
```

---

## 🎯 **Step 3: Verify Deployment**

```bash
# Check if bot is running
fly status

# View logs (to see scheduled posts)
fly logs

# Check current config
fly config show
```

**Expected Output:**
```
=== yeshua-x-bot
Status: running
Instances: 1
Region: dfw (Dallas)
```

---

## ⏰ **Step 4: Verify Schedule**

Your bot is now running on this schedule:

### **Texas Time (Central Time)**
- **7:00 AM** - Bible Verse (3-tweet thread)
- **8:00 AM** - US Markets (3-tweet thread)
- **9:00 AM** - AI News (3-tweet thread)

### **Beijing Time (China Standard Time)**
- **7:00 AM** - 圣经经文 (2-tweet thread)
- **8:00 AM** - 中国市场 (2-tweet thread)
- **9:00 AM** - AI突破 (2-tweet thread)

**Total: 15 tweets/day = 450 tweets/month** (within free tier!)

---

## 📊 **Monitoring Your Bot**

### **View Real-Time Logs:**
```bash
fly logs -a yeshua-x-bot
```

You'll see output like:
```
2025-10-21 07:00:01 [TEXAS] Posting Bible verse...
2025-10-21 07:00:03 Thread posted successfully (3 tweets)
2025-10-21 08:00:01 [TEXAS] Posting combined markets...
```

### **Check Bot Health:**
```bash
# See if it's running
fly status

# Restart if needed
fly apps restart yeshua-x-bot
```

### **SSH into Container (for debugging):**
```bash
fly ssh console
```

---

## 🛠️ **Common Commands**

```bash
# View current secrets (names only, not values)
fly secrets list

# Update a secret
fly secrets set TWITTER_API_KEY="new_key"

# Scale to 0 (pause bot without deleting)
fly scale count 0

# Scale back to 1 (resume bot)
fly scale count 1

# Stop and remove app (if you want to delete it)
fly apps destroy yeshua-x-bot
```

---

## 🔧 **Troubleshooting**

### **Bot Not Posting?**

1. **Check logs:**
   ```bash
   fly logs
   ```

2. **Verify secrets are set:**
   ```bash
   fly secrets list
   ```
   Should show: `TWITTER_API_KEY`, `TWITTER_API_SECRET`, etc.

3. **Check DRY_RUN mode:**
   ```bash
   fly config show
   ```
   Make sure `DRY_RUN = "false"`

### **Rate Limit Errors?**

- X Free Tier: 500 tweets/month
- Bot uses: 450 tweets/month
- Check you haven't exceeded limits

### **Missing Posts?**

- Check timezone settings in `config.py`
- Verify scheduler is running: `fly logs` should show scheduled jobs

---

## 💰 **Fly.io Costs**

**Your bot will use:**
- **Shared CPU**: ~$1.94/month (1 VM always running)
- **256MB RAM**: Free tier
- **Network**: Free (minimal usage)

**Total: ~$2-3/month** (Fly.io gives $5 free credit/month, so it's essentially free!)

---

## 🎉 **Deployment Checklist**

- [ ] Fly CLI installed
- [ ] Logged in to Fly.io (`fly auth login`)
- [ ] All secrets set (`fly secrets set ...`)
- [ ] Bot deployed (`fly deploy`)
- [ ] Status shows "running" (`fly status`)
- [ ] Logs show scheduler active (`fly logs`)
- [ ] First post scheduled for tomorrow 7 AM

---

## 📱 **Getting Notifications**

### **Set Up Fly.io Monitoring:**

```bash
# Add your email for alerts
fly auth whoami
```

Fly.io will email you if:
- App crashes
- Deployment fails
- Health checks fail

---

## 🚀 **You're Ready!**

Your bot is now running in the cloud and will start posting tomorrow morning at 7 AM Texas time!

**Monitor it with:**
```bash
fly logs -a yeshua-x-bot
```

**Need to update code?**
```bash
# Make changes locally
git add .
git commit -m "Update bot"

# Deploy to Fly.io
fly deploy
```

---

## 📞 **Support**

- **Fly.io Docs**: https://fly.io/docs
- **Fly.io Community**: https://community.fly.io
- **Your Bot Logs**: `fly logs`

Happy posting! 🙏

