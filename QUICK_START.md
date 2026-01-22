# QUICK START REFERENCE

## ⚡ Fast Setup (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the notebook (or skip if artifacts exist)
cd model
jupyter notebook model_building.ipynb
# Run all cells

# 3. Start the app
cd ..
python app.py
```

Open browser: `http://localhost:5000`

---

## 🎯 Key Things Implemented to Get Full Marks

### ✅ Data Preprocessing (PART A)
- [x] Handled missing values (Age → median, removed Survived NaNs)
- [x] Selected 5 features: Pclass, Sex, Age, SibSp, Fare
- [x] Encoded categorical (Sex: male=1, female=0)
- [x] **Split data BEFORE scaling** (prevents data leakage)
- [x] Fitted scaler ONLY on X_train
- [x] Applied scaler to both X_train and X_test

### ✅ Model Development (PART A)
- [x] Loaded Titanic dataset
- [x] Trained Random Forest Classifier
- [x] Printed classification report
- [x] Saved model with Joblib
- [x] Demonstrated reload without retraining

### ✅ Web GUI (PART B)
- [x] Flask app with HTML/CSS
- [x] Loads saved model
- [x] Accepts user input (5 features)
- [x] **Uses predict() for labels** (not argmax!)
- [x] **Uses predict_proba() for confidence** (not max!)
- [x] Displays survival result
- [x] Professional styling

### ✅ GitHub Upload (PART C)
- [x] Correct directory structure
- [x] All required files present
- [x] README with clear instructions

### ✅ Deployment (PART D)
- [x] Environment variable for PORT
- [x] debug=False (not True!)
- [x] Health check endpoint (/health)
- [x] Proper error handling

### ✅ Submission (Scorac.com)
- [x] Titanic_hosted_webGUI_link.txt ready
- [x] All required fields documented

---

## � Python Version (IMPORTANT for Render)

**Recommended**: Python 3.10.13 (specified in `runtime.txt`)

This ensures compatibility across:
- Local development
- Render.com deployment
- scikit-learn, Flask, and all dependencies

Check your Python version:
```bash
python --version
```

Should output: `Python 3.10.x` or higher

---

### Step 1: Replace Placeholder Text
Find and replace in project folder:
```
YourName → Your Full Name
YourMatricNo → Your Matric Number
```

### Step 2: Create GitHub Repository
```bash
git init
git add .
git commit -m "Initial Titanic Survival Prediction System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Titanic_Project_YourName_YourMatricNo.git
git push -u origin main
```

### Step 3: Deploy (Choose One)

#### **Option A: Render.com (Easiest)**
1. Go to render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Add environment variables:
   - PORT: 10000
   - DEBUG: False
7. Deploy
8. Copy the URL: `https://your-app-name.onrender.com`

#### **Option B: PythonAnywhere.com**
1. Sign up at pythonanywhere.com
2. Upload files via "Files" tab
3. Create web app (Flask)
4. Update WSGI file to point to app.py
5. Install requirements in bash console
6. Reload web app
7. Copy the URL: `https://yourname.pythonanywhere.com`

#### **Option C: Heroku Alternative (Railway.app)**
Similar to Render; connect GitHub and deploy

### Step 4: Update Submission File
Edit `Titanic_hosted_webGUI_link.txt`:
```
Name: YOUR FULL NAME
Matric Number: YOUR MATRIC NUMBER
Machine Learning Algorithm Used: Random Forest Classifier
Model Persistence Method Used: Joblib
Live URL of Hosted Application: https://your-deployed-app-url.com
GitHub Repository Link: https://github.com/YOUR_USERNAME/Titanic_Project_YourName_YourMatricNo
```

### Step 5: Submit to Scorac.com
Upload the entire folder structure named **Titanic_Project_EjikeChiamaka_22CG031853** before **February 5, 2026, 11:59 PM**

**Must include:**
- ✓ app.py
- ✓ requirements.txt
- ✓ runtime.txt (Python version)
- ✓ Procfile (deployment config)
- ✓ Titanic_hosted_webGUI_link.txt
- ✓ model/model_building.ipynb
- ✓ model/titanic_survival_model.pkl
- ✓ model/titanic_scaler.pkl
- ✓ templates/index.html
- ✓ static/style.css

---

## 🧪 Testing the Prediction Endpoint

### Test in Browser
1. Go to http://localhost:5000
2. Fill form:
   - Passenger Class: 3
   - Sex: male
   - Age: 25
   - Siblings/Spouses: 1
   - Fare: 7.25
3. Click "Predict Survival"
4. Should show result with confidence

### Test via API (cURL)
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"Pclass": 1, "Sex": "female", "Age": 25, "SibSp": 1, "Fare": 72.0}'
```

Expected response:
```json
{
    "prediction": "Survived",
    "confidence": 92.50,
    "probabilities": {
        "Did Not Survive": 7.50,
        "Survived": 92.50
    }
}
```

---

## ❌ Common Mistakes to Avoid (Already Fixed!)

### ✗ WRONG (Previous Assignment)
```python
# Mistake 1: Scaling before split
X_scaled = scaler.fit_transform(X)
X_train, X_test = train_test_split(X_scaled, ...)

# Mistake 2: Using argmax for predictions
prediction = model.predict(features_scaled)
predicted_class = np.argmax(prediction)  # WRONG!

# Mistake 3: Hard-coded port
app.run(debug=True, port=5003)
```

### ✓ CORRECT (This Project)
```python
# Fix 1: Split BEFORE scaling
X_train, X_test = train_test_split(X, ...)
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Fix 2: Use predict() and predict_proba()
pred_label = model.predict(features_scaled)[0]
proba = model.predict_proba(features_scaled)[0]
confidence = np.max(proba) * 100

# Fix 3: Environment variables
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=False)
```

---

## 📊 Model Training Checklist

Run `model_building.ipynb` and verify:
- [x] Dataset loads (714+ rows)
- [x] Missing values handled
- [x] Features encoded
- [x] **Train/test split FIRST**
- [x] **Scaler fitted ONLY on X_train**
- [x] Model trained
- [x] Classification report printed
- [x] Model saved to `titanic_survival_model.pkl`
- [x] Scaler saved to `titanic_scaler.pkl`
- [x] Features saved to `selected_features.pkl`
- [x] Reload test successful

---

## 🚀 Deployment Checklist

- [ ] Local testing works (python app.py)
- [ ] GitHub repository created and pushed
- [ ] Deployed to Render/PythonAnywhere/other platform
- [ ] Live URL working in browser
- [ ] /health endpoint returns OK
- [ ] /predict endpoint works with test data
- [ ] Titanic_hosted_webGUI_link.txt updated
- [ ] Folder renamed to Titanic_Project_[Name]_[MatricNo]
- [ ] Submitted to Scorac.com before deadline

---

## 📞 Debugging Help

### If model won't load:
```bash
# Check if files exist
ls model/titanic_survival_model.pkl
ls model/titanic_scaler.pkl
ls model/selected_features.pkl

# If missing, retrain:
jupyter notebook model/model_building.ipynb
```

### If port 5000 in use:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [PID] /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### If deployment fails:
1. Check environment variables set correctly
2. Ensure requirements.txt installed
3. Check logs in platform dashboard
4. Verify model files uploaded

---

## 🎓 Scoring Breakdown (Full 15 pts)

- **Part A (Model Development)**: 5 pts
  - Data preprocessing with no leakage
  - Correct algorithm implementation
  - Classification report printed
  - Model saved and reloaded successfully

- **Part B (Web GUI)**: 4 pts
  - Loads model correctly
  - Input form works
  - **Correct prediction logic (predict_proba)**
  - Professional interface

- **Part C (GitHub)**: 3 pts
  - Correct directory structure
  - All files present
  - Clear documentation

- **Part D (Deployment)**: 3 pts
  - Live URL working
  - Environment variables used
  - Deployment-safe code

---

**Target**: 15/15 ✓ All implementations done!
