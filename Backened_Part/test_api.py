"""
Test script for Expense Forecaster API
Tests all endpoints including AI features
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def test_health():
    """Test health endpoint"""
    print_section("Testing Health Check")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_add_expense():
    """Test adding a single expense"""
    print_section("Testing Add Expense")
    expense = {
        "date": "2025-12-05",
        "category": "Food",
        "amount": 45.99,
        "description": "Lunch at restaurant"
    }
    response = requests.post(f"{BASE_URL}/api/expenses", json=expense)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 201

def test_get_expenses():
    """Test getting all expenses"""
    print_section("Testing Get All Expenses")
    response = requests.get(f"{BASE_URL}/api/expenses")
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Total Expenses: {data.get('count', 0)}")
    if data.get('expenses'):
        print(f"First Expense: {json.dumps(data['expenses'][0], indent=2)}")
    return response.status_code == 200

def test_get_categories():
    """Test getting categories"""
    print_section("Testing Get Categories")
    response = requests.get(f"{BASE_URL}/api/expenses/categories")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_statistics():
    """Test getting statistics"""
    print_section("Testing Get Statistics")
    response = requests.get(f"{BASE_URL}/api/expenses/statistics")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_ai_analyze():
    """Test AI analysis (requires Gemini API key)"""
    print_section("Testing AI Analysis")
    print("Note: This requires GEMINI_API_KEY to be set in .env file")
    response = requests.post(f"{BASE_URL}/api/ai/analyze")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        print("✓ AI Analysis Successful!")
        analysis = data.get('analysis', {})
        print(f"\nAnalysis Keys: {list(analysis.keys())}")
        if 'summary_statistics' in analysis:
            stats = analysis['summary_statistics']
            print(f"\nSummary Statistics:")
            print(f"  - Total: ${stats.get('total', 0):.2f}")
            print(f"  - Average Monthly: ${stats.get('avg_monthly', 0):.2f}")
            print(f"  - Date Range: {stats.get('start_date')} to {stats.get('end_date')}")
    else:
        print(f"✗ AI Analysis Failed: {data.get('error')}")
        if 'hint' in data:
            print(f"Hint: {data['hint']}")
    
    return response.status_code == 200

def test_ai_predict():
    """Test AI prediction (requires Gemini API key)"""
    print_section("Testing AI Prediction")
    print("Note: This requires GEMINI_API_KEY to be set in .env file")
    
    prediction_request = {
        "period": "month",
        "periods": 1
    }
    
    response = requests.post(f"{BASE_URL}/api/ai/predict", json=prediction_request)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        print("✓ AI Prediction Successful!")
        prediction = data.get('prediction', {})
        print(f"\nPrediction Summary:")
        print(f"  - Total Predicted: ${prediction.get('total_predicted', 0):.2f}")
        print(f"  - Period: {prediction.get('period_type')}")
        print(f"  - Confidence: {prediction.get('confidence_level')}")
        if 'category_predictions' in prediction:
            print(f"\nCategory Predictions:")
            for cat, pred in prediction['category_predictions'].items():
                print(f"  - {cat}: ${pred.get('amount', 0):.2f} (confidence: {pred.get('confidence')})")
    else:
        print(f"✗ AI Prediction Failed: {data.get('error')}")
        if 'hint' in data:
            print(f"Hint: {data['hint']}")
    
    return response.status_code == 200

def test_ai_recommendations():
    """Test AI recommendations (requires Gemini API key)"""
    print_section("Testing AI Recommendations")
    print("Note: This requires GEMINI_API_KEY to be set in .env file")
    
    recommendation_request = {
        "budget": 2000
    }
    
    response = requests.post(f"{BASE_URL}/api/ai/recommendations", json=recommendation_request)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        print("✓ AI Recommendations Successful!")
        recommendations = data.get('recommendations', {})
        print(f"\nRecommendations Keys: {list(recommendations.keys())}")
    else:
        print(f"✗ AI Recommendations Failed: {data.get('error')}")
        if 'hint' in data:
            print(f"Hint: {data['hint']}")
    
    return response.status_code == 200

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print(" EXPENSE FORECASTER API - TEST SUITE")
    print("="*60)
    print(f" Testing at: {BASE_URL}")
    print(f" Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    results = {
        "Health Check": test_health(),
        "Add Expense": test_add_expense(),
        "Get Expenses": test_get_expenses(),
        "Get Categories": test_get_categories(),
        "Get Statistics": test_get_statistics(),
        "AI Analysis": test_ai_analyze(),
        "AI Prediction": test_ai_predict(),
        "AI Recommendations": test_ai_recommendations()
    }
    
    print_section("TEST RESULTS SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed < total:
        print("\n⚠ Some tests failed. Check the output above for details.")
        print("⚠ AI tests require GEMINI_API_KEY in .env file")
    else:
        print("\n✓ All tests passed successfully!")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to the API server")
        print("Make sure the server is running at http://localhost:5000")
        print("Run: python app.py")
        exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        exit(1)
