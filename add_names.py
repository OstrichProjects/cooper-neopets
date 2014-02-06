from app import app, models, db

users = models.User.query.all()
names = ['Jon','Shivam','Harnsowl','Mitchell','Anthony','Kenny','Christian','Marcello','Sharang','Malcolm','Vasily','Ethan','Dan']
i=0
for u in users:
	i=models.FirstName(name=names[i], author=u)
	db.session.add(i)
	i=i+1

db.session.commit()