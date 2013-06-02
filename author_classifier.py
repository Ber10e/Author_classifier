from getcorpus import corpus
from classifier import classify
from nltk.corpus import gutenberg
from help_functions import *
wrdsC = gutenberg.words()
wrds = [w.lower() for w in wrdsC]

def test():
    trainingsteksten_lang = [(text,"lang") for text in [wrds[:x] for x in range(150,170)]] 
    trainingsteksten_kort = [(text,"kort") for text in [wrds[:x] for x in range(60,70)]] 
    trainingsteksten = trainingsteksten_lang + trainingsteksten_kort
    classify("Hallo!",trainingsteksten,["f1","f2","f3"],["lang","kort"])
    
# lijst gewenste auteurs
authors=["AaronPressman","AlanCrosby","AlexanderSmith","BenjaminKangLim","BernardHickey"]

for a in authors:
    print a + ":" 
    print numberoftexts_cat(a,corpus())
    
print "\nAverage length of sentences per author:"
print SentenceLengths(corpus())