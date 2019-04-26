from functools import wraps
from flask import request, Response, redirect, session, url_for


def check_auth():
    #username, password
    """This function is called to check if a username /
    password combination is valid.
    """
    return 'username' in session

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return redirect(url_for('login'))
    # return Response(
    # 'Could not verify your access level for that URL.\n'
    # 'You have to login with proper credentials', 401,
    # {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        # if not auth or not check_auth(auth.username, auth.password):
        if not check_auth():
            return authenticate()
        return f(*args, **kwargs)
    return decorated
