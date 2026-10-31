import sqlite3

DB_NAME = "kamove.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pickup TEXT NOT NULL,
            destination TEXT NOT NULL,
            passengers INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            current_location TEXT NOT NULL,
            heading_to TEXT
        )
    """)

    connection.commit()
    connection.close()


def add_request(pickup, destination, passengers):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO requests (pickup, destination, passengers)
        VALUES (?, ?, ?)
    """, (pickup, destination, passengers))

    connection.commit()
    connection.close()