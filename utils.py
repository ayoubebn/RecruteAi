# utils.py
import hashlib
import os
from werkzeug.utils import secure_filename

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(input_password, stored_password):
    return hash_password(input_password) == stored_password

def save_cv(cv_file):
    upload_folder = 'static/cvs'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = secure_filename(cv_file.filename)
    cv_path = os.path.join(upload_folder, filename)
    cv_file.save(cv_path)

    return cv_path
