"""
Groepsopdracht2:
Bertine
Tuur
Erlinde
Jelte
"""

from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk import FreqDist
import pickle
wrdsC = gutenberg.words()
wrds = [w.lower() for w in wrdsC]
"""
print wrds[:100]
tt_ratio = float(len(wrds))/float(len(set(wrds)))
print "type/token ratio:"
print tt_ratio
print "documentlengte/aantal woorden:"
print len(wrds)
"""
print "-----------------"
#---------------------------------------------------------------------------------


trainingsteksten_lang = [(text,"lang") for text in [wrds[:x] for x in range(150,170)]] 
trainingsteksten_kort = [(text,"kort") for text in [wrds[:x] for x in range(60,70)]] 
trainingsteksten = trainingsteksten_lang + trainingsteksten_kort

corpusfile = open('corpus.pkl','r')
corpus = pickle.load(corpusfile)
corpusfile.close()


def classify(woorden):
    """ Classifies a text based on the trainingstexts, categories and features.
    Args: String (a text)
    Returns: String (prints propabilities per category)
    """
    categories = ["lang", "kort"] 
    features1 = ["f1","f2","f3"]    
    trained_model = train(trainingsteksten, categories, features1)
    print trained_model[1]
    print trained_model[0]
    score_cat = {}
    for c in categories:
        noemer = 1 * P_cat(c,trainingsteksten)
        teller = 1
        for f in features1:
            if(features(f,woorden)):
                noemer = noemer * trained_model[1][c][f]
                teller = teller * trained_model[0][f]
        score_cat[c] = float(noemer)/teller
        print c
        print score_cat[c]
    
    return "schrijver"

def P_cat(category,tr_texts):
    """ Calculates the propability of a text to be of a given category, using a set of traintexts
    Args: String (category), List of Strings (list of traintexts)
    Returns: Float
    """
    tr_texts_cat = []
    for (text,c) in tr_texts:
        if(c==category):
            tr_texts_cat+=[(text,c)]
    return float(len(tr_texts_cat))/len(tr_texts)
    
def train(tr_texts,categories,features):
    """ Trains a classifier based on a set of given traintexts, categories and features.
    Args:List of Strings (tr-texts), List of Strings (categories), List of Strings (features)
    Returns:Tuple of Dictionaries (dict{feature:P_feature},dict{cat:{feature:P_feature_cat}})
    """
    P_features1 = P_features(features,tr_texts)
    P_features_cat1 =  P_features_cat(features,categories,tr_texts)
    return (P_features1,P_features_cat1)
    
def P_features_cat(features, categories, tr_texts):
    """ Calculates the propabilities of a list of features in a the given categories, based on the traintexts.
    Args:List of Strings (features), List of Strings (categories), List of Tuples (String,String) (traintexts (text,category))
    Returns: {String:{String:Float}} ({category:{feature:propability}})
    """
    kansen ={}
    for c in categories:
        kansen[c]={}
        
    for f in features:
        for c in categories:
            kansen[c][f]=P_feat_cat(f,c,tr_texts)
    return kansen
        
        
def P_feat_cat(feature,cat,tr_texts):
    """ Calculates the propability of a feature given a category, based on the traintexts.
    Args: String(feature), String(category), List of Tuples (String,String) (traintexts (text,cat))
    Returns: Float
    """
    tr_texts_cat = []
    for (text,c) in tr_texts:
        if(c==cat):
            tr_texts_cat+=[(text,c)]
    return P_feature(feature,tr_texts_cat)
    
def features(fs, text):
    """ Calculates if a features is applicable to a text.
    Args:String (featurename), String (text)
    Returns: Boolean
    """
    if(fs=="f1"): # ----------------------first feature
        return (len(text) > 100)
    elif(fs=="f2"):# ----------------------second feature
        return ("chapter" in text)
    elif (fs=="f3"):# ----------------------third feature
        return (len(text) < 80)

def P_feature(f, trainingsteksten):
    """ Calculates the propability of a feature, based on a list of traintexts
    Args: String (feature), List of Tuples (String,String) (traintexts (text,category))
    Returns: Float
    """
    voorkomens = 0
    for (tekst,cat) in trainingsteksten:
        if(features(f,tekst)):
            voorkomens += 1
    return float(voorkomens)/float(len(trainingsteksten))
    
def P_features(features, tr_teksten):
    """ Calculates the propability of features to appear in a text, based on a list of traintexts
    Args: List of Strings (features), List of Tuples (String,String) (traintexts (text,category))
    Returns: {String:Float} ({feature:propability})
    """
    kansen = {}
    for f in features:
        kansen[f]=P_feature(f,tr_teksten)
    return kansen

classify(wrds[:70])

def SentenceLengths(corpus):
    AverageLengths={}
    
    for (text,cat) in corpus:
        AverageLengths[cat]=[]
    
    for (text,cat) in corpus:
       sentences=[len(word_tokenize(t)) for t in sent_tokenize(text)]
       sentence_length_text = sum(sentences) / float(len(sentences))
       AverageLengths[cat].append(sentence_length_text)
      
    for cat in AverageLengths.keys():
        average_sentence_cat = sum(AverageLengths[cat])/float(len(AverageLengths[cat]))
        AverageLengths[cat] = average_sentence_cat
    
    return AverageLengths


print "\nAverage length of sentences by author:"
print SentenceLengths(corpus)


def Generate_BoW(text):
    # generated bag of words of one text
    return FreqDist(word_tokenize(text))
