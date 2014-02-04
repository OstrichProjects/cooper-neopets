#!flask/bin/python
import mechanize
from bs4 import BeautifulSoup as soup
import datetime
from app import app, models, db

logins = models.User.query.all()

for i in logins:
	username = i.username
	password = i.password
	br = mechanize.Browser()
	br.open('http://www.neopets.com/login')

	br.select_form(nr=0)
	br.form['username']=username
	br.form['password']=password
	br.submit()
	if br.geturl()=='http://www.neopets.com/':
		neopoints = int([l.text for l in br.links(url_regex='inventory')][0].replace(',',''))

		bank = br.click_link(url='/bank.phtml')
		br.open(bank)
		soupbank=soup(br.response().read())
		bankpoints=soupbank.find(align='center',style='font-weight: bold;')
		if (type(bankpoints) is not unicode):
			bankpoints=0
		else:
			bankpoints=bankpoints.string
			bankpoints=bankpoints.replace(',','')
			bankpoints=bankpoints.replace(' NP','')
			bankpoints=int(bankpoints)

		totalpoints=bankpoints+neopoints
		totalpoints=str(totalpoints)

		datapoint = models.DataPoint(points=totalpoints,timestamp=datetime.datetime.now(), author=i)
		db.session.add(datapoint)

db.session.commit()