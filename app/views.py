from flask import render_template, flash, redirect
from app import app, db
from forms import LoginForm
from models import User
import unicodedata

@app.route('/')
@app.route('/index')
def index():
	users = User.query.all()
	data=[['Time']]
	for i in users[0].datapoints:
		data[0].append(i.timestamp.strftime('%Y-%m-%d-%H-%M'))
	for u in users:
		pointlist=[unicodedata.normalize('NFKD',u.username).encode('ascii','ignore')]
		for i in u.datapoints:
			pointlist.append(int(i.points))
		data.append(pointlist)
	for i in data:
		if (i.length < data[0].length):
			zeros = [0] * (data[0].length-i.length)
			data[0].insert(1,zeros)
	data=zip(*data)
	data=[list(row) for row in data]
	return render_template("index.html",
    	title = 'Cooper Neopets',
    	data=data)

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