# RENDER DEPLOYMENT GUIDE
## For Titanic Survival Prediction System

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure:
- [ ] Local testing successful (`python app.py` works)
- [ ] All model artifacts present (`model/*.pkl` files)
- [ ] GitHub repository created and code pushed
- [ ] Python 3.10.13 specified in `runtime.txt`
- [ ] `requirements.txt` has all dependencies
- [ ] `Procfile` contains: `web: gunicorn app:app`
- [ ] `.gitignore` file present
- [ ] No hardcoded ports or debug=True

---

## 🚀 Deployment Steps (10 minutes)

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub or email
3. Link your GitHub account

### Step 2: Create New Web Service
1. Click "New +" in top-right
2. Select "Web Service"
3. Connect your GitHub repository
4. Search for `Titanic_Project_EjikeChiamaka_22CG031853`
5. Click "Connect"

### Step 3: Configure Service
Fill in the following:

| Field | Value |
|-------|-------|
| **Name** | titanic-survival-prediction |
| **Region** | Choose closest to you (e.g., Frankfurt, Singapore) |
| **Branch** | main |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

### Step 4: Add Environment Variables
Click "Advanced" and add:

| Key | Value |
|-----|-------|
| **PORT** | 10000 |
| **DEBUG** | False |
| **PYTHON_VERSION** | 3.10.13 |

### Step 5: Create Web Service
- Click "Create Web Service"
- Wait 3-5 minutes for deployment
- You'll see logs in real-time
- Once done, you get a URL like: `https://titanic-survival-prediction.onrender.com`

### Step 6: Test Deployment
1. Visit the URL in browser
2. Fill out the form with test data:
   - Class: 3
   - Sex: male
   - Age: 25
   - SibSp: 1
   - Fare: 7.25
3. Click "Predict Survival"
4. Should see result with confidence

---

## 🔍 Troubleshooting Render Deployment

### Issue: Build Failed (Python Version)
**Error**: `Python 3.x not found`
**Fix**: 
- Verify `runtime.txt` contains: `python-3.10.13`
- Commit and push changes
- Redeploy

### Issue: Build Failed (Dependencies)
**Error**: `No module named 'flask'`
**Fix**:
- Verify `requirements.txt` exists
- Check all package names spelled correctly
- Redeploy

### Issue: Model Not Found
**Error**: `FileNotFoundError: model/titanic_survival_model.pkl`
**Fix**:
1. Ensure model files committed to GitHub:
   ```bash
   git add model/*.pkl
   git commit -m "Add model artifacts"
   git push
   ```
2. Redeploy on Render
3. Check Render logs for confirmation

### Issue: Port Error
**Error**: `Address already in use`
**Fix**:
- Render assigns PORT automatically
- App.py already reads: `port = int(os.environ.get("PORT", 10000))`
- Should work automatically

### Issue: ModuleNotFoundError: No module named 'app'
**Error**: When Render tries to run gunicorn
**Fix**:
- Ensure `app.py` exists in root directory
- `Procfile` contains: `web: gunicorn app:app`
- No typos in filenames

### Issue: 502 Bad Gateway
**Error**: After deployment, app gives 502 error
**Fix**:
- Check logs in Render dashboard
- Usually means app crashed on startup
- Common cause: Missing model files
- Solution: Commit and push all files, redeploy

---

## 📊 Monitoring Your Deployment

### View Logs
1. Go to your Render dashboard
2. Click on your service
3. Scroll to "Logs" tab
4. See real-time logs of requests

### Check Health
```
https://your-app-url.onrender.com/health
```
Should return:
```json
{
    "status": "OK",
    "model_status": "loaded"
}
```

### Redeploy After Changes
1. Make changes locally
2. Test with `python app.py`
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Your message"
   git push origin main
   ```
4. Render auto-deploys (or manually trigger)

---

## 📝 Git Commands for First-Time Setup

```bash
# Initialize git repo
git init
git add .
git commit -m "Initial Titanic Survival Prediction System"

# Rename branch to main
git branch -M main

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/Titanic_Project_EjikeChiamaka_22CG031853.git

# Push to GitHub
git push -u origin main

# For future updates
git add .
git commit -m "Update message"
git push
```

---

## ✅ Final Checklist Before Submission

- [ ] App runs locally without errors
- [ ] GitHub repository is public
- [ ] Deployed on Render (or other platform)
- [ ] Live URL working in browser
- [ ] Predictions working correctly
- [ ] `/health` endpoint returns OK
- [ ] Updated `Titanic_hosted_webGUI_link.txt` with live URL
- [ ] Ready for Scorac.com submission

---

## 📱 Live URL Format

Your deployed app URL will be:
```
https://titanic-survival-prediction.onrender.com
```

(Exact name depends on what you set in Render)

Add this URL to `Titanic_hosted_webGUI_link.txt`:
```
Live URL of Hosted Application: https://your-app-url-here.onrender.com
```

---

## 🆘 Need Help?

### Check These First:
1. Render Logs (most helpful)
2. Local testing (`python app.py`)
3. GitHub commit history (`git log`)
4. File structure matches requirements

### Common Success Signs:
✓ Build successful (green checkmark)
✓ App running (blue "Running" status)
✓ No errors in logs
✓ Home page loads
✓ Predictions work

---

**Estimated Render Free Tier Limits:**
- 750 free hours/month (enough for testing)
- Auto-pauses after 15 mins of inactivity
- Redeploy on next visit (takes ~30 secs)

---

**Deployment Deadline: February 5, 2026, 11:59 PM**
