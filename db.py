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
        hashed_password TEXT,
        user_type TEXT
    )
    ''')

    # Create job_offers table with skills_required column
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS job_offers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        skills_required TEXT,
        recruiter_username TEXT,
        FOREIGN KEY(recruiter_username) REFERENCES users(username)
    )
    ''')

    # Create applications table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_username TEXT,
        job_id INTEGER,
        cv_path TEXT,
        FOREIGN KEY(candidate_username) REFERENCES users(username),
        FOREIGN KEY(job_id) REFERENCES job_offers(id)
    )
    ''')
    
    conn.commit()
    conn.close()

def add_user(username, hashed_password, user_type):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, hashed_password, user_type) VALUES (?, ?, ?)', (username, hashed_password, user_type))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
    finally:
        conn.close()

def check_user(username, user_type):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND user_type = ?', (username, user_type))
    user = cursor.fetchone()
    conn.close()
    
    # Assuming the `users` table columns are in the order: id, username, hashed_password, user_type
    if user:
        user_dict = {
            'id': user[0],
            'username': user[1],
            'hashed_password': user[2],
            'user_type': user[3]
        }
        return user_dict
    return None

def get_job_offers(recruiter_username=None):
    conn = connect_db()
    cursor = conn.cursor()
    if recruiter_username:
        cursor.execute('SELECT * FROM job_offers WHERE recruiter_username=?', (recruiter_username,))
    else:
        cursor.execute('SELECT * FROM job_offers')
    job_offers = cursor.fetchall()
    conn.close()
    return job_offers

def add_job(title, description, recruiter_username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO job_offers (title, description, recruiter_username) VALUES (?, ?, ?)', (title, description, recruiter_username))
    conn.commit()
    conn.close()

def add_application(candidate_username, job_id, cv_path):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO applications (candidate_username, job_id, cv_path) VALUES (?, ?, ?)', 
                   (candidate_username, job_id, cv_path))
    conn.commit()
    conn.close()

def get_applications(recruiter_username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT a.candidate_username, a.cv_path, j.title, j.description 
    FROM applications a 
    JOIN job_offers j ON a.job_id = j.id 
    WHERE j.recruiter_username=?
    ''', (recruiter_username,))
    applications = cursor.fetchall()
    conn.close()
    return applications

def add_job_offer(title, description, skills_required, recruiter_username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO job_offers (title, description, skills_required, recruiter_username) VALUES (?, ?, ?, ?)', 
                   (title, description, skills_required, recruiter_username))
    conn.commit()
    conn.close()

def get_job_offers_by_recruiter(recruiter_username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM job_offers WHERE recruiter_username = ?', (recruiter_username,))
    job_offers = cursor.fetchall()
    conn.close()
    return job_offers

def get_all_job_offers():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM job_offers')
    job_offers = cursor.fetchall()
    conn.close()
    return job_offers

def get_job_offer_by_id(job_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM job_offers WHERE id = ?', (job_id,))
    job_offer = cursor.fetchone()
    conn.close()
    return job_offer

def get_candidate_dashboard_data(candidate_username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT j.title, j.description, a.cv_path 
    FROM applications a 
    JOIN job_offers j ON a.job_id = j.id 
    WHERE a.candidate_username = ?
    ''', (candidate_username,))
    applications = cursor.fetchall()
    conn.close()
    return applications

def get_recruiter_dashboard_data(recruiter_username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT j.title, j.description, a.candidate_username, a.cv_path 
    FROM job_offers j 
    LEFT JOIN applications a ON j.id = a.job_id 
    WHERE j.recruiter_username = ?
    ''', (recruiter_username,))
    job_offers = cursor.fetchall()
    conn.close()
    return job_offers

def search_job_offers(keyword):
    conn = connect_db()
    cursor = conn.cursor()
    # Search for job offers where the title or description contains the keyword
    cursor.execute('''
    SELECT * FROM job_offers 
    WHERE title LIKE ? OR description LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%'))
    job_offers = cursor.fetchall()
    conn.close()
    return job_offers

def get_user_profile(username):
    conn = connect_db()
    cursor = conn.cursor()
    # Fetch user profile information based on username
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    # Convert result to a dictionary for easier access in the template
    if user:
        user_profile = {
            'id': user[0],
            'username': user[1],
            'hashed_password': user[2],
            'user_type': user[3],
            # Add other fields as needed if present in your schema
        }
        return user_profile
    return None

def update_user_profile(username, profile_data):
    conn = connect_db()
    cursor = conn.cursor()
    # Update user profile information in the users table
    cursor.execute('''
    UPDATE users
    SET fullname = ?, email = ?, phone = ?, skills = ?, experience = ?
    WHERE username = ?
    ''', (
        profile_data['fullname'],
        profile_data['email'],
        profile_data['phone'],
        profile_data['skills'],
        profile_data['experience'],
        username
    ))
    conn.commit()
    conn.close()
