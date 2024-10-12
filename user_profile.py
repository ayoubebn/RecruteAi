from flask import Blueprint, render_template, request, redirect, url_for, session
from db import get_user_profile, update_user_profile

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Update user profile logic
        profile_data = {
            'fullname': request.form['fullname'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'skills': request.form['skills'],
            'experience': request.form['experience']
        }
        update_user_profile(session['username'], profile_data)
        return redirect(url_for('profile'))

    user_profile = get_user_profile(session['username'])
    return render_template('profile.html', profile=user_profile)
