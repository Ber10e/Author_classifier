"""
Groepsopdracht2:
Bertine
Tuur
Erlinde
Jelte
"""

from nltk.corpus import gutenberg
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

def classify(woorden):
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
    tr_texts_cat = []
    for (text,c) in tr_texts:
        if(c==category):
            tr_texts_cat+=[(text,c)]
    return float(len(tr_texts_cat))/len(tr_texts)
    
def train(tr_texts,categories,features):
    P_features1 = P_features(features,tr_texts)
    P_features_cat1 =  P_features_cat(features,categories,tr_texts)
    return (P_features1,P_features_cat1)
    
    
def P_features_cat(features, categories, tr_texts):
    kansen ={}
    for c in categories:
        kansen[c]={}
        
    for f in features:
        for c in categories:
            kansen[c][f]=P_feat_cat(f,c,tr_texts)
    return kansen
        
        
def P_feat_cat(feature,cat,tr_teksten):
    tr_texts_cat = []
    for (text,c) in tr_teksten:
        if(c==cat):
            tr_texts_cat+=[(text,c)]
    return P_feature(feature,tr_texts_cat)
    
def features(fs, woorden):
    if(fs=="f1"):
        return (len(woorden) > 100)
    elif(fs=="f2"):
        return ("chapter" in woorden)
    elif (fs=="f3"):
        return (len(woorden) < 80)

def P_feature(f, trainingsteksten):
    voorkomens = 0
    for (tekst,cat) in trainingsteksten:
        if(features(f,tekst)):
            voorkomens += 1
    return float(voorkomens)/float(len(trainingsteksten))
    
def P_features(features, tr_teksten):
    kansen = {}
    for f in features:
        kansen[f]=P_feature(f,tr_teksten)
    return kansen


    
    
    
classify(wrds[:70])
