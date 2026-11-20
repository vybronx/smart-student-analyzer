import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'smart-student-analyzer-production-key-2026')
    
    # Database Configuration: 'mysql' or 'sqlite'
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        DB_TYPE = 'mysql'
        # Parse URI: mysql://user:password@host:port/dbname
        parsed = urlparse(DATABASE_URL)
        MYSQL_USER = parsed.username or 'root'
        MYSQL_PASSWORD = parsed.password or ''
        MYSQL_HOST = parsed.hostname or 'localhost'
        MYSQL_PORT = parsed.port or 3306
        MYSQL_DB = parsed.path.lstrip('/') or 'smart_student_analyzer'
    else:
        DB_TYPE = os.getenv('DB_TYPE', 'sqlite').lower()
        MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
        MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
        MYSQL_USER = os.getenv('MYSQL_USER', 'root')
        MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
        MYSQL_DB = os.getenv('MYSQL_DB', 'smart_student_analyzer')
    
    # SQLite file path
    SQLITE_PATH = os.path.join(BASE_DIR, 'smart_student_analyzer.db')
