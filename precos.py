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

	sorties, today = {}, []
	for manga in articles:
		sortie = {}
		try:
			sortie['date'] = manga.xpath('//span[@class="f-buybox-deliverydate"]')[0].text
			sortie['date'] = ConvertDate(sortie['date']).date().strftime("%d/%m/%Y")
		except:
			sortie['date'] = "00"
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
		mangaTxt = f"{sortie['date']}\-|-/{sortie['img']}\-|-/{sortie['titre']}\-|-/{sortie['tome']}\-|-/{sortie['edition']}"
		sorties[mangaTxt] = sortie
		today.append(mangaTxt)

	end = time.time()
	file = open('assets/precos.txt', "r")
	Lasts = file.read().split("\n")
	newprecos = list(set(today) - set(Lasts))
	file.close()
	print(f"{int(end - start)}secondes pour trouver les résultats")
	sorties2 = []
	for newpreco in newprecos:
		sorties2.append(sorties[newpreco])
	file = open('assets/precos.txt', "w+")
	for mangaTxt in today:
		file.write("%s\n" % mangaTxt)
	file.close()
	return sorties2
