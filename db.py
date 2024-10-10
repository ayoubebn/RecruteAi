import sqlite3

def connect_db():
    return sqlite3.connect('app.db')

def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        user_type TEXT
    )
    ''')

    # Create jobs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        recruiter_username TEXT
    )
    ''')

    # Create applications table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_username TEXT,
        job_id INTEGER,
        FOREIGN KEY(job_id) REFERENCES jobs(id)
    )
    ''')
    
    conn.commit()
    conn.close()

def add_user(username, password, user_type):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)', (username, password, user_type))
    conn.commit()
    conn.close()

def check_user(username, user_type):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND user_type=?', (username, user_type))
    user = cursor.fetchone()
    conn.close()
    return user

def get_jobs(recruiter_username=None):
    conn = connect_db()
    cursor = conn.cursor()
    if recruiter_username:
        cursor.execute('SELECT * FROM jobs WHERE recruiter_username=?', (recruiter_username,))
    else:
        cursor.execute('SELECT * FROM jobs')
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def add_job(title, description, recruiter_username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO jobs (title, description, recruiter_username) VALUES (?, ?, ?)', (title, description, recruiter_username))
    conn.commit()
    conn.close()

def add_application(candidate_username, job_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO applications (candidate_username, job_id) VALUES (?, ?)', (candidate_username, job_id))
    conn.commit()
    conn.close()

def get_applications(recruiter_username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT a.candidate_username, j.title 
    FROM applications a 
    JOIN jobs j ON a.job_id = j.id 
    WHERE j.recruiter_username=?
    ''', (recruiter_username,))
    applications = cursor.fetchall()
    conn.close()
    return applications
