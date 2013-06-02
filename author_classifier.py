from getcorpus import corpus
from classifier import classify
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk import FreqDist

wrdsC = gutenberg.words()
wrds = [w.lower() for w in wrdsC]

trainingsteksten_lang = [(text,"lang") for text in [wrds[:x] for x in range(150,170)]] 
trainingsteksten_kort = [(text,"kort") for text in [wrds[:x] for x in range(60,70)]] 
trainingsteksten = trainingsteksten_lang + trainingsteksten_kort


classify("Hallo!",trainingsteksten,["f1","f2","f3"],["lang","kort"])
    
# lijst gewenste auteurs
authors=["AaronPressman","AlanCrosby","AlexanderSmith","BenjaminKangLim","BernardHickey"]



def numberoftexts_cat(author,texts):
    """counts the number of texts of a given author"""
    count = 0
    for (text,cat) in texts:
        if(cat == author):
            count +=1
    return count   

def SentenceLengths(corp):
    AverageLengths={}
    
    for (text,cat) in corp:
        AverageLengths[cat]=[]
    
    for (text,cat) in corp:
       sentences=[len(word_tokenize(t)) for t in sent_tokenize(text)]
       sentence_length_text = sum(sentences) / float(len(sentences))
       AverageLengths[cat].append(sentence_length_text)
      
    for cat in AverageLengths.keys():
        average_sentence_cat = sum(AverageLengths[cat])/float(len(AverageLengths[cat]))
        AverageLengths[cat] = average_sentence_cat
    
    return AverageLengths

def Generate_BoW(text):
    # generated bag of words of one text
    return FreqDist(word_tokenize(text))

for a in authors:
    print a + ":" 
    print numberoftexts_cat(a,corpus())
    

print "\nAverage length of sentences per author:"
print SentenceLengths(corpus())