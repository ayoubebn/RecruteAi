from flask import render_template, request, redirect, url_for, session
from db import get_all_job_offers, add_application
import os

def candidate_dashboard():
    if 'username' not in session or session['user_type'] != 'candidate':
        return redirect(url_for('login', user_type='candidate'))
    
    job_offers = get_all_job_offers()
    return render_template('candidate_dashboard.html', job_offers=job_offers)

def apply(job_offer_id):
    if request.method == 'POST':
        # Télécharger le CV
        cv_file = request.files['cv']
        cv_path = os.path.join('static/cvs', cv_file.filename)
        cv_file.save(cv_path)

        # Ajouter la candidature à la base de données
        candidate_id = session['username']  # Utiliser l'ID du candidat connecté
        add_application(candidate_id, job_offer_id, cv_path)
        return redirect(url_for('candidate_dashboard_route'))
    
    return render_template('apply.html', job_offer_id=job_offer_id)