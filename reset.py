from app import app, models, db

u = models.User.query.all()

for u in users:
	if u.username=='testing314':
		db.session.delete(u)

data = models.Datapoint.query.all()
for d in data:
	db.session.delete(d)

db.session.commit()
