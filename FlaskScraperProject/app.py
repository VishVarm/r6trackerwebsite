from flask import Flask, render_template, request, redirect, session, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def kdScraper(gamertag):
	URL = "https://r6.tracker.network/profile/xbox/" + gamertag
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	for kd in soup.find('div', {'data-stat': 'PVPKDRatio'}):
		return kd.strip()

def killsScraper(gamertag):
	URL = "https://r6.tracker.network/profile/xbox/" + gamertag
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	for kills in soup.find('div', {'data-stat': 'PVPKills'}):
		return kills.strip()

def rankedKDScraper(gamertag):
	URL = "https://r6.tracker.network/profile/xbox/" + gamertag
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	for rankedkd in soup.find('div', {'data-stat': 'RankedKDRatio'}):
		return rankedkd.strip()

def rankedKillsScraper(gamertag):
	URL = "https://r6.tracker.network/profile/xbox/" + gamertag
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	for rankedKills in soup.find('div', {'data-stat': 'RankedKills'}):
		return rankedKills.strip()

def casualKDScraper(gamertag):
	URL = "https://r6.tracker.network/profile/xbox/" + gamertag
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	for unrankedkd in soup.find('div', {'data-stat': 'UnRankedKDRatio'}):
		return unrankedkd.strip()

def scrapeSite(gamertag):
	URL = "https://r6.tracker.network/profile/xbox/" + gamertag
	page = requests.get(URL)
	soup = BeautifulSoup(page.content, "html.parser")
	stats = {}
	for kd in soup.find('div', {'data-stat': 'PVPKDRatio'}):
		stats['generalKD'] = kd.strip()
	for kills in soup.find('div', {'data-stat': 'PVPKills'}):
		stats['generalKills'] = kills.strip()
	for rankedkd in soup.find('div', {'data-stat': 'RankedKDRatio'}):
		stats['rankedKD'] = rankedkd.strip()
	for rankedKills in soup.find('div', {'data-stat': 'RankedKills'}):
		stats['rankedKills'] = rankedKills.strip()
	for unrankedkd in soup.find('div', {'data-stat': 'UnRankedKDRatio'}):
		stats['unrankedKD'] = unrankedkd.strip()
	for unrankedKills in soup.find('div', {'data-stat': 'UnRankedKills'}):
		stats['unrankedKills'] = unrankedKills.strip()
	"""	
	for ranks in soup.find_all(['small', 'div'], {'class': 'r6-quickseason__rank trn-text--dimmed'}):
		print(ranks.text)	
	for seasonName in soup.find_all('div', {'class': 'r6-quickseason__label'}):
		print(seasonName.text.strip())
	"""
	"""
	for rank in soup.find_all(['small', 'div', 'span'], {'class': ['r6-quickseason__rank trn-text--dimmed', 'r6-quickseason__label', 'r6-quickseason__value']}):
		#print(seasonName.text.strip())
		print(rank.text.strip())
	
	print("BREAK")
	for topRank in soup.find_all('span', {'class': 'r6-quickseason__value'}):
		print(topRank.text.strip())
	"""
	"""
	for topRank in soup.find_all(['span', 'div'], {'class': ['r6-quickseason__value', 'r6-quickseason__label']}):
		print(topRank.text.strip())
		#print("BREAK")
	"""
	mmrHistory = {}
	for seasonName, topRank in zip(soup.find_all('div', {'class': 'r6-quickseason__label'}), soup.find_all('span', {'class': 'r6-quickseason__value'})):
		#print(seasonName.text.strip())
		#print(topRank.text.strip())
		mmrHistory[seasonName.text.strip()] = topRank.text.strip()

	for seasonName, topRank in mmrHistory.items():
		print(seasonName + ": " + topRank)
	
	"""
	x = 0
	for seasonName in soup.find_all('div', {'class': 'r6-quickseason__label'}):
		print(seasonName.text.strip())
		x = x + 1
		print(x)
		mmrHistory[seasonName] = '0'
	x = 0
	for topRank in soup.find_all('span', {'class': 'r6-quickseason__value'}):
		print(topRank.text.strip())
		x = x + 1
		print(x)
	"""
	"""
	divContents = soup.find_all('div', {'class': "r6-quickseason"})
	#print(divContent)
	for divContent in divContents:
		for seasonName in divContent.find_all('div', {'class': 'r6-quickseason__label'}):
			print(seasonName.text.strip())
		#print("PENIS")
	#print("NOOOOO")
	"""
	
	"""
	for divContent in soup.find('div', {'class': "r6-quickseason"}):
		#print(divContent)
		if(x > 0):
			for seasonName in divContent.find_all('div', {'class': 'r6-quickseason__label'}):
				print(seasonName)
		print(x)
		x = x + 1
	"""	

	
	return stats



#app.gamertag == ''
app.secret_key = 'BAD_SECRET_KEY'


@app.route('/', methods=["POST","GET"])
def base_page():
	if request.method == "POST":
		session["username"] = request.form["gamertag"]
		return redirect(url_for("stat_page"))
		#return render_template("testing.html", username=gamertag, kdstat=kdScraper(gamertag), killstat=killsScraper(gamertag))
	else:
		pass
	if request.method == "GET":
		pass
	return render_template('index.html')
	
@app.route('/stat_page')
def stat_page():
	#return render_template("testing.html", username=session.get("username"), kdstat=kdScraper(session.get("username")), killstat=killsScraper(session.get("username")), rankedKDStat=rankedKDScraper(session.get("username")),\
	#	rankedKillsStat=rankedKillsScraper(session.get("username")), unrankedKDStat=casualKDScraper(session.get("username")))
	stats = scrapeSite(session.get("username"))
	return render_template("testing.html", username=session.get("username"), kdstat=stats['generalKD'], killstat=stats['generalKills'], rankedKDStat=stats['rankedKD'], rankedKillsStat=stats['rankedKills'], unrankedKDStat=stats['unrankedKD'], unrankedKillsStat=stats['unrankedKills'])

if __name__ == "__main__":
	app.run(debug=True)
	
	
	
	
	