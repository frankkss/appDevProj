from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You are not authorized to access this page.', 'danger')
            return redirect(url_for('home_page'))  # Redirect to a safe page
        return f(*args, **kwargs)
    return decorated_function