"""
Quick Start - Expense Forecaster Backend
Run this script to verify everything is working
"""

import os
import sys

def check_dependencies():
    """Check if all required packages are installed"""
    print("Checking dependencies...")
    required = ['flask', 'flask_cors', 'google.generativeai', 'pandas', 'numpy', 'dotenv']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies installed\n")
    return True

def check_env_file():
    """Check if .env file exists and has API key"""
    print("Checking environment configuration...")
    
    if not os.path.exists('.env'):
        print("  ✗ .env file not found")
        print("  Creating .env file from template...")
        with open('.env.example', 'r') as src:
            with open('.env', 'w') as dst:
                dst.write(src.read())
        print("  ✓ .env file created")
    else:
        print("  ✓ .env file exists")
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("  ⚠ GEMINI_API_KEY not configured")
        print("  AI features will not work until you add your API key")
        print("  Get free key at: https://makersuite.google.com/app/apikey")
        print("")
        return False
    else:
        print(f"  ✓ GEMINI_API_KEY configured ({api_key[:10]}...)")
        return True

def check_data_folder():
    """Check if data folder exists"""
    print("\nChecking data storage...")
    
    if not os.path.exists('data'):
        os.makedirs('data')
        print("  ✓ data/ folder created")
    else:
        print("  ✓ data/ folder exists")
    
    if os.path.exists('data/expenses.json'):
        import json
        with open('data/expenses.json', 'r') as f:
            expenses = json.load(f)
        print(f"  ✓ Found {len(expenses)} expenses in database")
    else:
        print("  ℹ No expenses in database yet")
    
    return True

def main():
    """Run all checks"""
    print("=" * 60)
    print(" EXPENSE FORECASTER - QUICK START CHECK")
    print("=" * 60)
    print("")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    has_api_key = check_env_file()
    
    # Check data folder
    check_data_folder()
    
    print("\n" + "=" * 60)
    print(" STATUS SUMMARY")
    print("=" * 60)
    
    if has_api_key:
        print("✅ Backend is FULLY READY!")
        print("   All features including AI will work")
    else:
        print("⚠️  Backend is PARTIALLY READY")
        print("   Basic features work, AI features need API key")
    
    print("\n📝 TO START THE SERVER:")
    print("   python app.py")
    
    print("\n📝 TO TEST THE API:")
    print("   python test_api.py")
    
    if not has_api_key:
        print("\n📝 TO ENABLE AI FEATURES:")
        print("   1. Get free API key: https://makersuite.google.com/app/apikey")
        print("   2. Add to .env file: GEMINI_API_KEY=your_key_here")
        print("   3. Restart the server")
    
    print("\n" + "=" * 60)
    print("")

if __name__ == "__main__":
    main()
