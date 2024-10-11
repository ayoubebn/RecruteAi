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
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND user_type = ?', (username, user_type))
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

def add_application(candidate_id, job_offer_id, cv_path):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO applications (candidate_id, job_offer_id, cv_path) VALUES (?, ?, ?)', 
                   (candidate_id, job_offer_id, cv_path))
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

def add_user(username, password, user_type):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # Change 'password' to 'hashed_password' to match the database schema
    cursor.execute('INSERT INTO users (username, hashed_password, user_type) VALUES (?, ?, ?)', 
                   (username, password, user_type))

    conn.commit()
    conn.close()

def add_job_offer(title, description, skills_required, recruiter_id):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO job_offers (title, description, skills_required, recruiter_id) VALUES (?, ?, ?, ?)', 
                   (title, description, skills_required, recruiter_id))
    conn.commit()
    conn.close()

def get_job_offers_by_recruiter(recruiter_username):
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM job_offers WHERE recruiter_id = (SELECT id FROM users WHERE username = ?)', (recruiter_username,))
    job_offers = cursor.fetchall()
    conn.close()
    return job_offers

def get_all_job_offers():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM job_offers')
    job_offers = cursor.fetchall()
    conn.close()
    return job_offers