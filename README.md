# 🚀 Expense Forecaster - Complete Project

An **AI-powered expense forecasting application** that predicts future expenses using historical data and seasonal patterns. Built with Flask (backend) and React (frontend).

## ✨ Features

### 💰 Expense Management
- ✅ Add, edit, and delete expenses
- ✅ Category-based organization
- ✅ Date filtering and search
- ✅ Bulk import support
- ✅ Real-time statistics

### 🤖 AI-Powered Predictions
- ✅ Monthly and quarterly expense forecasts
- ✅ Category-specific predictions
- ✅ Confidence level indicators
- ✅ Seasonal pattern detection
- ✅ Risk factor analysis

### 📊 Analytics & Insights
- ✅ Spending pattern analysis
- ✅ Trend identification
- ✅ Anomaly detection
- ✅ Smart budget recommendations
- ✅ Savings opportunities

### 🎨 Beautiful UI
- ✅ Modern, responsive design with Tailwind CSS
- ✅ Intuitive navigation
- ✅ Interactive dashboards
- ✅ Real-time data visualization

---

## 🛠️ Tech Stack

### Backend
- **Flask 3.0.0** - Python web framework
- **Google Gemini AI** - AI predictions and analysis
- **Pandas 2.1.4** - Data manipulation
- **NumPy 1.26.2** - Numerical computations
- **Flask-CORS** - Cross-origin support

### Frontend
- **React 19** - UI library
- **Vite 7** - Build tool
- **Tailwind CSS 4** - Styling
- **Modern ES6+** - JavaScript

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### 1. Clone the Repository
```bash
cd ExpenseForecaster
```

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file
# Add your Gemini API key (get free at https://makersuite.google.com/app/apikey)
# Copy .env.example to .env and add:
GEMINI_API_KEY=your_api_key_here
DEBUG=True
HOST=0.0.0.0
PORT=5000

# Run the backend server
python app.py
```

The backend will start at **http://localhost:5000**

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start at **http://localhost:5173**

---

## 🚀 Usage

### 1. **Open the Application**
Navigate to http://localhost:5173 in your browser

### 2. **Generate Sample Data** (Optional)
Click the "Generate Sample Data" button to create 100 test expenses

### 3. **Explore Features**
- **Dashboard**: View overview and statistics
- **Expenses**: Add, edit, view your expenses
- **Predictions**: Get AI-powered expense forecasts
- **Analytics**: Deep insights and recommendations

### 4. **Add Your Own Expenses**
- Go to "Expenses" tab
- Click "Add Expense"
- Fill in the form and submit

### 5. **Get AI Predictions**
- Go to "Predictions" tab
- Select period (month/quarter) and number of periods
- Click "Predict" to see AI-generated forecasts

### 6. **View Analytics**
- Go to "Analytics" tab
- Click "Analyze Expenses" for AI insights
- Click "Get Recommendations" for budget tips

---

## 📁 Project Structure

```
ExpenseForecaster/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── ai_agent.py           # AI forecasting engine
│   ├── data_manager.py       # Data persistence
│   ├── config.py             # Configuration
│   ├── requirements.txt      # Python dependencies
│   ├── test_api.py          # API test suite
│   ├── quick_start.py       # Setup verification
│   ├── .env                 # Environment variables (create this!)
│   ├── .env.example         # Example environment file
│   └── data/
│       └── expenses.json    # Expense data storage
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Dashboard.jsx    # Dashboard component
    │   │   ├── Expenses.jsx     # Expense management
    │   │   ├── Predictions.jsx  # AI predictions
    │   │   └── Analytics.jsx    # Analytics & insights
    │   ├── services/
    │   │   └── api.js          # API service layer
    │   ├── App.jsx             # Main app component
    │   ├── main.jsx            # Entry point
    │   └── index.css           # Global styles
    ├── package.json            # npm dependencies
    ├── vite.config.js         # Vite configuration
    └── index.html             # HTML template
```

---

## 🔑 Getting Gemini API Key (FREE)

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Select "Create API key in new project"
5. Copy the generated key
6. Add to `backend/.env`:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```
7. Restart the backend server

---

## 🎯 API Endpoints

### Expense Management
- `GET /api/health` - Health check
- `GET /api/expenses` - Get all expenses
- `POST /api/expenses` - Add expense
- `POST /api/expenses/bulk` - Add multiple expenses
- `GET /api/expenses/<id>` - Get expense by ID
- `PUT /api/expenses/<id>` - Update expense
- `DELETE /api/expenses/<id>` - Delete expense
- `GET /api/expenses/categories` - Get categories
- `GET /api/expenses/statistics` - Get statistics

### AI Features
- `POST /api/ai/analyze` - Analyze expenses
- `POST /api/ai/predict` - Predict future expenses
- `POST /api/ai/recommendations` - Get recommendations

### Utilities
- `POST /api/utils/generate-sample-data` - Generate test data
- `DELETE /api/utils/clear-data` - Clear all data

---

## 📊 Sample API Requests

### Add an Expense
```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-05",
    "category": "Food",
    "amount": 45.99,
    "description": "Groceries"
  }'
```

### Get Prediction
```bash
curl -X POST http://localhost:5000/api/ai/predict \
  -H "Content-Type: application/json" \
  -d '{
    "period": "month",
    "periods": 1
  }'
```

### Analyze Expenses
```bash
curl -X POST http://localhost:5000/api/ai/analyze
```

---

## 🎨 Features Showcase

### Dashboard
- Real-time statistics cards
- Quick action buttons
- Date range visualization
- Responsive layout

### Expenses View
- Sortable, filterable table
- Category badges
- Inline editing
- Search functionality

### AI Predictions
- Interactive prediction form
- Category breakdown
- Confidence indicators
- Risk factor warnings

### Analytics
- Spending visualizations
- AI-powered insights
- Budget recommendations
- Savings opportunities

---

## 🐛 Troubleshooting

### Backend won't start
- Check if Python 3.11+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check if port 5000 is available

### Frontend won't start
- Check if Node.js is installed: `node --version`
- Install dependencies: `npm install`
- Check if port 5173 is available

### AI features not working
- Make sure GEMINI_API_KEY is set in `backend/.env`
- Restart the backend server after adding the key
- Check if you have internet connection (API requires network)

### CORS errors
- Make sure backend is running on port 5000
- Check if Flask-CORS is installed
- Verify API_BASE_URL in `frontend/src/services/api.js`

---

## 📝 Testing

### Backend Testing
```bash
cd backend
python test_api.py
```

### Quick Start Check
```bash
cd backend
python quick_start.py
```

---

## 🚀 Production Deployment

### Backend
```bash
# Install production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🤝 Contributing

This is a learning project. Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Share improvements

---

## 📄 License

This project is open source and available for educational purposes.

---

## 🎉 Acknowledgments

- **Google Gemini AI** for powerful AI predictions
- **Tailwind CSS** for beautiful styling
- **React & Vite** for fast development
- **Flask** for robust backend

---

## 📧 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify all dependencies are installed
3. Ensure API key is configured correctly
4. Check console logs for errors

---

## 🌟 Future Enhancements

- [ ] Export data to CSV/Excel
- [ ] Data visualization charts
- [ ] Multiple user accounts
- [ ] Email notifications
- [ ] Mobile app
- [ ] Dark mode
- [ ] Budget alerts
- [ ] Receipt scanning

---

**Built with ❤️ using AI-powered technology**

🔗 Frontend: http://localhost:5173
🔗 Backend: http://localhost:5000
🔗 API Docs: http://localhost:5000/api/health
