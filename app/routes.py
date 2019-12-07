from app import app, db
from flask import render_template, url_for, redirect, flash
from app.models import Product, User
from app.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
import datetime

@app.route('/')
@app.route('/index', methods={'GET'})
def index():
    products = Product.query.all()
    return render_template('index.html', title="Home", products=products)

@app.route('/products', methods={'GET'})
def products():
    products = Product.query.all()
    return render_template('products.html', title="Products", products=products)

@app.route('/login', methods={'GET', 'POST'})
def login():

    form = LoginForm()

    if form.validate_on_submit():
        # qurey the db for the user information and log them in if everything is valid.
        user = User.query.filter_by(email=form.email.data).first()

        # if user doesn't exsit, reload page and flash message
        if user is None or not user.check_password(form.password.data):
            flash('Invalid credentials')
            return redirect(url_for('login'))

        #if user exists and credentials are correct, log them in
        login_user(user)
        flash(f"You have been logged in.")
        return redirect(url_for('profile', username=current_user.username))

    return render_template('form.html', form=form, title='Login')

@app.route('/register', methods={'GET', 'POST'})
def register():
    # if user is already logged in , redirect them.
    if current_user.is_authenticated:
        flash("you are already logged in")
        return redirect(url_for('profile', username=current_user.username))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            email = form.email.data,
        )

        # include password
        user.set_password(form.password.data)

        # add to stage and commit
        db.session.add(user)
        db.session.commit()

        flash(f"You have been registered.")
        return redirect(url_for('login'))

    return render_template('form.html', form=form, title='Register')

@app.route('/profile')
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username=''):
    # if username is empty
    if not username:
        return redirect(url_for('login'))

    person = User.query.filter_by(username=username).first()

    return render_template('profile.html', title='Profile', person=person)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
