from flask import render_template, request, redirect, url_for, session
from db import get_all_job_offers, add_application, get_job_offer_by_id
import os

def candidate_dashboard():
    if 'username' not in session or session['user_type'] != 'candidate':
        return redirect(url_for('login', user_type='candidate'))
    
    job_offers = get_all_job_offers()
    return render_template('candidate_dashboard.html', job_offers=job_offers)

def apply(job_offer_id):
    if 'username' not in session or session['user_type'] != 'candidate':
        return redirect(url_for('login', user_type='candidate'))

    if request.method == 'POST':
        # Récupérer les informations du formulaire
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        skills = request.form['skills']
        
        cv_file = request.files['cv']
        cv_path = os.path.join('static/cvs', cv_file.filename)
        cv_file.save(cv_path)
        
        add_application(session['username'], job_offer_id, fullname, email, phone, skills, cv_path)
        
        return redirect(url_for('candidate.candidate_dashboard'))
    
    
    job_offer = get_job_offer_by_id(job_offer_id)
    return render_template('apply.html', job_offer=job_offer)
