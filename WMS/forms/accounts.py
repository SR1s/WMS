from flask.ext.wtf import Form, validators
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required

class LoginForm(Form):
    user_no = TextField('user_no',[Required()])
    user_ps = PasswordField('user_ps',[Required()])

