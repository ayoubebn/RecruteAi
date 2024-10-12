from flask import render_template, request, redirect, url_for, session
from db import add_user, check_user, get_job_offer_by_id, add_application, add_job
from utils import hash_password, verify_password, save_cv
import logging

logging.basicConfig(level=logging.DEBUG)

def candidate_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = check_user(username, 'candidate')

        logging.debug(f"User: {user}")
        logging.debug(f"Password: {password}")

        if user and verify_password(password, user['hashed_password']):
            session['username'] = username
            session['user_type'] = 'candidate'
            return redirect(url_for('candidate_dashboard_route'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

def recruiter_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = check_user(username, 'recruiter')

        logging.debug(f"User: {user}")
        logging.debug(f"Password: {password}")

        if user and verify_password(password, user['hashed_password']):
            session['username'] = username
            session['user_type'] = 'recruiter'
            return redirect(url_for('recruiter_dashboard_route'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

def candidate_register():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])

        # Vérifier si le nom d'utilisateur existe déjà
        existing_user = check_user(username, 'candidate')
        if existing_user:
            return render_template('register.html', error="Username already exists")

        # Si l'utilisateur n'existe pas, l'ajouter
        add_user(username, password, 'candidate')
        return redirect(url_for('login', user_type='candidate'))
    return render_template('register.html')

def recruiter_register():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])

        # Vérifier si le nom d'utilisateur existe déjà
        existing_user = check_user(username, 'recruiter')
        if existing_user:
            return render_template('register.html', error="Username already exists")

        # Si l'utilisateur n'existe pas, l'ajouter
        add_user(username, password, 'recruiter')
        return redirect(url_for('login', user_type='recruiter'))
    return render_template('register.html')


def apply(job_offer_id):
    if 'username' not in session or session['user_type'] != 'candidate':
        return redirect(url_for('login', user_type='candidate'))

    job_offer = get_job_offer_by_id(job_offer_id)
    
    if request.method == 'POST':
        # Récupérer les informations du formulaire
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        skills = request.form['skills']
        
        # Enregistrer le CV si attaché
        cv_file = request.files['cv']
        cv_path = save_cv(cv_file)
        
        # Ajouter la candidature
        add_application(session['username'], job_offer_id, fullname, email, phone, skills, cv_path)
        
        return redirect(url_for('candidate_dashboard_route'))

    return render_template('apply_to_job.html', job_offer=job_offer)

def create_offer():
    if 'username' not in session or session['user_type'] != 'recruiter':
        return redirect(url_for('login', user_type='recruiter'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        required_skills = request.form['required_skills']

        # Ajouter l'offre d'emploi à la base de données
        add_job(session['username'], title, description, required_skills)

        return redirect(url_for('recruiter_dashboard_route'))

    return render_template('create_offer.html')