import os
import sqlite3
import pymysql
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash
from config import Config

def get_connection():
    """Returns an active database connection based on config (MySQL or SQLite)."""
    if Config.DB_TYPE == 'mysql':
        try:
            # Common cloud MySQL options (TiDB, Aiven, etc. require SSL)
            connect_kwargs = {
                'host': Config.MYSQL_HOST,
                'port': Config.MYSQL_PORT,
                'user': Config.MYSQL_USER,
                'password': Config.MYSQL_PASSWORD,
                'database': Config.MYSQL_DB,
                'cursorclass': DictCursor,
                'autocommit': True,
                'connect_timeout': 10
            }
            
            # Enable SSL if connecting to cloud provider (e.g., TiDB Cloud, Aiven)
            if Config.MYSQL_HOST not in ('localhost', '127.0.0.1', 'db'):
                connect_kwargs['ssl'] = {'ssl_mode': 'REQUIRED'}

            conn = pymysql.connect(**connect_kwargs)
            return conn, 'mysql'
        except Exception as e:
            # Fallback without SSL if SSL was rejected, else fall back to SQLite
            try:
                connect_kwargs.pop('ssl', None)
                conn = pymysql.connect(**connect_kwargs)
                return conn, 'mysql'
            except Exception as e2:
                print(f"[Database Warning] Cloud MySQL connection failed ({e2}). Using local SQLite.")

    # SQLite fallback
    conn = sqlite3.connect(Config.SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn, 'sqlite'

def query_db(query, args=(), one=False):
    """Executes a SELECT query and returns list of dictionaries (or a single dict)."""
    conn, engine = get_connection()
    try:
        if engine == 'sqlite':
            formatted_query = query.replace('%s', '?')
            cur = conn.cursor()
            cur.execute(formatted_query, args)
            rv = cur.fetchall()
            cur.close()
            result = [dict(row) for row in rv]
            return (result[0] if result else None) if one else result
        else:
            with conn.cursor() as cur:
                formatted_query = query.replace('?', '%s')
                cur.execute(formatted_query, args)
                rv = cur.fetchall()
                return (rv[0] if rv else None) if one else rv
    finally:
        conn.close()

def execute_db(query, args=(), commit=True):
    """Executes an INSERT, UPDATE, or DELETE query and returns the last inserted row id."""
    conn, engine = get_connection()
    try:
        if engine == 'sqlite':
            formatted_query = query.replace('%s', '?')
            cur = conn.cursor()
            cur.execute(formatted_query, args)
            if commit:
                conn.commit()
            last_id = cur.lastrowid
            cur.close()
            return last_id
        else:
            with conn.cursor() as cur:
                formatted_query = query.replace('?', '%s')
                cur.execute(formatted_query, args)
                if commit:
                    conn.commit()
                last_id = cur.lastrowid
                return last_id
    finally:
        conn.close()

def init_db():
    """Initializes schema tables and default admin if not existing."""
    conn, engine = get_connection()
    try:
        if engine == 'sqlite':
            cur = conn.cursor()
            cur.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'teacher',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NULL,
                roll_no TEXT NOT NULL UNIQUE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                dob DATE NULL,
                gender TEXT DEFAULT 'Male',
                course TEXT NOT NULL,
                semester INTEGER NOT NULL,
                contact_number TEXT NULL,
                email TEXT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_code TEXT NOT NULL UNIQUE,
                subject_name TEXT NOT NULL,
                credits INTEGER NOT NULL DEFAULT 3,
                course TEXT NOT NULL,
                semester INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS marks (
                mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,
                exam_type TEXT NOT NULL DEFAULT 'Semester Exam',
                marks_obtained REAL NOT NULL,
                max_marks REAL NOT NULL DEFAULT 100.0,
                grade TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
                UNIQUE (student_id, subject_id, exam_type)
            );

            CREATE TABLE IF NOT EXISTS reports (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                report_type TEXT NOT NULL,
                generated_by TEXT NOT NULL,
                file_path TEXT NULL,
                generated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS notifications (
                notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NULL,
                student_id INTEGER NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            conn.commit()
            cur.close()
        else:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) NOT NULL UNIQUE,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL DEFAULT 'teacher',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    student_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NULL,
                    roll_no VARCHAR(20) NOT NULL UNIQUE,
                    first_name VARCHAR(50) NOT NULL,
                    last_name VARCHAR(50) NOT NULL,
                    dob DATE NULL,
                    gender VARCHAR(10) DEFAULT 'Male',
                    course VARCHAR(50) NOT NULL,
                    semester INT NOT NULL,
                    contact_number VARCHAR(20) NULL,
                    email VARCHAR(100) NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    subject_id INT AUTO_INCREMENT PRIMARY KEY,
                    subject_code VARCHAR(20) NOT NULL UNIQUE,
                    subject_name VARCHAR(100) NOT NULL,
                    credits INT NOT NULL DEFAULT 3,
                    course VARCHAR(50) NOT NULL,
                    semester INT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS marks (
                    mark_id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    subject_id INT NOT NULL,
                    exam_type VARCHAR(50) NOT NULL DEFAULT 'Semester Exam',
                    marks_obtained DECIMAL(5,2) NOT NULL,
                    max_marks DECIMAL(5,2) NOT NULL DEFAULT 100.00,
                    grade VARCHAR(5) NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT uq_student_sub UNIQUE (student_id, subject_id, exam_type)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    report_id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT NOT NULL,
                    report_type VARCHAR(50) NOT NULL,
                    generated_by VARCHAR(50) NOT NULL,
                    file_path VARCHAR(255) NULL,
                    generated_date DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS notifications (
                    notification_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NULL,
                    student_id INT NULL,
                    message VARCHAR(255) NOT NULL,
                    type VARCHAR(30) DEFAULT 'info',
                    is_read TINYINT(1) DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                conn.commit()

        # Seed default admin if user table is empty
        admin_check = query_db("SELECT * FROM users WHERE username = 'admin'", one=True)
        if not admin_check:
            pwd_hash = generate_password_hash('admin123')
            execute_db(
                "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)",
                ('admin', 'admin@smartanalyzer.edu', pwd_hash, 'admin')
            )
            print("[Database] Default admin account (admin / admin123) initialized.")
    finally:
        conn.close()
