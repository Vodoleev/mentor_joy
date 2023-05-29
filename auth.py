from app import db, app
from models import Users
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = "Авторизуйтесь для сохранения данных"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, Users)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('auth.login'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=request.form.get('email')).first()
        if user and check_password_hash(user.psw, request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("auth.profile"))

        flash("Неверный логин или пароль", "error")

    return render_template("login.html", title="Авторизация", form=form)


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['email'], username=request.form['name'], psw=hash)
            db.session.add(u)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Регистрация', form=form)
