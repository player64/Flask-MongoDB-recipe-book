from flask import Flask, session, request, render_template, redirect, url_for
from requires_auth import requires_auth


app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/')
@requires_auth
def index():
    return 'Secret'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)