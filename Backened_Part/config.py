import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Configuration class for the application"""
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Data storage
    DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'data')
    
    @staticmethod
    def init_app():
        """Initialize application directories"""
        os.makedirs(Config.DATA_FOLDER, exist_ok=True)
