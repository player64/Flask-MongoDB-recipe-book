from flask import Flask, session, request, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
from passlib.hash import sha256_crypt
from datetime import datetime
from bson.objectid import ObjectId
from functools import wraps
from werkzeug.datastructures import MultiDict
from dotenv import load_dotenv
import os
from models.AuthorModel import AuthorModel
from forms import RegistrationForm, LoginForm, RecipeForm
from webpackManifest import WebpackManifest

# wireframe -> https://xd.adobe.com/spec/3363e2bb-a0eb-4512-659b-50443e231490-4552/

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

manifest_params = {
    'static_folder': '/static',
    'manifest_path': './static/manifest.json'
}

manifest = WebpackManifest(app, manifest_params)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not AuthorModel.is_logged():
            flash('You need to login to continue', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated


@app.template_filter()
def capitalize(text):
    """Convert a string to capitalize"""
    return text[0].upper() + text[1:]


"""
Create models
"""
authors = AuthorModel(mongo)


@app.context_processor
def inject_to_template():
    """ Inject global data to templates """
    return dict(user=authors.logged_as())


@app.route('/')
def index():
    return render_template('index.html', body_class='home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global authors
    # MultiDict([('username', 'mariusz')])
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():

        author = authors.authenticate(request.form.to_dict())
        if author is not False:
            session['user'] = {
                'id': str(ObjectId(author['_id'])),
                'username': author['username']
            }
            flash('Successfully logged in', 'success')
            return redirect(url_for('index'))

        flash('Wrong username or password', 'error')
        return redirect(url_for('login'))

    if 'user' in session:
        session.pop('user', None)
    return render_template('login.html', form=form, body_class='login')


@app.route('/logout')
def logout():
    flash('Successfully logged out', 'success')
    return redirect('login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Method is used for register user
    :return: template register or redirect to login
    """
    global authors
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        if authors.get_by_username(username):
            flash(u'Username {} is already registered'.format(username), 'error')
            return redirect(url_for('register'))
        data = {
            'username': username.lower(),
            'password': sha256_crypt.encrypt(request.form.get('password')),
            'registered': datetime.now(),
        }
        authors.register(data)
        flash(u'You have been registered', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, title="Register",  body_class='register')


@app.route('/recipe/add', methods=['GET', 'POST'])
@requires_auth
def new_recipe():
    # More complete example of FieldList with FormField
    # https://gist.github.com/doobeh/5d0f965502b86fee80fe
    # https://medium.com/python-pandemonium/never-write-for-loops-again-91a5a4c84baf
    data = MultiDict(
        [
            ('title', 'Ragu'),
            ('introduction', 'some'),
            ('method-0', 'Add some'),
            ('method-1', 'Add some'),
            ('method-2', 'Add two'),
            ('categories-0', 'Bake'),
            ('categories-1', 'Chicken')
        ]
    )
    form = RecipeForm(data, request.form)
    if request.method == 'POST' and form.validate():
        return 'Post'
    return render_template('recipe_edit.html',
                           form=form,
                           title='Add recipe',
                           body_class='edit_recipe')


@app.route('/user/<user_id>')
def user(user_id):
    user_db = authors.get_one_by_id(ObjectId(user_id))
    return render_template('user.html', user_db=user_db)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
