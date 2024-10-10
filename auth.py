from flask import render_template, request, redirect, url_for, session
from db import add_user, check_user
from utils import hash_password, verify_password

def candidate_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = check_user(username, 'candidate')

        if user and verify_password(password, user['password']):
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

        if user and verify_password(password, user['password']):
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
        add_user(username, password, 'candidate')
        return redirect(url_for('login', user_type='candidate'))
    return render_template('register.html')

def recruiter_register():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        add_user(username, password, 'recruiter')
        return redirect(url_for('login', user_type='recruiter'))
    return render_template('register.html')
