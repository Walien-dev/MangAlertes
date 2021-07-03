import requests, time, datetime, json
from requests_html import HTMLSession
from dateparser import parse as ConvertDate
import time


def fnac():
	start = time.time()
	session = HTMLSession()
	headers = {"accept-language":"fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"}
	r = session.get("https://livre.fnac.com/l37273/Top-des-mangas-a-paraitre/Manga?sl&ssi=2&sso=2&PageIndex=1", headers=headers)
	results = int(r.html.xpath('//div[@class="sliderTotal"]')[0].text.split(' ')[0])
	pages = int(results/20)+1

	articles= [] 
	for page in range(0, pages):
		page += 1
		r = session.get(f"https://livre.fnac.com/l37273/Top-des-mangas-a-paraitre/Manga?sl&ssi=2&sso=2&PageIndex={page}", headers=headers)
		articles += r.html.xpath('//article[@class="Article-itemGroup"]')

	sorties = {}
	for manga in articles:
		try:
			date = manga.xpath('//span[@class="f-buybox-deliverydate"]')[0].text
			date = ConvertDate(date).date().strftime("%m, %d, %Y")
		except:
			date = "00"
		sortie = {}
		try:
			sortie['img'] = manga.xpath('//img/@data-lazyimage')[0]
		except:
			sortie['img'] = 'assets/noimage.png'
		sortie['titre'] = manga.xpath('//a')[0].text.split(' - ')[0]
		try:
			sortie['tome'] = manga.xpath('//a')[0].text.split(' - ')[1].split(' : ')[0]
		except:
			sortie['tome'] = "Tome ?"
		if 'collector' in manga.xpath('//a')[0].text:
			sortie['edition'] = "Edition collector"
		else:
			sortie['edition'] = "Edition simple"
		if date in sorties:
			sorties[date].append(sortie)
		else:
			sorties[date] = [sortie]

	end = time.time()
	file = open('assets/precos.json', "w+")
	file.write(json.dumps(sorties, sort_keys=True, indent=4))
	file.close()
	print(f"{int(end - start)}secondes pour trouver les résultats")