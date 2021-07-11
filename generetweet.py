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

def msg(day, preco=False):
	for i, sortie in enumerate(day):
		if len(mmessage) == 0:
			if preco:
				StartTweet = "🚨 NOUVELLES PRECOMMANDES DETECTÉES🚨"
			else:
				StartTweet = "☀ VOICI LES SORTIES DU JOUR ☀"
			mmessage.append(f"{StartTweet}\n\n- {sortie['titre']} {sortie['tome']} ({sortie['edition']})")
			img(i, day)
		elif len(mmessage[len(mmessage)-1]) >= 175:
			mmessage.append(f"\n- {sortie['titre']} {sortie['tome']} ({sortie['edition']})")
			img(i, day)
		else:
			mmessage[len(mmessage)-1] += f"\n- {sortie['titre']} {sortie['tome']} ({sortie['edition']})"
		if preco:
			mmessage[len(mmessage)-1] += f" (Sort le: {sortie['date']})"
	return mmessage, imagetweets
