from flask import render_template, flash, redirect
from app import app, db
from forms import LoginForm
from models import User

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
    	title = 'Cooper Neopets',
    	data=[])

@app.route('/login', methods= ['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		u = User(username = form.username.data, password = form.password.data)
		db.session.add(u)
		db.session.commit()
		return redirect('/login')
	return render_template("login.html",
		title = 'Cooper Neopets',
		form = form,
		users=User.query.all())