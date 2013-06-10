"""Kort stukje code dat laat zien hoe je prob_classify kunt gebruiken om de probability scores van een testdocument voor de verschillende categorieen te krijgen.
"""

import nltk.tokenize as tokenize
import nltk
import random

"""Laadt corpus"""
movie_reviews = nltk.corpus.movie_reviews 

documents = [(set(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)

"""Feature extraction: Laat enkel 2000 meest frequente woorden toe"""
def document_features(document): 
    """
    return: dict{string:Bool}
    """
    
    features = {}
    for word in word_features:
        features[word] = (word in document)
    return features

all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = all_words.keys()[:2000]

"""Selecteer training set"""
train_set = [(document_features(d), c) for (d, c) in documents[:200]]

"""Train classifier"""
classifier = nltk.NaiveBayesClassifier.train(train_set)

"""Zelfgeschreven `testdocumenten'"""
tests = ["this city",
         "i love this city",
         "i hate this city"]

"""Zet de woorden in de testdocumenten om in dictionary. OPM: Gebruik niet document_features functie wegens independence assumptie van Naive Bayes"""
def bag_of_words(words):
    return dict([word, True] for word in words)

"""Print de probability scores van de verschillende testdocumenten per categorie."""
for test in tests:
    words = tokenize.word_tokenize(test)
    feats = bag_of_words(words)
    print feats
    print('{s} => Pos label has prob of {c1}; Neg label has prob of {c2}'.format(s = test, c1 = classifier.prob_classify(feats).prob('pos'), c2= classifier.prob_classify(feats).prob('neg')))
          
 

 
