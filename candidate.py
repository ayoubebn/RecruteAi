from flask import render_template, request, session, redirect, url_for
from db import get_jobs, add_application

def candidate_dashboard():
    jobs = get_jobs()
    if request.method == 'POST':
        job_id = request.form['job_id']
        add_application(session['username'], job_id)
        return redirect(url_for('candidate_dashboard_route'))
    return render_template('candidate_dashboard.html', jobs=jobs)
