# 🚀 Render.com Deployment - RECOMMENDED

## ✅ Deploy Both Frontend and Backend to Render

Render is the easiest way to deploy your full-stack app (Python backend + React frontend).

---

## 📋 Step 1: Sign Up for Render

1. Go to: **https://render.com**
2. Click **"Get Started"**
3. Sign up with GitHub
4. Authorize Render to access your repositories

---

## 🐍 Step 2: Deploy Backend (Python FastAPI)

### 2.1 Create Web Service
1. On Render dashboard, click **"New +"** → **"Web Service"**

### 2.2 Connect Repository
1. Find and select: **`Krishna-Rapido/internal_tools_v1`**
2. Click **"Connect"**

### 2.3 Configure Backend
Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `internal-tools-backend` |
| **Region** | `Singapore` (or closest to you) |
| **Branch** | `main` (or `v3` if that's your main branch) |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` (auto-detected) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python main.py` |
| **Instance Type** | **Free** |

### 2.4 Add Environment Variables (if needed)
- Click **"Advanced"** → **"Add Environment Variable"**
- Add any secrets (Presto credentials, etc.)

### 2.5 Deploy
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. **IMPORTANT**: Copy your backend URL
   - Example: `https://internal-tools-backend.onrender.com`
   - You'll see it at the top of the page

---

## ⚛️ Step 3: Deploy Frontend (React/Vite)

### 3.1 Create Static Site
1. Click **"New +"** → **"Static Site"**

### 3.2 Connect Same Repository
1. Select: **`Krishna-Rapido/internal_tools_v1`**
2. Click **"Connect"**

### 3.3 Configure Frontend
Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `internal-tools-frontend` |
| **Branch** | `main` (or `v3`) |
| **Root Directory** | `frontend` |
| **Build Command** | `npm install && npm run build` |
| **Publish Directory** | `frontend/dist` |

### 3.4 Add Environment Variable
⚠️ **CRITICAL STEP**:

1. Click **"Advanced"** → **"Add Environment Variable"**
2. Add this variable:
   ```
   Key: VITE_API_BASE_URL
   Value: https://internal-tools-backend.onrender.com
   ```
   (Use YOUR actual backend URL from Step 2.3)

### 3.5 Deploy
1. Click **"Create Static Site"**
2. Wait 3-5 minutes
3. Your frontend is live!
   - Example: `https://internal-tools-frontend.onrender.app`

---

## 🔧 Step 4: Update Backend CORS

Your backend needs to allow requests from the frontend.

### 4.1 Update main.py

In `/Users/krishna.poddar/Desktop/Rapido EDA/GIG/internal_tools_v1/backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://internal-tools-frontend.onrender.app",  # Your frontend URL
        "http://localhost:5173",  # For local development
        "*"  # Or use specific domains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4.2 Push Changes

```bash
cd /Users/krishna.poddar/Desktop/Rapido\ EDA/GIG/internal_tools_v1
git add backend/main.py
git commit -m "Update CORS for Render deployment"
git push
```

Render will automatically redeploy your backend!

---

## ✅ Step 5: Test Your Deployment

1. **Visit your frontend**: `https://internal-tools-frontend.onrender.app`
2. **Test backend connection**:
   - Visit: `https://internal-tools-backend.onrender.com/health`
   - Should return: `{"status":"ok"}`
3. **Test the app**:
   - Upload a CSV
   - Run analyses
   - Everything should work!

---

## 🎉 You're Live!

✅ **Frontend**: https://internal-tools-frontend.onrender.app  
✅ **Backend**: https://internal-tools-backend.onrender.com  

Share the frontend URL with your team!

---

## 🔄 Making Updates

```bash
# Make your changes
git add .
git commit -m "Your update message"
git push

# Both frontend and backend will auto-deploy!
# Wait 2-5 minutes for rebuild
```

---

## ⚠️ Important: Free Tier Limitations

**Render Free Tier**:
- ✅ 750 hours/month (plenty for testing)
- ⚠️ Backend sleeps after 15 minutes of inactivity
- ⚠️ First request after sleep: 30-60 seconds to wake up
- ✅ Frontend (static site): Always instant

**Upgrade to Paid** ($7/month per service) if you need:
- No sleep time
- Faster performance
- More hours

---

## 🐛 Troubleshooting

### CSS Not Loading (MIME Type Error)

**Already Fixed!** The vite.config now uses `base: '/'` for Render.

If you still see issues:
```bash
cd frontend
npm run build
# Check that dist/index.html references assets correctly
cat dist/index.html | grep assets
```

### Backend Not Responding

1. Check Render logs:
   - Go to backend service → "Logs" tab
   - Look for errors

2. Check health endpoint:
   - Visit: `https://your-backend.onrender.com/health`
   - Should return `{"status":"ok"}`

### Frontend Shows Blank Page

1. Check browser console (F12)
2. Look for API connection errors
3. Verify `VITE_API_BASE_URL` environment variable is set correctly in Render

---

## 📝 Files Created for You

✅ `backend/Procfile` - Render/Heroku config  
✅ `backend/railway.json` - Railway config  
✅ `backend/render.yaml` - Render config  
✅ `frontend/vite.config.ts` - Updated with smart base path  
✅ `.gitignore` - Ignore build files  
✅ `.github/workflows/deploy.yml` - GitHub Actions (if you use GitHub Pages)  

---

## 🎯 Quick Commands

```bash
# From project root

# 1. Commit and push
git add .
git commit -m "Deploy to Render"
git push

# 2. Go to Render.com and create services
# 3. Done!
```

---

**Need help?** Open an issue on GitHub or check the Render documentation: https://render.com/docs

Your app is ready to deploy! 🚀

