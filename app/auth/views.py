import uuid

from flask_babel import _
from random_username.generate import generate_username
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user

from ..models import User, roles
from . import auth
from .. import db
from .forms import (
    LoginForm,
    CadastrarUsuarioForm,
    AlterarSenhaForm,
    CadastroRapido
)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    # Validate submited data
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # POST/REDIRECT/GET Pattern - Prevent unwanted redirects
            next = request.args.get("next")
            if next is None or not next.startswith('/'):
                next = url_for("main.sound_test")
            return redirect(url_for("main.sound_test"))
        flash(_("Email ou senha incorreta."), "warning")
    return render_template("auth/login.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = CadastrarUsuarioForm()

    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            name=form.name.data,
            password=form.password.data,
            role=roles["user"],
            last_audio=None,
            seed=None
        )
        db.session.add(user)
        db.session.commit()
        flash(form.email.data + _(" cadastrado com sucesso!"), "success")
        return redirect(url_for("auth.login"))
    users = User.query.all()
    return render_template("auth/signup.html", form=form, users=users)


@auth.route("/fast_signup", methods=["GET", "POST"])
def fast_signup():
    form = CadastroRapido()

    rand_name = generate_username(1)[0]
    rand_email = (rand_name+'@email.com').lower()
    rand_password = str(uuid.uuid4())[:8]

    if form.validate_on_submit():
        user = User(
            email=rand_email,
            name=rand_name,
            password=rand_password,
            role=roles['user'],
            last_audio=None,
            seed=None
        )
        db.session.add(user)
        db.session.commit()

        flash(_("Cadastrado rápido criado com sucesso!"), "success")
        flash(_("Email: ") + rand_email, "info")
        flash(_("Senha: ") + rand_password, "info")

        # Log in automatically and force remember_me
        login_user(user, True)
        # POST/REDIRECT/GET Pattern - Prevent unwanted redirects
        next = request.args.get("next")
        if next is None or not next.startswith('/'):
            next = url_for("main.sound_test")
        return redirect(url_for("main.sound_test"))
    users = User.query.all()
    return render_template("auth/fast_signup.html", form=form, users=users)


@auth.route("/finished_fast_signup/<rand_email>/<rand_password>/<rand_name>", methods=["GET", "POST"])
def finished_fast_signup(rand_email, rand_password, rand_name):
    return render_template(
        "auth/finished_fast_signup.html",
        rand_email=rand_email,
        rand_password=rand_password,
        rand_user=rand_name
    )

@auth.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = AlterarSenhaForm()
    if form.validate_on_submit():
        # Verifies current password
        if current_user.verify_password(form.current_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash(_("Senha alterada com sucesso!"), "success")
            return redirect(url_for("main.hello"))
        else:
            flash(_("Senha atual incorreta"), "warning")
    return render_template("auth/change_password.html", form=form)

@auth.route("/terms", methods=["GET", "POST"])
def terms():
    return render_template("auth/terms.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.hello"))
