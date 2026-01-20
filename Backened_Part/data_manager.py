import json
import os
from datetime import datetime
from config import Config

class DataManager:
    """Manages expense data storage and retrieval"""
    
    def __init__(self):
        """Initialize data manager"""
        Config.init_app()
        self.data_file = os.path.join(Config.DATA_FOLDER, 'expenses.json')
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize the storage file if it doesn't exist"""
        if not os.path.exists(self.data_file):
            self._save_data([])
    
    def _save_data(self, data):
        """Save data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_data(self):
        """Load data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def add_expense(self, expense_data):
        """
        Add a new expense record
        
        Args:
            expense_data: dict with keys: date, category, amount, description
        
        Returns:
            dict: Added expense with generated ID
        """
        expenses = self._load_data()
        
        # Generate ID
        expense_id = max([e.get('id', 0) for e in expenses], default=0) + 1
        
        # Validate and format expense
        expense = {
            'id': expense_id,
            'date': expense_data.get('date', datetime.now().strftime('%Y-%m-%d')),
            'category': expense_data.get('category', 'Uncategorized'),
            'amount': float(expense_data.get('amount', 0)),
            'description': expense_data.get('description', ''),
            'created_at': datetime.now().isoformat()
        }
        
        expenses.append(expense)
        self._save_data(expenses)
        
        return expense
    
    def add_bulk_expenses(self, expense_list):
        """
        Add multiple expenses at once
        
        Args:
            expense_list: List of expense dictionaries
        
        Returns:
            dict: Summary of added expenses
        """
        added_expenses = []
        
        for expense_data in expense_list:
            try:
                expense = self.add_expense(expense_data)
                added_expenses.append(expense)
            except Exception as e:
                print(f"Error adding expense: {e}")
        
        return {
            'success': True,
            'count': len(added_expenses),
            'expenses': added_expenses
        }
    
    def get_all_expenses(self):
        """Get all expense records"""
        return self._load_data()
    
    def get_expense_by_id(self, expense_id):
        """Get a specific expense by ID"""
        expenses = self._load_data()
        for expense in expenses:
            if expense.get('id') == expense_id:
                return expense
        return None
    
    def get_expenses_by_date_range(self, start_date, end_date):
        """Get expenses within a date range"""
        expenses = self._load_data()
        filtered = []
        
        for expense in expenses:
            expense_date = datetime.strptime(expense['date'], '%Y-%m-%d')
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            if start <= expense_date <= end:
                filtered.append(expense)
        
        return filtered
    
    def get_expenses_by_category(self, category):
        """Get all expenses for a specific category"""
        expenses = self._load_data()
        return [e for e in expenses if e.get('category') == category]
    
    def update_expense(self, expense_id, updated_data):
        """Update an existing expense"""
        expenses = self._load_data()
        
        for i, expense in enumerate(expenses):
            if expense.get('id') == expense_id:
                # Update fields
                expense.update({
                    'date': updated_data.get('date', expense['date']),
                    'category': updated_data.get('category', expense['category']),
                    'amount': float(updated_data.get('amount', expense['amount'])),
                    'description': updated_data.get('description', expense['description']),
                    'updated_at': datetime.now().isoformat()
                })
                expenses[i] = expense
                self._save_data(expenses)
                return expense
        
        return None
    
    def delete_expense(self, expense_id):
        """Delete an expense by ID"""
        expenses = self._load_data()
        original_length = len(expenses)
        
        expenses = [e for e in expenses if e.get('id') != expense_id]
        
        if len(expenses) < original_length:
            self._save_data(expenses)
            return True
        
        return False
    
    def clear_all_expenses(self):
        """Clear all expense data"""
        self._save_data([])
        return True
    
    def get_categories(self):
        """Get list of all unique categories"""
        expenses = self._load_data()
        categories = set([e.get('category') for e in expenses if e.get('category')])
        return sorted(list(categories))
    
    def get_statistics(self):
        """Get basic statistics about expenses"""
        expenses = self._load_data()
        
        if not expenses:
            return {
                'total_expenses': 0,
                'count': 0,
                'categories': 0,
                'date_range': None
            }
        
        total = sum([e.get('amount', 0) for e in expenses])
        dates = [e.get('date') for e in expenses if e.get('date')]
        
        return {
            'total_expenses': total,
            'count': len(expenses),
            'categories': len(self.get_categories()),
            'date_range': {
                'start': min(dates) if dates else None,
                'end': max(dates) if dates else None
            }
        }
