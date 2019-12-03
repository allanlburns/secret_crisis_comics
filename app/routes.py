from app import app, db
from flask import render_template, url_for, redirect
from app.models import Product

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")

@app.route('/products', methods={'GET'})
def products():
    return render_template('index.html', title="Products")
