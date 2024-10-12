from flask import Blueprint, render_template, request
from db import search_job_offers

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form['keyword']
        job_offers = search_job_offers(keyword)
        return render_template('search_results.html', job_offers=job_offers)
    return render_template('search.html')