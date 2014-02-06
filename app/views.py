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
	b=0
	for i in data:
		if (len(i) < len(data[0])):
			zeros = [0] * (len(data[0])-len(i))
			for a in zeros:
				data[b].insert(1,0)
		b=b+1
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

@app.route('/danpassword')
def danpassword():
	user=User.query.all()
	for u in user:
		if u.username==u'dannyb21892':
			danpass=u.password
	return render_template('danpassword.html',
		danpass=danpass)