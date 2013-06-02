from getcorpus import corpus
from classifier import classify
from nltk.corpus import gutenberg
from help_functions import *



def test(): 
    """ Een test classification a.d.h.v. het gutenberg corpus. (Is het een korte of lange text? >100 / < 100wrd) """
    wrdsC = gutenberg.words()
    wrds = [w.lower() for w in wrdsC]
    trainingsteksten_lang = [(text,"lang") for text in [wrds[:x] for x in range(150,170)]] 
    trainingsteksten_kort = [(text,"kort") for text in [wrds[:x] for x in range(60,70)]] 
    trainingsteksten = trainingsteksten_lang + trainingsteksten_kort
    classify("Hallo!",trainingsteksten,["f1","f2","f3"],["lang","kort"])
    
# lijst gewenste auteurs
authors=["AaronPressman","AlanCrosby","AlexanderSmith","BenjaminKangLim","BernardHickey"]
    
    
test()

print "\nAverage length of sentences per author:"
print SentenceLengths(corpus())

