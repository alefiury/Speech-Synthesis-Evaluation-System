from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.fields.html5 import EmailField
from ..models import User

class LoginForm(FlaskForm):
    email = EmailField('Seu Email', validators=[DataRequired(), Email()],
                       render_kw={"placeholder": "Seu Email"})
    password = PasswordField('Sua Senha',
                             render_kw={"placeholder": "Sua Senha"},
                             validators=[DataRequired()])
    remember_me = BooleanField('Lembre-se de mim')
    submit = SubmitField('Log in')


class CadastrarUsuarioForm(FlaskForm):
    email = EmailField('Email:', validators=[
                       DataRequired(), Email()], render_kw={"placeholder": "Email", "cols": 12})
    name = TextField('Nome:', validators=[
                     DataRequired()], render_kw={"placeholder": "Nome", "cols": 12})
    password = PasswordField('Senha:', render_kw={"placeholder": "Senha"},
                             validators=[DataRequired(),
                                         EqualTo('confirm',
                                                 message='Senhas diferentes')])
    confirm = PasswordField('Repita a Senha:',
                            render_kw={"placeholder": "Repita a Senha"},
                            validators=[DataRequired()])

    terms = BooleanField('', validators=[DataRequired()])

    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('O email já existe.')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('O nome de usuário já existe.')


class AlterarSenhaForm(FlaskForm):
    current_password = PasswordField('Senha:',
                                     render_kw={"placeholder": "Senha"},
                                     validators=[DataRequired()])
    password = PasswordField('Nova Senha:',
                             render_kw={"placeholder": "Nova Senha"},
                             validators=[DataRequired(),
                                         EqualTo('confirm',
                                                 message='Senhas diferentes')])
    confirm = PasswordField('Repita a nova senha:',
                            render_kw={"placeholder": "Repita a Nova Senha"},
                            validators=[DataRequired()])

    submit = SubmitField('Alterar Senha')
