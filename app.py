import os
import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model artifacts at startup
try:
    model = joblib.load('model/titanic_survival_model.pkl')
    scaler = joblib.load('model/titanic_scaler.pkl')
    selected_features = joblib.load('model/selected_features.pkl')
    logger.info('✓ Model, scaler, and features loaded successfully')
except Exception as e:
    logger.error(f'✗ Error loading model artifacts: {e}')
    model = None
    scaler = None
    selected_features = None


@app.route('/')
def index():
    """Render the main prediction page"""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint - useful for monitoring deployment"""
    model_status = 'loaded' if model is not None else 'not loaded'
    return jsonify({
        'status': 'OK',
        'model_status': model_status
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint
    
    Expected JSON input:
    {
        "Pclass": 3,
        "Sex": "male",
        "Age": 25.0,
        "SibSp": 1,
        "Fare": 7.25
    }
    
    Returns:
    {
        "prediction": "Survived" or "Did Not Survive",
        "confidence": 78.45,
        "probabilities": {"Did Not Survive": 21.55, "Survived": 78.45}
    }
    """
    try:
        # Validate model is loaded
        if model is None or scaler is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Validate required fields
        missing_fields = [f for f in selected_features if f not in data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {missing_fields}'}), 400
        
        # Extract and validate input values
        try:
            Pclass = int(data['Pclass'])
            Sex = data['Sex'].lower()
            Age = float(data['Age'])
            SibSp = int(data['SibSp'])
            Fare = float(data['Fare'])
            
            # Validate ranges
            if not (1 <= Pclass <= 3):
                return jsonify({'error': 'Pclass must be 1, 2, or 3'}), 400
            if Sex not in ['male', 'female']:
                return jsonify({'error': 'Sex must be "male" or "female"'}), 400
            if not (0 <= Age <= 120):
                return jsonify({'error': 'Age must be between 0 and 120'}), 400
            if SibSp < 0:
                return jsonify({'error': 'SibSp cannot be negative'}), 400
            if Fare < 0:
                return jsonify({'error': 'Fare cannot be negative'}), 400
            
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Invalid input values: {str(e)}'}), 400
        
        # Encode Sex: Male=1, Female=0
        sex_encoded = 1 if Sex == 'male' else 0
        
        # Create feature vector in the correct order
        features = np.array([[Pclass, sex_encoded, Age, SibSp, Fare]])
        
        # Scale features using the fitted scaler
        features_scaled = scaler.transform(features)
        
        # ✓ CORRECT INFERENCE LOGIC
        # Use predict() for class label (not argmax!)
        predicted_class = int(model.predict(features_scaled)[0])
        
        # Use predict_proba() for confidence scores
        probabilities = model.predict_proba(features_scaled)[0]
        confidence = float(np.max(probabilities)) * 100
        
        # Map prediction to readable text
        prediction_text = 'Survived' if predicted_class == 1 else 'Did Not Survive'
        
        # Prepare response
        response = {
            'prediction': prediction_text,
            'confidence': round(confidence, 2),
            'probabilities': {
                'Did Not Survive': round(float(probabilities[0]) * 100, 2),
                'Survived': round(float(probabilities[1]) * 100, 2)
            },
            'input_features': {
                'Pclass': Pclass,
                'Sex': Sex,
                'Age': Age,
                'SibSp': SibSp,
                'Fare': Fare
            }
        }
        
        logger.info(f'Prediction made: {prediction_text} (confidence: {confidence:.2f}%)')
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Error in prediction: {str(e)}')
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # ✓ DEPLOYMENT-SAFE CONFIGURATION
    # Use environment variables for port and debug settings
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
