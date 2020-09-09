from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from siteA import app, db
from siteA.models import Item, User, Teams


@app.route('/')
def index():
    team = Teams.query.order_by(reversed(Teams.points)).all()
    return render_template('index.html', data=team)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        name = request.form['name']
        text = request.form['text']

        item = Item(name=name, text=text)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')

        except:
            return "Ошибка"
    else:
        return render_template('create.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')

            return redirect(next_page)
        else:
            flash('Неверный логин или пароль ')

    else:
        flash('Введите логин и пароль')

    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password_retr = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password_retr):
            flash('Заполните форму')
        elif password != password_retr:
            flash("Пароли не совпадают")
        else:
            hash_pass = generate_password_hash(password)
            new_user = User(login=login, password=hash_pass)
            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login_page'))
            except:
                return "Ошибка"

    return render_template("registration.html")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next' + request.url)

    return response
