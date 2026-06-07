import sqlite3

conn = sqlite3.connect(
    "database.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS moods(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS journal(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


def save_mood(mood):
    cursor.execute(
        "INSERT INTO moods(mood) VALUES(?)",
        (mood,)
    )
    conn.commit()


def save_journal(text):
    cursor.execute(
        "INSERT INTO journal(content) VALUES(?)",
        (text,)
    )
    conn.commit()


def get_moods():
    cursor.execute("SELECT mood FROM moods")
    return cursor.fetchall()
