import sqlite3
import pandas as pd
import os

# التأكد من وجود مجلد البيانات
DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "mishkat_sovereign.db")

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # جدول المسارات الوجودية
    c.execute('''CREATE TABLE IF NOT EXISTS sessions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                 title TEXT, 
                 content TEXT, 
                 phase TEXT)''')
    conn.commit()
    conn.close()

def save_session(title, content, phase):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO sessions (title, content, phase) VALUES (?, ?, ?)", 
              (title, content, phase))
    conn.commit()
    conn.close()

def get_all_sessions():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM sessions ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def delete_session(session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE id=?", (session_id,))
    conn.commit()
    conn.close()
