import sqlite3

conn = any
cursor = any


class SQLiteCRUD:
    def __init__(db_name):
        global conn
        conn = sqlite3.connect('my_database.db')
        global cursor
        cursor = conn.cursor()
        
        # Example table creation for 'users'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        conn.commit()

    def create_user(self, name, email):
        try:
            global cursor
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            return cursor.lastrowid # Return the ID of the newly inserted row
        except sqlite3.IntegrityError:
            print(f"Error: User with email '{email}' already exists.")
            return None
        
    def get_all_users():
        global cursor
        if cursor == any:
            SQLiteCRUD()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()

    def get_user_by_id( user_id):
        global cursor
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()
    
    def update_user_email(user_id, new_email):
        global cursor
        global conn
        cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
        conn.commit()
        return cursor.rowcount > 0 # True if a row was updated

    def delete_user(user_id):
        global cursor
        global conn
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0 # True if a row was deleted
    
    def close():
        global conn
        conn.close()