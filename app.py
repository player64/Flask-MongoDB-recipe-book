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
from models.RecipeModel import RecipeModel
from models.CategoryModel import CategoryModel
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


@app.template_filter()
def truncate_text(text):
    return text[:120] + '...' if len(text) >= 120 else text


@app.context_processor
def template_functions():
    def string_limit(text, limit):
        short_text = text.split(' ')[:limit]
        str = '...' if len(short_text) >= limit else ''
        return ' '.join(short_text) + str

    def pagination_url(type, attr, page_no, order, total_pages=None):
        paginate = page_no

        if type == 'prev':
            if page_no == 1:
                return '#'
            paginate = page_no - 1
        elif type == 'next':
            if total_pages == page_no:
                return '#'
            paginate = page_no + 1

        if attr['name'] == 'author':
            return url_for('index', page_no=paginate, order_by=order, author_name=attr['author'])
        elif attr['name'] == 'tag':
            return url_for('index', page_no=paginate, order_by=order,
                           tag_name=attr['tag']['name'], tag_value=attr['tag']['value'])
        else:
            return url_for('index', page_no=paginate, order_by=order)

    return dict(string_limit=string_limit, pagination_url=pagination_url)


"""
Create models
"""
author_model = AuthorModel(mongo)
recipe_model = RecipeModel(mongo)
cuisine_model = CategoryModel(mongo, 'cuisines')
category_model = CategoryModel(mongo, 'categories')


@app.context_processor
def inject_to_template():
    """ Inject global data to templates """
    return dict(user=author_model.logged_as())


@app.route('/author/<author_name>/page/<page_no>')
@app.route('/author/<author_name>/page/<page_no>/order-by/<order_by>')
@app.route('/author/<author_name>/order-by/<order_by>')
@app.route('/author/<author_name>')
@app.route('/tag/<tag_name>/<tag_value>/page/<page_no>')
@app.route('/tag/<tag_name>/<tag_value>/page/<page_no>/order-by/<order_by>')
@app.route('/tag/<tag_name>/<tag_value>/order-by/<order_by>')
@app.route('/tag/<tag_name>/<tag_value>/')
@app.route('/page/<page_no>')
@app.route('/page/<page_no>/order-by/<order_by>')
@app.route('/order-by/<order_by>')
@app.route('/')
def index(page_no=None, order_by=None, author_name=None, tag_name=None, tag_value=None):
    if not page_no:
        page_no = 1
    else:
        page_no = int(page_no)

    if not order_by:
        order_by = 'created'

    query = {}
    if author_name is not None:
        page_attr = {
            'name': 'author',
            'author': author_name,
            'link': '/author/'+author_name
        }
        query = {'author': author_name}
    elif tag_name is not None and tag_value is not None:
        page_attr = {
            'name': 'tag',
            'tag': {
                'name': tag_name,
                'value': tag_value
            },
            'link': '/tag/' + tag_name + '/' + tag_value
        }
        query = {tag_name: {'$in': [tag_value]}}
    else:
        page_attr = {
            'name': 'index',
            'link': ''
        }

    recipes = recipe_model.get_archive(query, page_no, order_by)
    return render_template('index.html',
                           body_class='archive',
                           page_attr=page_attr,
                           recipes=recipes,
                           page=page_no,
                           order_by=order_by,
                           pagination=recipe_model.archive_pagination(query))


@app.route('/login', methods=['GET', 'POST'])
def login():
    global author_model
    # MultiDict([('username', 'mariusz')])
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():

        author = author_model.authenticate(request.form.to_dict())
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
    global author_model
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        if author_model.get_by_username(username):
            flash(u'Username {} is already registered'.format(username), 'error')
            return redirect(url_for('register'))
        data = {
            'username': username.lower(),
            'password': sha256_crypt.encrypt(request.form.get('password')),
            'registered': datetime.now(),
        }
        author_model.register(data)
        flash(u'You have been registered', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, title="Register", body_class='register')


@app.route('/recipe/add', methods=['GET', 'POST'])
@requires_auth
def new_recipe():
    # More complete example of FieldList with FormField
    # https://gist.github.com/doobeh/5d0f965502b86fee80fe
    # https://medium.com/python-pandemonium/never-write-for-loops-again-91a5a4c84baf
    """
        data = MultiDict(
        [
            ('title', 'Ragu'),
            ('introduction', 'some'),
            ('method-0', 'Add some'),
            ('method-1', 'Add some'),
            ('method-2', 'Add two'),
            ('categories-0', 'Bake'),
            ('categories-1', 'Chicken'),
            ('cuisines-1', 'French')
        ]
    )
    init_form = RecipeForm(data, request.form)
    :return:
    """

    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        recipe_model.add(form, session['user']['username'])
        return 'POST'
    return render_template('recipe_edit.html',
                           form=form,
                           title='Add recipe',
                           body_class='edit_recipe')


@app.route('/recipe/<recipe_id>')
def view_recipe(recipe_id):
    return recipe_id


@app.route('/user/<user_id>')
def user(user_id):
    user_db = author_model.get_one_by_id(ObjectId(user_id))
    return render_template('user.html', user_db=user_db)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
