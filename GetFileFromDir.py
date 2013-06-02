import os
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk import FreqDist
import pickle
from random import randint

corpus=[] #Een lijst van tuples die een string (per nieuwsbericht/file) en een label van de auteur bevatten.

# lijst gewenste auteurs
authors=["AaronPressman","AlanCrosby","AlexanderSmith","BenjaminKangLim","BernardHickey"]

def get_content(filename):
	"""Read file and return contents as string
	"""
	f=open(filename,'r')
	return f.read()

for r,d,f in os.walk(".\C50train"):
	try:
		authorname=r.split('\\')[2]		#Alleen op het laagste niveau in de boom
		for files in f:
			if authorname in authors:
				corpus.append((get_content(os.path.join(r,files)), authorname))
	except:
		pass

#schrijft corpus naar bestand, als lijst tuples
corpusfile = open('corpus.pkl','wb')
pickle.dump(corpus,corpusfile)
corpusfile.close()

#importeert corpus
corpusfile = open('corpus.pkl','rb')
corpusimport = pickle.load(corpusfile)
corpusfile.close()
