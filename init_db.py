import sqlite3

def create_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Drop the table if it exists to avoid conflicts (optional)
    cursor.execute('DROP TABLE IF EXISTS users')

    # Create the users table with 'hashed_password' instead of 'password'
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        hashed_password TEXT,  -- Renaming this to hashed_password
                        user_type TEXT)''')
    
    # Drop and recreate jobs and applications tables if necessary
    cursor.execute('DROP TABLE IF EXISTS jobs')
    cursor.execute('DROP TABLE IF EXISTS applications')

    # Create the jobs table
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        description TEXT,
                        recruiter_username TEXT)''')

    # Create the applications table
    cursor.execute('''CREATE TABLE IF NOT EXISTS applications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        candidate_username TEXT,
                        job_id INTEGER,
                        FOREIGN KEY(job_id) REFERENCES jobs(id))''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
    print("Database and tables created successfully.")  