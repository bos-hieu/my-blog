from flask import session, flash, redirect, url_for
from functools import wraps #need to understand

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in') is None:
            flash('Error, Please log in first.')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function
