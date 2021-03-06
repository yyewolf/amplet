from db import app, db
from models import *
from flask import render_template, redirect, url_for, session, flash
from flask_login import login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Email, Length, ValidationError

##############################
########### LOGIN  ###########
##############################


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(max=50)], render_kw={"placeholder": "Pseudo"})
    password = PasswordField("Password", validators=[InputRequired(), Length(max=50)], render_kw={"placeholder":  "Mot de passe"})
    submit = SubmitField("Se connecter")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email(message="Email invalide"), Length(max=100)], render_kw={"placeholder": "exemple@gmail.com"})
    username = StringField("Username", validators=[InputRequired(), Length(max=50)], render_kw={"placeholder": "Pseudo"})
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Mot de passe"})
    numero = IntegerField("Numero",validators=[InputRequired()],render_kw={"placeholder": "Numéro de rue"})
    rue = StringField("rue",validators=[InputRequired()], render_kw={"placeholder": "Nom de rue"})
    ville = StringField("ville",validators=[InputRequired()], render_kw={"placeholder": "Nom de la ville"})
    codepostal = IntegerField("codepostal",validators=[InputRequired()],render_kw={"placeholder": "Code Postal de la ville"})
    submit = SubmitField("S'inscrire")

    def validate_username(self, username):
        existing_user_username = users.User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("Ce nom d'utilisateur existe déjà merci d'en choisir un autre")

    def validate_email(self, email):
        existing_user_email = users.User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError("Cette addresse email est déjà utilisée par un autre utilisateur merci d'en choisir une autre")

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_adresse = adresses.Adresse(numero=form.numero.data,rue=form.rue.data,ville=form.ville.data,codepostal=form.codepostal.data)
        new_user = users.User(username=form.username.data, email=form.email.data,id_adresse=new_adresse.id)
        new_user.set_password(form.password.data)
        db.session.add(new_adresse)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('auth.html', title='Register', form=form, login=False)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("index"))
        flash("Vérifiez que le nom d'utilisateur / mot de passe est correct")
    return render_template('auth.html', title="Login", form=form, login=True)

@app.route('/logout', methods=["GET","POST"])
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))