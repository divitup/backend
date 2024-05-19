import sqlite3  # Assuming you are using sqlite

conn = sqlite3.connect('receipts.db', check_same_thread=False)
c = conn.cursor()

# Create the table
c.execute('''
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    s3_url TEXT,
    processed INTEGER,
    result TEXT
)
''')

conn.commit()
