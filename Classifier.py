"""
Groepsopdracht2:
Bertine
Tuur
Erlinde
Jelte
"""

from features import features

def classify(text, trained_model, features1, categories,tr_texts):
    """ Classifies a text based on the trainingstexts, categories and features.
    Args: String (a text), List of Tuples (String,String), List of Strings, List of Strings
    Returns: String (prints propabilities per category)
    """
    if (trained_model == []):
        trained_model = train(tr_texts, categories, features1)
    #print trained_model[0]
    #print trained_model[1]
    score_cat = {}
    for c in categories:
        noemer = 1 * P_cat(c,tr_texts)
        teller = 1
        for f in features1:
            if(features(f,text)):
                noemer = noemer * trained_model[1][c][f]
                teller = teller * trained_model[0][f]
        score_cat[c] = float(noemer)/teller
        #print c
        #print score_cat[c]
    result = "false"
    max_score = (1.0/len(categories))
    for c in categories:
        if (score_cat[c]>max_score):
            result = c
            max_score = score_cat[c]
    #print "CLASSIFIED AS: " + result
    return result

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

