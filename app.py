from flask import Flask, render_template, redirect, url_for
from dashboard import dashboard_bp
from recruiter import recruiter_bp
from search import search_bp
from user_profile import profile_bp
from auth import candidate_login, recruiter_login, candidate_register, recruiter_register
from candidate import candidate_dashboard, apply as candidate_apply
from db import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize DB
init_db()

# Register blueprints
app.register_blueprint(dashboard_bp)
app.register_blueprint(recruiter_bp, url_prefix='/recruiter')
app.register_blueprint(search_bp, url_prefix='/search')
app.register_blueprint(profile_bp, url_prefix='/profile')

@app.route('/')
def home():
    return render_template('home.html')

# Define login and register routes
@app.route('/login/<user_type>', methods=['GET', 'POST'])
def login(user_type):
    return candidate_login() if user_type == 'candidate' else recruiter_login()

@app.route('/register/<user_type>', methods=['GET', 'POST'])
def register(user_type):
    return candidate_register() if user_type == 'candidate' else recruiter_register()

@app.route('/candidate/dashboard')
def candidate_dashboard_route():
    return candidate_dashboard()

@app.route('/candidate/apply/<int:job_offer_id>', methods=['GET', 'POST'])
def apply_to_job(job_offer_id):
    return candidate_apply(job_offer_id)

if __name__ == '__main__':
    app.run(debug=True)
