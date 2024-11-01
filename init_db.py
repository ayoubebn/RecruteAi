# init_db.py
import sqlite3

def create_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        hashed_password TEXT,
                        user_type TEXT)''')

    cursor.execute('DROP TABLE IF EXISTS job_offers')
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_offers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        description TEXT,
                        skills_required TEXT,
                        recruiter_username TEXT,
                        FOREIGN KEY(recruiter_username) REFERENCES users(username))''')

    cursor.execute('DROP TABLE IF EXISTS applications')
    cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        candidate_username TEXT,
                        job_id INTEGER,
                        cv_path TEXT,
                        FOREIGN KEY(candidate_username) REFERENCES users(username),
                        FOREIGN KEY(job_id) REFERENCES job_offers(id))''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    print("Database and tables created successfully.")
