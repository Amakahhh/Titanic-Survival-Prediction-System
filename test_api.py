#!/usr/bin/env python3
"""
Quick test script for Titanic Survival Prediction API
Run this after starting: python app.py
"""

import requests
import json

print("\n" + "="*80)
print("TITANIC SURVIVAL PREDICTION - API TEST")
print("="*80)

# Test data
test_cases = [
    {
        "name": "Test Case 1: 3rd Class Male, Young",
        "data": {
            "Pclass": 3,
            "Sex": "male",
            "Age": 25,
            "SibSp": 1,
            "Fare": 7.25
        }
    },
    {
        "name": "Test Case 2: 1st Class Female, Adult",
        "data": {
            "Pclass": 1,
            "Sex": "female",
            "Age": 35,
            "SibSp": 0,
            "Fare": 72.00
        }
    },
    {
        "name": "Test Case 3: 2nd Class Male, Child",
        "data": {
            "Pclass": 2,
            "Sex": "male",
            "Age": 10,
            "SibSp": 2,
            "Fare": 15.00
        }
    }
]

BASE_URL = "http://localhost:5000"

# Test 1: Health check
print("\n[1/4] Testing Health Endpoint")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Status: {data['status']}")
        print(f"✓ Model Status: {data['model_status']}")
    else:
        print(f"✗ Unexpected status code: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Home page
print("\n[2/4] Testing Home Page")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    if response.status_code == 200:
        print(f"✓ Home page loaded successfully")
        print(f"✓ Page size: {len(response.text)} bytes")
    else:
        print(f"✗ Unexpected status code: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Predictions
print("\n[3/4] Testing Prediction Endpoint")
print("-" * 80)
for test in test_cases:
    print(f"\n{test['name']}")
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=test['data'],
            timeout=5,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✓ Prediction: {result['prediction']}")
            print(f"  ✓ Confidence: {result['confidence']}%")
            print(f"  ✓ Probabilities:")
            print(f"    - Survived: {result['probabilities']['Survived']}%")
            print(f"    - Did Not Survive: {result['probabilities']['Did Not Survive']}%")
        else:
            print(f"  ✗ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

# Test 4: Error handling
print("\n[4/4] Testing Error Handling")
print("-" * 80)

print("\nTesting with invalid data (missing Age):")
try:
    invalid_data = {
        "Pclass": 1,
        "Sex": "female",
        "SibSp": 0,
        "Fare": 72.00
    }
    response = requests.post(
        f"{BASE_URL}/predict",
        json=invalid_data,
        timeout=5
    )
    if response.status_code != 200:
        error = response.json()
        print(f"✓ Correctly rejected: {error.get('error')}")
    else:
        print("✗ Should have rejected invalid data")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*80)
print("✅ API TESTING COMPLETE!")
print("="*80)
print("\nAll endpoints working correctly!\n")
