from functools import wraps
from Author import Author
from flask import redirect, url_for


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not Author.is_logged():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
