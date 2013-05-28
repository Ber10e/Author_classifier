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
    category = ["lang", "kort"]
    features = ["f1","f2"]    
    print P_features(features,trainingsteksten)
    
    return "schrijver"



def P_feat_cat(feature,cat,tr_teksten):
    tr_teksten_cat = [(tekst,cat) in tr_teksten]
    voorkomens = 0
    for (text,cat) in tr_teksten_cat:
        if(features(feature,text)):
            voorkomens += 1
    return float(voorkomens)/len(tr_teksten_cat)
    
def features(fs, woorden):
    if(fs=="f1"):
        return (len(woorden) > 100)
    elif(fs=="f2"):
        return ("chapter" in woorden)

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


    
    
    
classify(["YO!"])