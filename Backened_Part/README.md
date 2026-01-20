# Expense Forecaster Backend

AI-powered expense forecasting system using Flask and Google Gemini API.

## Features

- **Expense Management**: CRUD operations for expense tracking
- **AI Analysis**: Analyze spending patterns and trends using Gemini AI
- **Expense Prediction**: Forecast future expenses for months or quarters
- **Smart Recommendations**: Get AI-powered suggestions for expense optimization
- **Seasonal Pattern Detection**: Identify seasonal spending variations

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the backend directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DEBUG=True
HOST=0.0.0.0
PORT=5000
```

**Get your free Gemini API Key:**
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

### 3. Run the Server

```bash
python app.py
```

The server will start at `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /api/health` - Check server status

### Expense Management
- `GET /api/expenses` - Get all expenses
  - Query params: `?start_date=2024-01-01&end_date=2024-12-31` or `?category=Food`
- `POST /api/expenses` - Add new expense
  ```json
  {
    "date": "2024-12-05",
    "category": "Food",
    "amount": 45.99,
    "description": "Groceries"
  }
  ```
- `POST /api/expenses/bulk` - Add multiple expenses
  ```json
  {
    "expenses": [
      {"date": "2024-12-05", "category": "Food", "amount": 45.99, "description": "Groceries"},
      {"date": "2024-12-04", "category": "Transport", "amount": 20.00, "description": "Uber"}
    ]
  }
  ```
- `GET /api/expenses/<id>` - Get expense by ID
- `PUT /api/expenses/<id>` - Update expense
- `DELETE /api/expenses/<id>` - Delete expense
- `GET /api/expenses/categories` - Get all categories
- `GET /api/expenses/statistics` - Get statistics

### AI Features
- `POST /api/ai/analyze` - Analyze expenses with AI
  ```json
  {
    "expenses": [] // Optional, uses all expenses if not provided
  }
  ```
- `POST /api/ai/predict` - Predict future expenses
  ```json
  {
    "period": "month",  // or "quarter"
    "periods": 1        // number of periods to forecast
  }
  ```
- `POST /api/ai/recommendations` - Get AI recommendations
  ```json
  {
    "budget": 2000  // Optional monthly budget
  }
  ```

### Utilities
- `POST /api/utils/generate-sample-data` - Generate 100 sample expenses for testing
- `DELETE /api/utils/clear-data` - Clear all expense data

## Project Structure

```
backend/
├── app.py              # Main Flask application
├── ai_agent.py         # AI agent for predictions and analysis
├── data_manager.py     # Data storage and management
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .env.example       # Example environment file
└── data/              # JSON data storage (auto-created)
    └── expenses.json  # Expense records
```

## Usage Example

1. **Generate Sample Data** (for testing):
   ```bash
   curl -X POST http://localhost:5000/api/utils/generate-sample-data
   ```

2. **Analyze Expenses**:
   ```bash
   curl -X POST http://localhost:5000/api/ai/analyze
   ```

3. **Predict Next Month's Expenses**:
   ```bash
   curl -X POST http://localhost:5000/api/ai/predict \
     -H "Content-Type: application/json" \
     -d '{"period": "month", "periods": 1}'
   ```

4. **Get Recommendations**:
   ```bash
   curl -X POST http://localhost:5000/api/ai/recommendations \
     -H "Content-Type: application/json" \
     -d '{"budget": 2000}'
   ```

## Technologies Used

- **Flask**: Web framework
- **Google Gemini AI**: AI-powered predictions and analysis
- **Pandas**: Data analysis
- **NumPy**: Numerical computations
- **Flask-CORS**: Cross-origin resource sharing

## Notes

- Data is stored in JSON format in the `data/` directory
- The Gemini API key is free to use with rate limits
- All AI operations require valid historical expense data
- Predictions improve with more historical data
