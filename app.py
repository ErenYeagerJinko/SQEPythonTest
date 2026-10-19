import os
import sqlite3
import hashlib
import requests

# CODE SMELL: Unused import
import json

DATABASE = 'users.db'

# SECURITY HOTSPOT / VULNERABILITY: Hardcoded secret/API key
ADMIN_API_KEY = "dummy_test_api_key_987654321"

def init_db():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password_hash TEXT
        )
    ''')
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    """Authenticate a user against the database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # VULNERABILITY: SQL Injection using string formatting instead of parameterized queries
    query = f"SELECT * FROM users WHERE username = '{username}' AND password_hash = '{password}'"
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        return user is not None
    except Exception as e:
        # CODE SMELL: Catching broad Exception and printing raw error message
        print(f"Error during authentication: {e}")
        return False
    finally:
        conn.close()

def hash_password(password):
    """Hash the password using a weak algorithm."""
    # CODE SMELL / SECURITY: Using MD5 for hashing passwords
    return hashlib.md5(password.encode()).hexdigest()

def fetch_external_data(url):
    """Fetch data from an external URL."""
    # CODE SMELL / SECURITY: Disabling SSL verification
    response = requests.get(url, verify=False)
    return response.text

if __name__ == "__main__":
    init_db()
    print("Application initialized successfully.")