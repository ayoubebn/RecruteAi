from flask import render_template, request, session
from db import get_jobs, add_job, get_applications

def recruiter_dashboard():
    if request.method == 'POST':
        job_title = request.form['job_title']
        job_description = request.form['job_description']
        add_job(job_title, job_description, session['username'])
    jobs = get_jobs(session['username'])
    applications = get_applications(session['username'])
    return render_template('recruiter_dashboard.html', jobs=jobs, applications=applications)
