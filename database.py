import sqlite3
import bcrypt
import os

DB_NAME = 'password_vault.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Zero Plaintext Policy enforced. Only bcrypt hashes stored.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def check_duplicate_and_store(password: str) -> bool:
    """
    Checks if a password matches any previously used password.
    If it's a duplicate, returns True and aborts submission.
    If not, hashes the password with bcrypt and stores it, returning False.
    """
    password_bytes = password.encode('utf-8')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Retrieve all historical hashes
    cursor.execute('SELECT hash FROM password_history')
    records = cursor.fetchall()
    
    for row in records:
        stored_hash = row[0].encode('utf-8')
        try:
            # Secure comparison using bcrypt
            if bcrypt.checkpw(password_bytes, stored_hash):
                conn.close()
                return True
        except ValueError:
            pass # Ignore invalid hashes
            
    # Hash and salt workflow with bcrypt
    salt = bcrypt.gensalt(rounds=12) # Optimal work factor
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    cursor.execute('INSERT INTO password_history (hash) VALUES (?)', (hashed.decode('utf-8'),))
    conn.commit()
    conn.close()
    
    return False
