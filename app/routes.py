from app import app, db
from flask import render_template, url_for, redirect, flash, jsonify, session
from app.models import Product, User
from app.forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
import datetime
import requests

def checkCartSession():
    try:
        return session['cart']
    except:
        session['cart'] = []

@app.context_processor
def getGlobal():
    try:
        return {'sessionCart': session['cart']}
    except:
        session['cart'] = []
    return {'sessionCart': session['cart']}

@app.route('/')
@app.route('/index', methods={'GET'})
def index():
    checkCartSession()
    session['cart'] = []
    products = Product.query.all()
    return render_template('index.html', title="Home", products=products)

@app.route('/products', methods={'GET'})
def products():
    # checkCartSession()
    products = Product.query.all()
    print(session['cart'])
    return render_template('products.html', title="Products", products=products)

@app.route('/products/add/<id>', methods=['GET', 'POST'])
def productsAdd(id):
    # checkCartSession()
    product = Product.query.get(id)
    item = {'id': product.id,
            'name': product.name,
            'image': product.image,
            'price': product.price,
            'description': product.description
            }

    session['cart'].append(item)

    flash(f"{item['name']} added to cart")



    return redirect(url_for('products'))

@app.route('/products/view', methods=['GET', 'POST'])
def products_view():

    total = 0
    for item in session['cart']:
        total += item['price']

    total = round(total, 2)

    return render_template('products_view.html', total=total)

@app.route('/new_arrivals', methods={'GET'})
def new_arrivals():
    checkCartSession()
    URL = 'http://api.shortboxed.com/comics/v1/new'
    r = requests.get(URL)
    new_arrivals = r.json()

    return render_template('new_arrivals.html', new_arrivals=new_arrivals)





@app.route('/login', methods={'GET', 'POST'})
def login():
    checkCartSession()
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
    checkCartSession()
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
    checkCartSession()
    # if username is empty
    if not username:
        return redirect(url_for('login'))

    person = User.query.filter_by(username=username).first()

    return render_template('profile.html', title='Profile', person=person)

@app.route('/logout')
def logout():
    checkCartSession()

    logout_user()
    return redirect(url_for('login'))
