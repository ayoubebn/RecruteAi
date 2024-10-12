from flask import Blueprint, render_template, session
from db import get_notifications

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications')
def notifications():
    if 'username' not in session:
        return redirect(url_for('login'))

    notifications = get_notifications(session['username'])
    return render_template('notifications.html', notifications=notifications)
