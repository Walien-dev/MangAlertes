mmessage = []
imagetweets = []

def img(i, day):
	thistweet, start = [], 0
	for o in range(0, len(day)):
		start += 1
		if start <= 4:
			try:
				thistweet.append(day[i+o]['img'])
			except Exception as e:
				print(e)
				break
		else:
			break
	imagetweets.append(thistweet)

def msg(day):
	for i, sortie in enumerate(day):
		if len(mmessage) == 0:
			mmessage.append(f"☀ VOICI LES SORTIES DU JOUR ☀\n\n- {sortie['titre']} {sortie['tome']} ({sortie['edition']})")
			img(i, day)
		elif len(mmessage[len(mmessage)-1]) >= 200:
			mmessage.append(f"\n- {sortie['titre']} {sortie['tome']} ({sortie['edition']})")
			img(i, day)
		else:
			mmessage[len(mmessage)-1] += f"\n- {sortie['titre']} {sortie['tome']} ({sortie['edition']})"
	return mmessage, imagetweets