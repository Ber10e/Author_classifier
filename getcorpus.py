import pickle
import re

def corpus(num):
    corpusfile = open('corpus.pkl','r')
    c = pickle.load(corpusfile)
    corpusfile.close()
    c1 = []
    for (text,author) in c[:(num*50)]:
        c1 += [(re.sub(r"(?<=[a-z])\.",r" .",text),author)] # leest punten als apparte 'woorden' als ze aan het eind v. een zin staan (niet in afkortingen met hoofdletters)
    return c1[:(num*50)]

