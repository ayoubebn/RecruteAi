from flask import Flask, render_template, redirect, url_for, session
from auth import candidate_login, recruiter_login, candidate_register, recruiter_register
from candidate import candidate_dashboard
from recruiter import recruiter_dashboard
from db import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize DB
init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login/<user_type>', methods=['GET', 'POST'])
def login(user_type):
    if user_type == 'candidate':
        return candidate_login()
    elif user_type == 'recruiter':
        return recruiter_login()

@app.route('/register/<user_type>', methods=['GET', 'POST'])
def register(user_type):
    if user_type == 'candidate':
        return candidate_register()
    elif user_type == 'recruiter':
        return recruiter_register()

@app.route('/candidate/dashboard')
def candidate_dashboard_route():
    return candidate_dashboard()

@app.route('/recruiter/dashboard')
def recruiter_dashboard_route():
    return recruiter_dashboard()

if __name__ == '__main__':
    app.run(debug=True)
