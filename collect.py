#!flask/bin/python
import mechanize
from bs4 import BeautifulSoup as soup
import datetime
from app import app, models, db
import unicodedata

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
	neopoints = int([l.text for l in br.links(url_regex='inventory')][0].replace(',',''))

	bank = br.click_link(url='/bank.phtml')
	br.open(bank)
	soupbank=soup(br.response().read())
	bankpoints=soupbank.find(align='center',style='font-weight: bold;')
	if (bankpoints is None):
		bankpoints=0
	else:
		bankpoints=bankpoints.text
		bankpoints=str(bankpoints)
		bankpoints=bankpoints.replace(',','')
		bankpoints=bankpoints.replace(' NP','')
		bankpoints=int(bankpoints)
		print bankpoints

	stockpage = br.open('http://www.neopets.com/stockmarket.phtml?type=portfolio')
	stockhtml = soup(br.response().read())
	tableline = stockhtml.find(bgcolor='#BBBBBB')
	if tableline is None:
		stockpoints=0
	else:
		tablefirst = tableline.find(align='center')
		tablesecond = tablefirst.findNextSibling()
		stockpoints = tablesecond.findNextSibling()
		stockpoints=stockpoints.text
		stockpoints=str(stockpoints)
		stockpoints=int(stockpoints.replace(',',''))

	totalpoints=bankpoints+neopoints+stockpoints
	totalpoints=str(totalpoints)
	print i.username + ' has ' + totalpoints

	datapoint = models.DataPoint(points=totalpoints,timestamp=datetime.datetime.now(), author=i)
	db.session.add(datapoint)

	logout = br.click_link(url='/logout.phtml')
	br.open(logout)

db.session.commit()