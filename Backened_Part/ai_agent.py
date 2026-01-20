import google.generativeai as genai
import pandas as pd
import json
from datetime import datetime, timedelta
from config import Config

class ExpenseForecastingAgent:
    """AI Agent for predicting expenses using Gemini API"""
    
    def __init__(self):
        """Initialize the AI agent with Gemini API"""
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def analyze_expenses(self, expense_data):
        """
        Analyze historical expense data and identify patterns
        
        Args:
            expense_data: List of expense records with date, category, and amount
        
        Returns:
            dict: Analysis results including trends and patterns
        """
        if not expense_data or len(expense_data) == 0:
            return {"error": "No expense data provided"}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(expense_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Prepare analysis prompt
        summary_stats = self._get_summary_statistics(df)
        
        prompt = f"""
You are an expert financial analyst AI agent. Analyze the following expense data and provide insights:

Expense Summary:
- Total Expenses: ${summary_stats['total']:.2f}
- Average Monthly Expense: ${summary_stats['avg_monthly']:.2f}
- Number of Transactions: {summary_stats['count']}
- Date Range: {summary_stats['start_date']} to {summary_stats['end_date']}

Category Breakdown:
{summary_stats['category_breakdown']}

Recent Transactions (Last 10):
{summary_stats['recent_transactions']}

Please analyze:
1. Spending patterns and trends
2. Seasonal variations if any
3. Category-wise insights
4. Any unusual spending patterns

Provide a concise analysis in JSON format with keys: trends, patterns, insights, anomalies.
"""
        
        try:
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            # Try to extract JSON from the response
            try:
                # Find JSON in the response
                json_start = analysis_text.find('{')
                json_end = analysis_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    analysis = json.loads(analysis_text[json_start:json_end])
                else:
                    analysis = {"analysis": analysis_text}
            except:
                analysis = {"analysis": analysis_text}
            
            analysis['summary_statistics'] = summary_stats
            return analysis
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def predict_expenses(self, expense_data, forecast_period='month', periods=1):
        """
        Predict future expenses using historical data and AI analysis
        
        Args:
            expense_data: List of expense records
            forecast_period: 'month' or 'quarter'
            periods: Number of periods to forecast
        
        Returns:
            dict: Predictions with breakdown by category
        """
        if not expense_data or len(expense_data) == 0:
            return {"error": "No expense data provided for prediction"}
        
        # Convert to DataFrame
        df = pd.DataFrame(expense_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Get summary statistics
        summary_stats = self._get_summary_statistics(df)
        
        # Calculate trends
        monthly_totals = df.groupby(df['date'].dt.to_period('M'))['amount'].sum()
        category_monthly = df.groupby([df['date'].dt.to_period('M'), 'category'])['amount'].sum()
        
        # Prepare prediction prompt
        prompt = f"""
You are an expert financial forecasting AI agent. Based on the historical expense data provided, predict future expenses.

Historical Data Summary:
- Time Period: {summary_stats['start_date']} to {summary_stats['end_date']}
- Total Expenses: ${summary_stats['total']:.2f}
- Average Monthly: ${summary_stats['avg_monthly']:.2f}
- Number of months: {summary_stats['months_count']}

Monthly Totals:
{monthly_totals.to_dict()}

Category Breakdown:
{summary_stats['category_breakdown']}

Seasonal Patterns:
{self._identify_seasonal_patterns(df)}

Task: Predict expenses for the next {periods} {forecast_period}(s).

Consider:
1. Historical trends (increasing/decreasing)
2. Seasonal variations (holidays, yearly cycles)
3. Category-specific patterns
4. Recent changes in spending

Provide predictions in JSON format with this structure:
{{
    "total_predicted": <total amount>,
    "period_type": "{forecast_period}",
    "periods": {periods},
    "category_predictions": {{
        "category_name": {{"amount": <value>, "confidence": <percentage>}}
    }},
    "reasoning": "<brief explanation of prediction logic>",
    "confidence_level": "<high/medium/low>",
    "risk_factors": ["factor1", "factor2"]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            prediction_text = response.text
            
            # Extract JSON from response
            try:
                json_start = prediction_text.find('{')
                json_end = prediction_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    predictions = json.loads(prediction_text[json_start:json_end])
                else:
                    # Fallback: create basic prediction
                    predictions = self._create_fallback_prediction(df, forecast_period, periods)
            except:
                predictions = self._create_fallback_prediction(df, forecast_period, periods)
            
            predictions['historical_average'] = summary_stats['avg_monthly']
            predictions['forecast_date'] = datetime.now().strftime('%Y-%m-%d')
            
            return predictions
            
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}
    
    def get_recommendations(self, expense_data, budget=None):
        """
        Get AI-powered recommendations for expense management
        
        Args:
            expense_data: List of expense records
            budget: Optional monthly budget limit
        
        Returns:
            dict: Recommendations for saving and optimization
        """
        if not expense_data or len(expense_data) == 0:
            return {"error": "No expense data provided"}
        
        df = pd.DataFrame(expense_data)
        df['date'] = pd.to_datetime(df['date'])
        
        summary_stats = self._get_summary_statistics(df)
        
        budget_context = f"Monthly Budget: ${budget:.2f}" if budget else "No budget specified"
        
        prompt = f"""
You are a personal finance advisor AI. Analyze the expense data and provide actionable recommendations.

Expense Summary:
- Average Monthly Expense: ${summary_stats['avg_monthly']:.2f}
- {budget_context}
- Total Categories: {len(summary_stats['category_totals'])}

Category Spending:
{summary_stats['category_breakdown']}

Provide recommendations in JSON format:
{{
    "savings_opportunities": [
        {{"category": "<category>", "current_spending": <amount>, "recommended_reduction": <amount>, "reason": "<explanation>"}}
    ],
    "budget_recommendations": {{
        "category_name": <recommended_amount>
    }},
    "action_items": ["item1", "item2"],
    "priority_areas": ["area1", "area2"]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            recommendations_text = response.text
            
            try:
                json_start = recommendations_text.find('{')
                json_end = recommendations_text.rfind('}') + 1
                if json_start != -1 and json_end > json_start:
                    recommendations = json.loads(recommendations_text[json_start:json_end])
                else:
                    recommendations = {"recommendations": recommendations_text}
            except:
                recommendations = {"recommendations": recommendations_text}
            
            return recommendations
            
        except Exception as e:
            return {"error": f"Recommendations generation failed: {str(e)}"}
    
    def _get_summary_statistics(self, df):
        """Calculate summary statistics from expense DataFrame"""
        total = df['amount'].sum()
        count = len(df)
        
        # Monthly statistics
        df['month'] = df['date'].dt.to_period('M')
        months = df['month'].nunique()
        avg_monthly = total / months if months > 0 else total
        
        # Category breakdown
        category_totals = df.groupby('category')['amount'].sum().to_dict()
        category_breakdown = "\n".join([f"- {cat}: ${amt:.2f}" for cat, amt in category_totals.items()])
        
        # Recent transactions
        recent = df.tail(10)[['date', 'category', 'amount', 'description']].to_string(index=False)
        
        return {
            'total': total,
            'count': count,
            'months_count': months,
            'avg_monthly': avg_monthly,
            'start_date': df['date'].min().strftime('%Y-%m-%d'),
            'end_date': df['date'].max().strftime('%Y-%m-%d'),
            'category_totals': category_totals,
            'category_breakdown': category_breakdown,
            'recent_transactions': recent
        }
    
    def _identify_seasonal_patterns(self, df):
        """Identify seasonal patterns in expenses"""
        df['month_num'] = df['date'].dt.month
        monthly_avg = df.groupby('month_num')['amount'].mean().to_dict()
        
        patterns = []
        month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                      7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        
        for month, avg in sorted(monthly_avg.items()):
            patterns.append(f"{month_names[month]}: ${avg:.2f}")
        
        return "\n".join(patterns) if patterns else "Not enough data for seasonal analysis"
    
    def _create_fallback_prediction(self, df, forecast_period, periods):
        """Create a simple fallback prediction based on averages"""
        avg_monthly = df['amount'].sum() / max(df['date'].dt.to_period('M').nunique(), 1)
        
        if forecast_period == 'quarter':
            predicted_total = avg_monthly * 3 * periods
        else:
            predicted_total = avg_monthly * periods
        
        category_predictions = {}
        category_totals = df.groupby('category')['amount'].sum()
        total = category_totals.sum()
        
        for category, amount in category_totals.items():
            percentage = amount / total if total > 0 else 0
            category_predictions[category] = {
                "amount": predicted_total * percentage,
                "confidence": "medium"
            }
        
        return {
            "total_predicted": predicted_total,
            "period_type": forecast_period,
            "periods": periods,
            "category_predictions": category_predictions,
            "reasoning": "Prediction based on historical averages and category distribution",
            "confidence_level": "medium",
            "risk_factors": ["Limited historical data", "Seasonal variations not accounted for"]
        }
