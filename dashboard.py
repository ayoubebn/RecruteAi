from flask import Blueprint, render_template, session, redirect, url_for
from db import get_candidate_dashboard_data, get_recruiter_dashboard_data
from auth import login


dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if session['user_type'] == 'candidate':
        data = get_candidate_dashboard_data(session['username'])
        return render_template('candidate_dashboard.html', data=data)
    elif session['user_type'] == 'recruiter':
        data = get_recruiter_dashboard_data(session['username'])
        return render_template('recruiter_dashboard.html', data=data)