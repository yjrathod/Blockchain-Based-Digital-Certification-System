import sqlite3
from datetime import datetime
import os

def create_database():
    """Create the SQLite database and tables"""
    
    # Create database file
    db_path = 'certificates.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create participants table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS participants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        organization TEXT,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create certificates table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        participant_id INTEGER,
        certificate_type TEXT NOT NULL,
        pdf_path TEXT NOT NULL,
        email_subject TEXT,
        email_body TEXT,
        sent_at TIMESTAMP,
        email_status TEXT DEFAULT 'pending',
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (participant_id) REFERENCES participants (id)
    )
    ''')
    
    # Create certificates folder if it doesn't exist
    if not os.path.exists('certificates'):
        os.makedirs('certificates')
        print("Created 'certificates' folder for PDF files")
    
    conn.commit()
    conn.close()
    
    print("✅ Database 'certificates.db' created successfully!")
    print("✅ Tables 'participants' and 'certificates' created!")

if __name__ == "__main__":
    create_database()