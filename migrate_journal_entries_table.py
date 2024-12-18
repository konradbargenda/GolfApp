import sqlite3

def migrate_journal_entries_table():
    conn = sqlite3.connect('golf_app.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise TEXT,
            time TEXT,
            points TEXT,
            notes TEXT,
            date TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    c.execute('''
        INSERT INTO journal_entries_new (id, notes, timestamp)
        SELECT id, entry, timestamp FROM journal_entries
    ''')

    c.execute('DROP TABLE journal_entries')

    c.execute('ALTER TABLE journal_entries_new RENAME TO journal_entries')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate_journal_entries_table()
