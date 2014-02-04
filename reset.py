from app import app, models, db

users = models.User.query.all()

for u in users:
	for i in u.datapoints:
		db.session.delete(i)

db.session.commit()
