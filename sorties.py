import requests, datetime
from requests_html import HTMLSession
from dateparser import parse as ConvertDate

def recup():
	session = HTMLSession()
	resp = session.get("https://www.mangacollec.com/planning")
	planning = resp.html.xpath('//div[@id="planning"]')[0]

	sorties = {}

	for i, h2 in enumerate(planning.find('h2')):
		date = ConvertDate(h2.text).date().strftime("%m, %d, %Y") #month, day, YEAR (ex: 08, 22, 2021)
		sorties[date] = []
		for li in planning.find('ul')[i].find('li'):
			sortie = {}  
			try:
				sortie['img'] = li.xpath('//img/@src')[0]
			except:
				sortie['img'] = 'assets/noimage.png'
			sortie['titre'] = li.xpath('//span[@class="primary-title"]')[0].text
			sortie['tome'] = li.xpath('//span[@class="secondary-title"]')[0].text
			sortie['edition'] = li.xpath('//a/@title')[0].replace(sortie['titre'], '').replace(sortie['tome'], '')
			sorties[date].append(sortie)
	return sorties
