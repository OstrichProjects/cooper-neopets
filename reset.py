from app import app, models, db

users = models.User.query.all()

for u in users:
	if u.username==u'dannyb21892':
		db.session.delete(u)

db.session.commit()
