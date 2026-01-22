# Titanic Survival Prediction System

A machine learning-powered web application that predicts whether a Titanic passenger would have survived the disaster based on their characteristics.

## Project Overview

This project implements a complete machine learning pipeline with a web-based GUI for predicting Titanic passenger survival. The system uses a Random Forest Classifier trained on historical passenger data.

### Features Used (5 Input Features)
- **Pclass**: Passenger Class (1st, 2nd, or 3rd)
- **Sex**: Passenger Gender (Male/Female)
- **Age**: Passenger Age (in years)
- **SibSp**: Number of Siblings/Spouses aboard
- **Fare**: Ticket Price (in British Pounds)

### Target Variable
- **Survived**: Whether the passenger survived (0 = Did Not Survive, 1 = Survived)

## Project Structure

```
Titanic_Project_EjikeChiamaka_22CG031853/
├── app.py                          # Flask web application
├── requirements.txt                # Python dependencies
├── Titanic_hosted_webGUI_link.txt  # Submission details
├── model/
│   ├── model_building.ipynb        # Model development notebook
│   ├── titanic_survival_model.pkl  # Trained model artifact
│   └── titanic_scaler.pkl          # Feature scaler artifact
├── static/
│   └── style.css                   # CSS styling
└── templates/
    └── index.html                  # HTML interface
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <your-github-repo-url>
cd Titanic_Project_EjikeChiamaka_22CG031853
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Model Artifacts
Ensure these files exist in the `model/` directory:
- `titanic_survival_model.pkl` (trained Random Forest model)
- `titanic_scaler.pkl` (feature scaler)
- `selected_features.pkl` (feature names)

If missing, run the model development notebook:
```bash
cd model
jupyter notebook model_building.ipynb
```

## Running the Application

### Local Development
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

### Using Gunicorn (Production-like)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app.py
```

### With Environment Variables (Deployment)
```bash
# Set port
set PORT=8000        # Windows
export PORT=8000     # Linux/Mac

# Set debug mode (optional)
set DEBUG=False      # Windows
export DEBUG=False   # Linux/Mac

python app.py
```

## API Endpoints

### 1. GET `/`
**Description**: Returns the main web GUI
```
Method: GET
Response: HTML page
```

### 2. GET `/health`
**Description**: Health check endpoint (useful for monitoring)
```
Method: GET
Response: 
{
    "status": "OK",
    "model_status": "loaded"
}
```

### 3. POST `/predict`
**Description**: Makes a survival prediction based on passenger data

**Request Format**:
```json
{
    "Pclass": 3,
    "Sex": "male",
    "Age": 25.0,
    "SibSp": 1,
    "Fare": 7.25
}
```

**Response Format** (Success - 200 OK):
```json
{
    "prediction": "Survived",
    "confidence": 78.45,
    "probabilities": {
        "Did Not Survive": 21.55,
        "Survived": 78.45
    },
    "input_features": {
        "Pclass": 3,
        "Sex": "male",
        "Age": 25.0,
        "SibSp": 1,
        "Fare": 7.25
    }
}
```

**Response Format** (Error - 400/500):
```json
{
    "error": "Missing fields: ['Age']"
}
```

## Model Details

### Algorithm
- **Type**: Random Forest Classifier
- **Hyperparameters**:
  - `n_estimators`: 100
  - `max_depth`: 10
  - `random_state`: 42

### Data Preprocessing
✓ **Correct approach implemented**:
1. Train-test split FIRST (80% train, 20% test)
2. Fit StandardScaler ONLY on training data
3. Apply scaler to both train and test sets

### Model Performance
- **Metric**: Classification Report
- Run the notebook to see detailed metrics

## Key Features

### ✓ Data Leakage Prevention
- Scaler fitted only on training data
- Train/test split before scaling
- Proper feature validation

### ✓ Correct Inference Logic
- Uses `model.predict()` for class labels
- Uses `model.predict_proba()` for confidence scores
- Prevents argmax errors with classifier outputs

### ✓ Deployment-Safe Configuration
- Port from environment variables (default: 5000)
- Debug mode controlled by environment (default: False)
- Health check endpoint for monitoring
- Proper error handling and logging

### ✓ Feature Validation
- Saved feature names for consistency
- Input validation on all fields
- Range validation for numeric inputs

## Deployment Options

### Option 1: Render.com
1. Push repository to GitHub
2. Connect repository to Render
3. Set environment variables:
   - `PORT`: 10000 (Render's port)
   - `DEBUG`: False
4. Deploy

### Option 2: PythonAnywhere.com
1. Upload project files
2. Create web app (Flask)
3. Configure WSGI file to point to app.py
4. Set up virtual environment with requirements

### Option 3: Streamlit Cloud
- Simplest option for Streamlit apps
- Fork repository and deploy

### Option 4: Heroku (or similar alternatives)
1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Deploy using git push
3. Set environment variables via dashboard

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Model artifacts not found
**Solution**: Check `model/` directory contains:
- `titanic_survival_model.pkl`
- `titanic_scaler.pkl`
- `selected_features.pkl`

### Issue: Port already in use
**Solution**: Use a different port
```bash
set PORT=5001
python app.py
```

### Issue: Prediction returns wrong results
**Cause**: Model artifacts might be corrupted
**Solution**: Retrain model by running `model_building.ipynb`

## Testing the Prediction API

### Using cURL
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"Pclass": 1, "Sex": "female", "Age": 25, "SibSp": 1, "Fare": 72.0}'
```

### Using Python
```python
import requests

data = {
    "Pclass": 1,
    "Sex": "female",
    "Age": 25,
    "SibSp": 1,
    "Fare": 72.0
}

response = requests.post('http://localhost:5000/predict', json=data)
print(response.json())
```

## Key Implementation Details

### Avoiding Previous Mistakes

**1. Model Inference Mismatch** ✓
- Uses `model.predict()` for class labels (not argmax)
- Uses `model.predict_proba()` for confidence

**2. Data Preprocessing Leakage** ✓
- Split data BEFORE scaling
- Fit scaler only on X_train

**3. Deployment Robustness** ✓
- Uses environment variables for port
- Sets debug=False for production
- Includes health check endpoint

**4. Feature Validation** ✓
- Saves selected features
- Validates feature ordering in app.py

## Technologies Used

- **Backend**: Flask (Python web framework)
- **ML Framework**: scikit-learn
- **Data Processing**: pandas, numpy
- **Model Persistence**: joblib
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Gunicorn (WSGI server)

## Model Evaluation Metrics

The model is evaluated using:
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- Classification Report

See `model_building.ipynb` for detailed evaluation results.

## Performance Notes

- **Training Data**: ~714 passengers
- **Test Data**: ~178 passengers
- **Features**: 5 numerical/encoded features
- **Classes**: Binary (Survived/Did Not Survive)

## Submission Requirements

All files required for Scorac.com submission:
- ✓ `app.py`
- ✓ `requirements.txt`
- ✓ `Titanic_hosted_webGUI_link.txt` (create before submission)
- ✓ `model/model_building.ipynb`
- ✓ `model/titanic_survival_model.pkl`
- ✓ `model/titanic_scaler.pkl`
- ✓ `templates/index.html`
- ✓ `static/style.css`

## File: Titanic_hosted_webGUI_link.txt

Create this file with the following content:
```
Name: Your Full Name
Matric Number: Your Matric Number
Machine Learning Algorithm Used: Random Forest Classifier
Model Persistence Method: Joblib
Live URL of Hosted Application: https://your-deployed-app-url.com
GitHub Repository Link: https://github.com/your-username/Titanic_Project_YourName_YourMatricNo
```

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Titanic Dataset](https://www.kaggle.com/c/titanic/)

## Author Notes

This project demonstrates:
- Complete ML pipeline from data to deployment
- Production-safe code practices
- Web GUI development
- API design
- Model persistence and reloading
- Error handling and validation

---

**Submission Deadline**: Friday, February 5, 2026, 11:59 PM  
**Score Target**: Full marks (15/15 pts)
