import pickle
import re

def corpus(num):
    corpusfile = open('corpus.pkl','r')
    c = pickle.load(corpusfile)
    corpusfile.close()
    c1 = []
    for (text,author) in c[:(num*50)]:
        c1 += [(re.sub(r"(?<=[a-z])\.",r" .",text),author)] # leest punten als apparte 'woorden' als ze aan het eind v. een zin staan (niet in afkortingen met hoofdletters)
    # deze replace maakt om de een of ander vage reden dat er te weinig auteurs worden ingelezen
    #   	c1 += [(re.sub(r"&amp;",r"and",text),author)]
    return c1[:(num*50)]

def corpus_train():
    corpusfile = open('traincorpus.pkl','r')
    c = pickle.load(corpusfile)
    corpusfile.close()
    c1 = []
    for (text,author) in c:
        c1 += [(re.sub(r"(?<=[a-z])\.",r" .",text),author)] # leest punten als apparte 'woorden' als ze aan het eind v. een zin staan (niet in afkortingen met hoofdletters)
    # deze replace maakt om de een of ander vage reden dat er te weinig auteurs worden ingelezen
    #   	c1 += [(re.sub(r"&amp;",r"and",text),author)]
    return c1
    
def corpus_dev():
    corpusfile = open('devcorpus.pkl','r')
    c = pickle.load(corpusfile)
    corpusfile.close()
    c1 = []
    for (text,author) in c:
        c1 += [(re.sub(r"(?<=[a-z])\.",r" .",text),author)] # leest punten als apparte 'woorden' als ze aan het eind v. een zin staan (niet in afkortingen met hoofdletters)
    # deze replace maakt om de een of ander vage reden dat er te weinig auteurs worden ingelezen
    #   	c1 += [(re.sub(r"&amp;",r"and",text),author)]
    return c1