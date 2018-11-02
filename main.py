import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
import glob,os,re
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import joblib
import pandas as pd

def authenticate_and_return_features(title):
	client_id = '' #use your own
	client_secret = ''
	client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	artist = ''
	sp.trace=False

	search_query = title + ' ' + artist
	result = sp.search(search_query)
	uri = ''
	for i in result['tracks']['items']:
	    # Find a songh that matches title and artist
	    if (i['artists'][0]['name'] == artist) and (i['name'] == title):
	        uri = i['uri']
	        break
	else:
	    try:
	        # Just take the first song returned by the search (might be named differently)
	        uri = result['tracks']['items'][0]['uri']
	    except:
	    	print(title)
	features = sp.audio_features(uri)
	return str(str(features[0]['energy'])+","+str(features[0]['valence']))

def format_name(c):
	ind = 0
	c = c[:-4]
	for b in range(len(c)):
	    if c[b].isalpha():
	        ind = b
	        break
	p =  c[ind::]
	p = " ".join(re.findall("[a-zA-Z\\n\']+", p))
	words = ['feat','ft','hq','audio','remix','explicit','video','official','lyric','vocal','instrumental']
	rc = re.compile('|'.join(map(re.escape, words)))
	p = rc.sub('',p)
	sp = p.split(' ')
	if len(sp)>4:
		for a in range(len(sp)-4):
			sp.pop()
		sp = ' '.join(sp)


	return sp

def files():
	data = []
	n,t=0,0
	f = open('Data.csv','a+')
	#loc = input('Enter path of your music: ').strip()
	loc = input('Enter path of music: ').strip()
	lis = glob.glob(loc+'/*.m4a')
	lis = lis+glob.glob(loc+'/*.mp3')
	#a[:-4]
	for a in lis:
		p = a.split('/')
		try:
			f.write(str(authenticate_and_return_features(format_name(p[-1].lower())))+','+','+a+'\n')
			print(1)
			t+=1			
			f.flush()
			
		except Exception as e:
			n+=1
	f.close()
	print('Tot: ',n+t,' Miss: ',n)
def ml_train():
	data = pd.read_csv('Data.csv', delimiter=',')
	try:
		cols = [4,5]
		df.drop(df.columns[cols],axis=1,inplace=True)
		df.to_csv('Data.csv',sep = ',')
		
	except:
		pass
	fh = open('happy.m3u','a+')
	fs = open('sad.m3u','a+')
	X = data[data.columns[0]]
	y = data[data.columns[1]]
	z = data[data.columns[3]]
	X = list(map(float,X))
	y = list(map(float,y))
	data = []
	for a in range(len(X)):
		data.append([X[a],y[a]])
	data = np.asarray(data)
	#print(data)
	kmeans = KMeans(n_clusters=2, random_state=0).fit(data)
	la = kmeans.labels_
	#0:sad, 1:happy
	for a in range(len(z)):
		if(la[a]==0):
			fh.write(str(z[a])+'\n')
		else:
			fs.write(str(z[a])+'\n')
	fh.close()
	fs.close()

#files()
ml_train()

