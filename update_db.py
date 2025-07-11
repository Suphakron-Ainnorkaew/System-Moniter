import sqlite3

def update_database():
    db_name = "system_monitor.db"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # เพิ่มคอลัมน์ core_mode ถ้ายังไม่มี
    try:
        cursor.execute("ALTER TABLE test_results ADD COLUMN core_mode TEXT DEFAULT 'all'")
        print("Added core_mode column to test_results table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column core_mode already exists")
        else:
            raise e
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_database()