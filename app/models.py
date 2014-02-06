from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, index=True, unique=True)
	password = db.Column(db.String, index=True, unique=False)
	firstname = db.Column(db.String, index=True, unique=False)
	datapoints = db.relationship('DataPoint', backref = 'author', lazy = 'dynamic')

	def __repr__(self):
		return '<User %r>' % (self.username)

class DataPoint(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	points = db.Column(db.Integer)
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Points %r>' % (self.points)