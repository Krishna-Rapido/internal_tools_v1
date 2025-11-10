# 🚀 COMPLETE DEPLOYMENT GUIDE - START HERE

## ⚠️ Important: GitHub Pages + Python Backend

**GitHub Pages CANNOT run Python servers.** You have two parts:
1. **Frontend** (React) → GitHub Pages ✅
2. **Backend** (Python/FastAPI) → Separate hosting ⚡

---

## 🎯 EASIEST PATH: Render.com (All-in-One)

### Why Render?
- ✅ Hosts both frontend AND backend
- ✅ Free tier
- ✅ Auto-deploys from GitHub
- ✅ Zero config needed
- ✅ 5-minute setup

---

## 📋 Step-by-Step: Deploy Everything to Render

### 1. Create Render Account
1. Go to: **https://render.com**
2. Click **"Get Started"**
3. Sign up with GitHub

### 2. Deploy Backend (Python)
1. Click **"New +"** → **"Web Service"**
2. Connect repository: `Krishna-Rapido/internal_tools_v1`
3. Configure:
   ```
   Name: internal-tools-backend
   Region: Singapore (closest to you)
   Branch: main (or v3)
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   Instance Type: Free
   ```
4. Click **"Create Web Service"**
5. Wait 5-10 minutes
6. **Copy the URL** (e.g., `https://internal-tools-backend.onrender.com`)

### 3. Deploy Frontend (React)
1. Click **"New +"** → **"Static Site"**
2. Connect same repository: `Krishna-Rapido/internal_tools_v1`
3. Configure:
   ```
   Name: internal-tools-frontend
   Branch: main (or v3)
   Root Directory: frontend
   Build Command: npm install && npm run build
   Publish Directory: frontend/dist
   ```
4. Add Environment Variable:
   ```
   Key: VITE_API_BASE_URL
   Value: https://internal-tools-backend.onrender.com
   ```
5. Click **"Create Static Site"**
6. Wait 3-5 minutes
7. **Your app is live!** (e.g., `https://internal-tools-frontend.onrender.app`)

### 4. Update Backend CORS
Update `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://internal-tools-frontend.onrender.app",  # Add your Render frontend URL
        "https://krishna-rapido.github.io",
        "http://localhost:5173",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push - Render will auto-redeploy!

---

## 🎉 You're Done!

✅ **Frontend**: https://internal-tools-frontend.onrender.app  
✅ **Backend**: https://internal-tools-backend.onrender.com  
✅ **Auto-deploys**: Every git push rebuilds both!

---

## 🔄 Alternative: Still Want GitHub Pages?

You can use GitHub Pages for frontend + Render for backend:

### 1. Deploy Backend to Render (same as above)

### 2. Update Frontend Environment
```bash
cd frontend
cat > .env.production << 'EOF'
VITE_API_BASE_URL=https://internal-tools-backend.onrender.com
EOF
```

### 3. Build and Deploy to GitHub Pages
```bash
git add .
git commit -m "Add production backend URL"
git push

# Wait for GitHub Actions to complete
# Then visit: https://krishna-rapido.github.io/internal_tools_v1/
```

---

## 💡 Quick Decision Guide

**Choose Render (Both Services)** if:
- ✅ You want the simplest setup
- ✅ You want auto-deploy from GitHub
- ✅ You're okay with one URL

**Choose GitHub Pages (Frontend) + Render (Backend)** if:
- ✅ You specifically want GitHub Pages
- ✅ You don't mind managing two deployments
- ✅ You want krishna-rapido.github.io URL

---

## 🐛 Common Issues

### Backend URL Not Working
**Check**:
1. Render backend is deployed and running (green status)
2. Visit `https://your-backend.onrender.com/health` - should return `{"status":"ok"}`
3. Frontend `.env.production` has correct backend URL
4. CORS is configured correctly

### Frontend Can't Connect to Backend
**Solution**:
1. Check browser console for CORS errors
2. Update CORS in `backend/main.py` to include frontend URL
3. Restart backend (Render auto-restarts on push)

### "Module Not Found" on Backend
**Solution**:
1. Make sure `requirements.txt` is complete
2. Render build logs will show which package is missing
3. Add to `requirements.txt` and push

---

## 📝 Files Already Created for You

✅ `backend/Procfile` - For Heroku/Railway  
✅ `backend/railway.json` - For Railway.app  
✅ `backend/render.yaml` - For Render.com  
✅ `.github/workflows/deploy.yml` - For GitHub Pages  
✅ `.gitignore` - Ignore unnecessary files  

---

## 🚀 RECOMMENDED STEPS (5 minutes):

```bash
# 1. Commit everything
cd /Users/krishna.poddar/Desktop/Rapido\ EDA/GIG/internal_tools_v1
git add .
git commit -m "Prepare for deployment"
git push

# 2. Go to Render.com
# - Deploy backend as Web Service
# - Copy backend URL

# 3. Update frontend
cd frontend
echo "VITE_API_BASE_URL=https://your-backend.onrender.com" > .env.production

# 4. Push again
cd ..
git add .
git commit -m "Add production backend URL"
git push

# 5. Deploy frontend on Render as Static Site
# OR use GitHub Pages (already configured)
```

---

**Need help?** Check:
- `BACKEND_DEPLOYMENT.md` - Detailed backend hosting guide
- `DEPLOYMENT_GUIDE.md` - Complete deployment reference
- `DEPLOY_NOW.md` - GitHub Pages specific guide

**Stuck?** The fastest path is Render.com for both services. Takes 5 minutes total.

