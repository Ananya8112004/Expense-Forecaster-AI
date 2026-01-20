from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from ai_agent import ExpenseForecastingAgent
from data_manager import DataManager
from datetime import datetime, timedelta
import traceback

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Initialize components
Config.init_app()
data_manager = DataManager()
ai_agent = None

def get_ai_agent():
    """Lazy initialization of AI agent"""
    global ai_agent
    if ai_agent is None:
        try:
            ai_agent = ExpenseForecastingAgent()
        except ValueError as e:
            raise ValueError(f"Failed to initialize AI agent: {str(e)}")
    return ai_agent

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Expense Forecaster API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

# Expense management endpoints
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses or filter by date range/category"""
    try:
        # Check for query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        category = request.args.get('category')
        
        if start_date and end_date:
            expenses = data_manager.get_expenses_by_date_range(start_date, end_date)
        elif category:
            expenses = data_manager.get_expenses_by_category(category)
        else:
            expenses = data_manager.get_all_expenses()
        
        return jsonify({
            'success': True,
            'count': len(expenses),
            'expenses': expenses
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    """Get a specific expense by ID"""
    try:
        expense = data_manager.get_expense_by_id(expense_id)
        
        if expense:
            return jsonify({
                'success': True,
                'expense': expense
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Expense not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    """Add a new expense"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate required fields
        if 'amount' not in data:
            return jsonify({
                'success': False,
                'error': 'Amount is required'
            }), 400
        
        expense = data_manager.add_expense(data)
        
        return jsonify({
            'success': True,
            'message': 'Expense added successfully',
            'expense': expense
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/expenses/bulk', methods=['POST'])
def add_bulk_expenses():
    """Add multiple expenses at once"""
    try:
        data = request.get_json()
        
        if not data or 'expenses' not in data:
            return jsonify({
                'success': False,
                'error': 'No expenses provided'
            }), 400
        
        result = data_manager.add_bulk_expenses(data['expenses'])
        
        return jsonify({
            'success': True,
            'message': f'{result["count"]} expenses added successfully',
            'expenses': result['expenses']
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """Update an existing expense"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        expense = data_manager.update_expense(expense_id, data)
        
        if expense:
            return jsonify({
                'success': True,
                'message': 'Expense updated successfully',
                'expense': expense
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Expense not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete an expense"""
    try:
        success = data_manager.delete_expense(expense_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Expense deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Expense not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/expenses/categories', methods=['GET'])
def get_categories():
    """Get list of all categories"""
    try:
        categories = data_manager.get_categories()
        
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/expenses/statistics', methods=['GET'])
def get_statistics():
    """Get expense statistics"""
    try:
        stats = data_manager.get_statistics()
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# AI Agent endpoints
@app.route('/api/ai/analyze', methods=['POST'])
def analyze_expenses():
    """Analyze expenses using AI agent"""
    try:
        agent = get_ai_agent()
        
        # Get expenses data
        data = request.get_json()
        
        if data and 'expenses' in data:
            expenses = data['expenses']
        else:
            # Use all expenses from database
            expenses = data_manager.get_all_expenses()
        
        if not expenses:
            return jsonify({
                'success': False,
                'error': 'No expense data available for analysis'
            }), 400
        
        # Perform analysis
        analysis = agent.analyze_expenses(expenses)
        
        if 'error' in analysis:
            return jsonify({
                'success': False,
                'error': analysis['error']
            }), 400
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'hint': 'Please set GEMINI_API_KEY in .env file'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/ai/predict', methods=['POST'])
def predict_expenses():
    """Predict future expenses using AI agent"""
    try:
        agent = get_ai_agent()
        
        data = request.get_json()
        
        # Get expenses data
        if data and 'expenses' in data:
            expenses = data['expenses']
        else:
            expenses = data_manager.get_all_expenses()
        
        if not expenses:
            return jsonify({
                'success': False,
                'error': 'No expense data available for prediction'
            }), 400
        
        # Get prediction parameters
        forecast_period = data.get('period', 'month') if data else 'month'
        periods = data.get('periods', 1) if data else 1
        
        # Validate parameters
        if forecast_period not in ['month', 'quarter']:
            return jsonify({
                'success': False,
                'error': 'Period must be either "month" or "quarter"'
            }), 400
        
        # Perform prediction
        prediction = agent.predict_expenses(expenses, forecast_period, periods)
        
        if 'error' in prediction:
            return jsonify({
                'success': False,
                'error': prediction['error']
            }), 400
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'hint': 'Please set GEMINI_API_KEY in .env file'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/ai/recommendations', methods=['POST'])
def get_recommendations():
    """Get AI-powered recommendations"""
    try:
        agent = get_ai_agent()
        
        data = request.get_json()
        
        # Get expenses data
        if data and 'expenses' in data:
            expenses = data['expenses']
        else:
            expenses = data_manager.get_all_expenses()
        
        if not expenses:
            return jsonify({
                'success': False,
                'error': 'No expense data available for recommendations'
            }), 400
        
        # Get budget if provided
        budget = data.get('budget') if data else None
        
        # Get recommendations
        recommendations = agent.get_recommendations(expenses, budget)
        
        if 'error' in recommendations:
            return jsonify({
                'success': False,
                'error': recommendations['error']
            }), 400
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'hint': 'Please set GEMINI_API_KEY in .env file'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

# Utility endpoint to generate sample data
@app.route('/api/utils/generate-sample-data', methods=['POST'])
def generate_sample_data():
    """Generate sample expense data for testing"""
    try:
        from datetime import timedelta
        import random
        
        categories = ['Food', 'Transportation', 'Utilities', 'Entertainment', 'Healthcare', 'Shopping', 'Education']
        descriptions = {
            'Food': ['Groceries', 'Restaurant', 'Coffee shop', 'Fast food'],
            'Transportation': ['Gas', 'Uber', 'Public transit', 'Parking'],
            'Utilities': ['Electricity', 'Water', 'Internet', 'Phone'],
            'Entertainment': ['Movies', 'Concert', 'Streaming service', 'Games'],
            'Healthcare': ['Pharmacy', 'Doctor visit', 'Dental', 'Gym'],
            'Shopping': ['Clothing', 'Electronics', 'Home goods', 'Gifts'],
            'Education': ['Books', 'Course', 'Supplies', 'Tuition']
        }
        
        # Generate expenses for last 6 months
        expenses = []
        start_date = datetime.now() - timedelta(days=180)
        
        for i in range(100):
            category = random.choice(categories)
            date = start_date + timedelta(days=random.randint(0, 180))
            amount = round(random.uniform(10, 500), 2)
            description = random.choice(descriptions[category])
            
            expenses.append({
                'date': date.strftime('%Y-%m-%d'),
                'category': category,
                'amount': amount,
                'description': description
            })
        
        result = data_manager.add_bulk_expenses(expenses)
        
        return jsonify({
            'success': True,
            'message': f'Generated {result["count"]} sample expenses',
            'count': result["count"]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/utils/clear-data', methods=['DELETE'])
def clear_data():
    """Clear all expense data"""
    try:
        data_manager.clear_all_expenses()
        
        return jsonify({
            'success': True,
            'message': 'All expense data cleared'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("=" * 50)
    print("Expense Forecaster API Server")
    print("=" * 50)
    print(f"Server starting on http://{Config.HOST}:{Config.PORT}")
    print("\nAvailable Endpoints:")
    print("- GET    /api/health - Health check")
    print("- GET    /api/expenses - Get all expenses")
    print("- POST   /api/expenses - Add new expense")
    print("- POST   /api/expenses/bulk - Add multiple expenses")
    print("- GET    /api/expenses/<id> - Get expense by ID")
    print("- PUT    /api/expenses/<id> - Update expense")
    print("- DELETE /api/expenses/<id> - Delete expense")
    print("- GET    /api/expenses/categories - Get all categories")
    print("- GET    /api/expenses/statistics - Get statistics")
    print("- POST   /api/ai/analyze - Analyze expenses with AI")
    print("- POST   /api/ai/predict - Predict future expenses")
    print("- POST   /api/ai/recommendations - Get AI recommendations")
    print("- POST   /api/utils/generate-sample-data - Generate test data")
    print("- DELETE /api/utils/clear-data - Clear all data")
    print("=" * 50)
    
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
