from flask import Blueprint, render_template, request, redirect, url_for, session
from db import add_job_offer, get_job_offers_by_recruiter

recruiter_bp = Blueprint('recruiter', __name__, url_prefix='/recruiter')

@recruiter_bp.route('/dashboard')
def dashboard():
    if 'username' not in session or session['user_type'] != 'recruiter':
        return redirect(url_for('auth.login', user_type='recruiter'))
    
    job_offers = get_job_offers_by_recruiter(session['username'])
    return render_template('recruiter_dashboard.html', job_offers=job_offers)

@recruiter_bp.route('/create_offer', methods=['GET', 'POST'])
def create_offer():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        skills_required = request.form['skills_required']
        recruiter_id = session['username']  # Utiliser l'ID du recruteur connecté
        add_job_offer(title, description, skills_required, recruiter_id)
        return redirect(url_for('recruiter.dashboard'))
    
    return render_template('create_offer.html')
