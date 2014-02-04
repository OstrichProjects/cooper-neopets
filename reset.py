from app import app, models, db

users = models.User.query.all()

for u in users:
	if u.username=='testing314':
		db.session.delete(u)
		print 'deleted testing'

db.session.commit()
