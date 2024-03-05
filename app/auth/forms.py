from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from ..models import User

class LoginForm(FlaskForm):
    email = EmailField(
        _l("Seu Email"),
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": _l("Seu Email")}
    )
    password = PasswordField(
        _l("Sua Senha"),
        render_kw={"placeholder": _l("Sua Senha")},
        validators=[DataRequired()]
    )
    remember_me = BooleanField(_l("Lembre-se de mim"))
    submit = SubmitField(_l("Log in"))


class CadastrarUsuarioForm(FlaskForm):
    email = EmailField(
        _l("Email:"),
        validators=
            [
                DataRequired(),
                Email()
            ],
            render_kw={
                "placeholder": _l("Email"),
                "cols": 12
            }
    )
    name = StringField(
        _l("Nome:"),
        validators=[DataRequired()],
        render_kw={
            "placeholder": _l("Nome"),
            "cols": 12
        }
    )
    password = PasswordField(
        _l("Senha:"),
        render_kw={"placeholder": _l("Senha")},
        validators=[
            DataRequired(),
            EqualTo(
                "confirm",
                message=_("Senhas diferentes")
            )
        ]
    )
    confirm = PasswordField(
        _l("Repita a Senha:"),
        render_kw={"placeholder": _l("Repita a Senha")},
        validators=[DataRequired()]
    )

    terms = BooleanField('', validators=[DataRequired()])

    submit = SubmitField(_l("Cadastrar"))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError(_("O email já existe."))

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError(_("O nome de usuário já existe."))

class CadastroRapido(FlaskForm):
    terms = BooleanField('', validators=[DataRequired()])

    submit = SubmitField(_l("Cadastrar"))

class AlterarSenhaForm(FlaskForm):
    current_password = PasswordField(
        _l("Senha Atual:"),
        render_kw={"placeholder": _l("Senha Atual")},
        validators=[DataRequired()]
    )
    password = PasswordField(
        _l("Nova Senha:"),
        render_kw={"placeholder": _l("Nova Senha")},
        validators=[
            DataRequired(),
            EqualTo(
                "confirm",
                message=_l("Senhas diferentes")
            )
        ]
    )
    confirm = PasswordField(
        _l("Repita a nova senha:"),
        render_kw={"placeholder": _l("Repita a Nova Senha")},
        validators=[DataRequired()]
    )

    submit = SubmitField(_l("Alterar Senha"))
