import tweepy, datetime, sorties, requests, generetweet, os, json

try:
	auth = tweepy.OAuthHandler(a_key, a_secret)
	auth.set_access_token(a_token, aa_secret)
	api = tweepy.API(auth)
	print("Twitter : ", api.me().screen_name)
except:
	print("Auth Twitter Fail")




while True:
	date = datetime.datetime.now().strftime("%m, %d, %Y")
	
	#
	# SORTIES DU JOUR
	#
	f = open('assets/ventes.json', 'r')
	data = json.load(f)
	f.close()
	if date not in data and date in sorties.recup():
		tweets, images = generetweet.msg(sorties.recup()[date])
		for i, imagetweet in enumerate(images):
			image = imagetweet[0]
			if 'noimage.png' not in image:
				img = requests.get(image).content
				image = "downloads/image.png"
				file = open(image, "wb")
				file.write(img)
				file.close()
			if i == 0:
				tweet = api.update_with_media(image, status=tweets[i])
				f = open('assets/ventes.json', 'w')
				data[date] = "Ok!!!"
				f.write(json.dumps(data, sort_keys=True, indent=4))
				f.close
			else:
				tweet = api.update_with_media(image, status=tweets[i], in_reply_to_status_id=tweet.id)


	#
	# DISPO EN PRECOMMANDE AUJOURD'HUI
	# 
