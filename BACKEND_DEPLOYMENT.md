# 🐍 Python Backend Deployment Guide

## Problem: GitHub Pages Can't Run Python

GitHub Pages only hosts static HTML/JS/CSS. For your Python backend (`python main.py`), you need a separate hosting service.

---

## ✅ Solution 1: Render.com (Easiest - Free Tier)

### Step 1: Create Render Account
1. Go to: https://render.com
2. Sign up with GitHub (free)

### Step 2: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `Krishna-Rapido/internal_tools_v1`
3. Configure:
   - **Name**: `internal-tools-backend`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or `v3`)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Instance Type**: `Free`

### Step 3: Set Environment Variables (if needed)
- Click "Environment" tab
- Add any secrets/config

### Step 4: Deploy
- Click **"Create Web Service"**
- Wait 5-10 minutes for first deployment
- You'll get a URL like: `https://internal-tools-backend.onrender.com`

### Step 5: Update Frontend
```bash
cd frontend
cat > .env.production << 'EOF'
VITE_API_BASE_URL=https://internal-tools-backend.onrender.com
EOF

git add .env.production
git commit -m "Add production backend URL"
git push
```

**⚠️ Note**: Free tier sleeps after 15 minutes of inactivity. First request after sleep takes 30-60 seconds.

---

## ✅ Solution 2: Railway.app (Good Free Tier)

### Step 1: Create Railway Account
1. Go to: https://railway.app
2. Sign up with GitHub

### Step 2: Deploy from GitHub
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose `Krishna-Rapido/internal_tools_v1`
4. Railway auto-detects Python

### Step 3: Configure
1. Go to project settings
2. **Root Directory**: Set to `backend`
3. **Start Command**: `python main.py`
4. **Install Command**: `pip install -r requirements.txt`

### Step 4: Deploy
- Railway automatically deploys
- You get a URL like: `https://internal-tools-production.up.railway.app`

### Step 5: Update Frontend
Same as Render (create `.env.production` with Railway URL)

---

## ✅ Solution 3: Fly.io (More Control)

### Step 1: Install Fly CLI
```bash
brew install flyctl
# OR
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login and Create App
```bash
cd backend
fly auth login
fly launch

# Answer prompts:
# App name: internal-tools-backend
# Region: Choose closest
# Database: No
# Deploy now: Yes
```

### Step 3: Configure (if needed)
Fly creates `fly.toml` automatically. Update if needed:

```toml
app = "internal-tools-backend"

[build]
  builder = "paketobuildpacks/builder:base"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true

[[vm]]
  memory = '256mb'
  cpu_kind = 'shared'
  cpus = 1
```

### Step 4: Deploy
```bash
fly deploy
```

You get: `https://internal-tools-backend.fly.dev`

---

## ✅ Solution 4: PythonAnywhere (Python Specific)

### Step 1: Create Account
1. Go to: https://www.pythonanywhere.com
2. Sign up (free tier: Beginner account)

### Step 2: Upload Code
1. Open **"Files"** tab
2. Upload your `backend` folder
3. Or clone from GitHub:
   ```bash
   git clone https://github.com/Krishna-Rapido/internal_tools_v1.git
   cd internal_tools_v1/backend
   pip install -r requirements.txt
   ```

### Step 3: Configure Web App
1. Go to **"Web"** tab
2. **Add a new web app**
3. Choose **"Manual configuration"**
4. Python version: **3.10+**
5. Configure WSGI file to point to your FastAPI app

### Step 4: Get URL
You get: `https://your-username.pythonanywhere.com`

---

## 🎯 Recommended: Render.com (Simplest)

### Why Render?
- ✅ Free tier
- ✅ Auto-deploys from GitHub
- ✅ Zero configuration
- ✅ HTTPS included
- ✅ Easy environment variables
- ⚠️ Sleeps after 15min inactivity (30-60s wake time)

---

## 🔧 Quick Setup: Render + GitHub Pages

### 1. Deploy Backend to Render (5 minutes)
```
1. Go to render.com → New Web Service
2. Connect GitHub repo
3. Root: backend
4. Start: python main.py
5. Deploy
6. Copy URL: https://your-app.onrender.com
```

### 2. Update Frontend (1 minute)
```bash
cd frontend
echo "VITE_API_BASE_URL=https://your-app.onrender.com" > .env.production
```

### 3. Deploy Frontend to GitHub Pages (already configured!)
```bash
git add .
git commit -m "Add production backend URL"
git push  # GitHub Actions will deploy
```

### 4. Done!
- Frontend: https://krishna-rapido.github.io/internal_tools_v1/
- Backend: https://your-app.onrender.com

---

## 🚨 Update CORS in Backend

After deploying backend, update `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://krishna-rapido.github.io",  # Add this
        "http://localhost:5173",
        "*"  # Or keep "*" for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Final Architecture

```
User Browser
    ↓
Frontend (GitHub Pages)
https://krishna-rapido.github.io/internal_tools_v1/
    ↓
Backend (Render/Railway/Fly)
https://your-backend.onrender.com
    ↓
Presto Database (Rapido Internal)
```

---

## 🎉 Next Steps

1. **Choose a backend host** (Render recommended)
2. **Deploy backend** (5 minutes)
3. **Update `.env.production`** with backend URL
4. **Push to GitHub** (frontend auto-deploys)
5. **Visit your app!**

Need help? See detailed guides for each platform in `DEPLOYMENT_GUIDE.md`

