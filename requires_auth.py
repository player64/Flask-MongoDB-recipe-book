from functools import wraps
from models.Author import AuthorModel
from flask import redirect, url_for


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not AuthorModel.is_logged():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
