import sqlite3

try:
    conn = sqlite3.connect('data/uber_eats_sl.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:", [t[0] for t in tables])
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
        count = cursor.fetchone()[0]
        print(f"  {table[0]}: {count} rows")
    
    conn.close()
except Exception as e:
    print(f"Error: {e}")
