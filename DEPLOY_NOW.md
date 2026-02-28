# 🚀 Deploy Your Bot NOW — Quick Start  
## Yeshua X Bot · Tremayne Timms

### **Step 1: Install Fly CLI**

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Mac/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

Close and reopen PowerShell/Terminal after install.

---

### **Step 2: Login to Fly.io**

```bash
fly auth login
```

This will open a browser. Sign up (free) or login.

---

### **Step 3: Set Your API Keys**

```bash
fly secrets set TWITTER_API_KEY="your_key_here"
fly secrets set TWITTER_API_SECRET="your_secret_here"
fly secrets set TWITTER_ACCESS_TOKEN="your_token_here"
fly secrets set TWITTER_ACCESS_TOKEN_SECRET="your_token_secret_here"
fly secrets set TWITTER_BEARER_TOKEN="your_bearer_token_here"
fly secrets set NEWS_API_KEY="your_newsapi_key_here"
fly secrets set GROQ_API_KEY="your_groq_key_here"
```

**⚠️ Important:** Replace `"your_key_here"` with your actual keys!

---

### **Step 4: Deploy! 🚀**

**Windows (PowerShell):**
```powershell
.\deploy.ps1
```

**Mac/Linux:**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Or manually:**
```bash
fly deploy --ha=false
```

---

## ✅ **That's It!**

Your bot is now running in the cloud and will start posting tomorrow at:

### **Texas Time (Central)**
- **7:00 AM** - Bible Verse (English)
- **8:00 AM** - US Markets
- **9:00 AM** - AI Breakthroughs

### **Beijing Time**
- **7:00 AM** - 圣经经文 (Chinese)
- **8:00 AM** - 中国市场
- **9:00 AM** - AI突破

**Total: 15 tweets/day**

---

## 📊 **Monitor Your Bot**

```bash
# Check if running
fly status

# Watch live logs
fly logs

# View schedule
fly logs | grep "Scheduled"
```

---

## 🛠️ **Useful Commands**

```bash
# Restart bot
fly apps restart yeshua-x-bot

# Stop bot (pause)
fly scale count 0

# Resume bot
fly scale count 1

# Update secrets
fly secrets set TWITTER_API_KEY="new_key"

# SSH into bot
fly ssh console

# Redeploy after changes
fly deploy
```

---

## 💰 **Cost**

- **~$2-3/month** (Fly.io gives $5/month free credit)
- Essentially **FREE** for the first few months!

---

## ❓ **Troubleshooting**

**Bot not posting?**
```bash
# Check logs
fly logs

# Verify secrets
fly secrets list

# Check status
fly status
```

**Need help?**
- See `FLY_DEPLOYMENT.md` for detailed guide
- Check logs: `fly logs`

---

## 🎉 **You're Live!**

Your bot is now in the cloud, will never stop, and will post automatically every day!

Monitor it: `fly logs`

Happy posting! 🙏

