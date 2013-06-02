from getcorpus import corpus
from classifier import classify
from help_functions import *


def split_train_test_data(classes, corpus, num_train):
    """splitst het corpus in een train deel (lengte te bepalen) en een testset
    """
    train_texts = []
    test_texts = []
    num_author = {}
    print len(corpus)
    for author in classes:
        num_author[author] = 0
    for (text,author) in corpus:
        if (num_author[author]<num_train):
            train_texts += [(text,author)]
            num_author[author] += 1
        else:
            test_texts += [(text,author)]
    return {"test":test_texts,"train": train_texts} 


def test():
    data = split_train_test_data(authors, corpus(),40)
    testdata = data["test"]
    traindata = data["train"]
    #print "length testdata:" + str(len(testdata))
    #print "length traindata:" +str(len(traindata))
    text = testdata[7]
    print text[0].lower().split()[:30]
    print ("\nTEXT OF: " + text[1])
    classify(text[0],traindata, features,authors)
    
    
# lijst gewenste auteurs
authors=["AaronPressman","AlanCrosby","AlexanderSmith","BenjaminKangLim","BernardHickey"]
features = ["f1","f2","f3","f4","f5","f6","f7","f8"]   
    
test()

print "\nAverage length of sentences per author:"
#print SentenceLengths(corpus())

corpus=corpus()
"""
for a in authors:
    print a + ":\n"
    print sorted(author_bow(a,corpus).items(), key=lambda x: x[1], reverse=True)[:30]  
""" 
    
    
    