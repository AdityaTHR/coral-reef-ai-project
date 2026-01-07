import sqlite3
import json
from datetime import datetime

class CoralDatabase:
    def __init__(self, db_name="coral_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Table for analysis results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coral_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                upload_date TEXT,
                coral_type TEXT,
                species_confidence REAL,
                health_status TEXT,
                health_confidence REAL,
                processing_time REAL
            )
        ''')
        
        self.conn.commit()
    
    def save_analysis(self, filename, coral_type, health_status, confidence):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO coral_analyses 
            (filename, upload_date, coral_type, health_status, species_confidence)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            filename,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            coral_type,
            health_status,
            confidence
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_analyses(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM coral_analyses ORDER BY upload_date DESC")
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()

# Test the database
if __name__ == "__main__":
    db = CoralDatabase()
    print("✅ Database created successfully!")
    print("📊 Table 'coral_analyses' is ready.")
    db.close()