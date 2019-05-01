from wtforms import Form, BooleanField, TextAreaField, HiddenField, StringField, PasswordField, validators, FieldList


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


"""
class RecipeForm(Form):
https://wtforms.readthedocs.io/en/stable/forms.html

 form = EditProfileForm(request.POST, obj=user)
 https://overiq.com/flask-101/form-handling-in-flask/
form = LoginForm(MultiDict([('username', 'mariusz')]), request.form)
https://stackoverflow.com/questions/32021650/how-to-validate-an-array-with-wtforms-and-flask?rq=1


{{ form.method.data }}
{{ form.method.label }}   
"""


class RecipeForm(Form):
    title = StringField('Title', [validators.DataRequired()])
    introduction = TextAreaField('Introduction')
    method = FieldList(TextAreaField('Method'), min_entries=1)
    ingredients = FieldList(HiddenField('Ingredients'), validators=[validators.DataRequired()], min_entries=1)
    categories = FieldList(HiddenField('Categories'), validators=[validators.DataRequired()], min_entries=1)
    cuisines = FieldList(HiddenField('Cuisines'), validators=[validators.DataRequired()], min_entries=1)
    allergens = FieldList(HiddenField('Allergens'), validators=[validators.DataRequired()], min_entries=1)
