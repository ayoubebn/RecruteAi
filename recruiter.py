from flask import render_template, request, redirect, url_for, session
from db import add_job_offer, get_job_offers_by_recruiter

def recruiter_dashboard():
    if 'username' not in session or session['user_type'] != 'recruiter':
        return redirect(url_for('login', user_type='recruiter'))
    
    job_offers = get_job_offers_by_recruiter(session['username'])
    return render_template('recruiter_dashboard.html', job_offers=job_offers)

def create_offer():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        skills_required = request.form['skills_required']
        recruiter_id = session['username']  # Utiliser l'ID du recruteur connecté
        add_job_offer(title, description, skills_required, recruiter_id)
        return redirect(url_for('recruiter_dashboard_route'))
    
    return render_template('create_offer.html')
