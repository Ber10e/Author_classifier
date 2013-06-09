from getcorpus import corpus
from classifier import train,classify,p_feat_cat,p_feature,features as feat
from help_functions import *
from time import time
import operator
import pickle
import datetime
from math import *


corp=corpus(50)
compactcorpus = compactcorpus(corp)
authors = compactcorpus.keys()
chosenfeatures = []
chosenfeatures1 = [  "tri:('',he,said)>0",
                    "tri:(,,'',said)>0",
                    "tri:(,,'',he)>0",
                    "tri:(,,'',said)>0",
                    "tri:(the,indonesian,government)>0",
                    "tri:(billion,yen,()>0",
                    "tri:(.,he,said)>0"
                 ]

def test_features1(features):
    """
    Calculates the P(feature), P(feature|category) for every category, and the variance.
    """
    print "------------"
    for f in features:
        cat_feat_list=[]
        print "\n"
        print "P("+str(f)+")=\t"+ str(p_feature(f,corp))
        for cat in authors:
            print "P("+str(f)+"|"+str(cat)+")=\t"+ str(p_feat_cat(f,cat,corp))
            cat_feat_list.append(p_feat_cat(f,cat,corp))
        print "variance"+"("+str(f)+")=\t\t"+ str(variance(cat_feat_list))
    print "------------"   

def test_features2(features,num_rounds):
    """
    Tests the classifier on a set of features, returning it's precision
    """

    correct = {}
    for a in authors:
        correct[a]=0
    incorrect = 0
    runs = 0
    print "aantal features:" + str(len(features))
    print "testfeature:"+ str(features)

    for i in range(0,num_rounds):
        start = time()
        data = split_train_test_data(authors, corp,45)
        testdata = data["test"]
        traindata = data["train"]
        trained_model = train(traindata, authors, features)
        print "model trained in:" + str(time()-start) + "seconds"
        for j in range(0,len(testdata)):
            text = testdata[j]
            if (classify(text[0],trained_model, features,authors,traindata)==text[1]):
                correct[text[1]] +=1
                runs +=1
            else:
                incorrect +=1
                runs +=1    
    print "runs:"+str(runs)
    totalcorrect = 0
    for a in authors:
        totalcorrect += correct[a]
    print "correct:"+ str(totalcorrect)
    return float(totalcorrect)/runs

def pos_features():
    """
    Constructs a List of tuples of names and corresponding function (features)
    """
    trigrams = list(set([tri for (tri,num) in [x for sub in trigrams_dict(authors,corp,5).values()[3:] for x in sub]]))
    wrds = list(set(['internet']))
    minimal_wrdoccurence = ["wrd:"+wrd+">"+str(num) for wrd in wrds for num in range(0,1)]
    minimal_trigram_occurence = ["tri:("+str(tri[0])+","+str(tri[1])+","+str(tri[2])+")>"+str(num) for tri in trigrams for num in range(0,1)]
    features = minimal_trigram_occurence #+ minimal_word_occurence
    return features


def feature_selection(filename,basefeatures,features,num_rounds,num_selections):
    """
    test elke feature in een lijst van features (features), je kunt ook basefeatures toevoegen (deze worden niet getest, maar wel meegenomen).
    Ook moet je een aantal auteurs meegeven waarop je wilt testen, het aantal 'testronden', en het aantal te selecteren features.
    De features worden dan getest dmv testfeatures2, deze geeft een precision per feature, de hoogste n (n=num_selections) features worden naar het opgegeven bestand weggeschreven.
    Args:(String,List of features, List of features(string/naam, function), Integer, Integer, Integer)
    Returns: Ordered List of features + schrijft een textbestand
    """
    prec_dict = {}
    length = len(features)
    print "feature selection on: "+ str(length)+" features."
    for f in features:
        start = time()
        prec_dict[f] = test_features2((basefeatures+[f]),num_rounds)
        length = length - 1
        if((length % 5) ==0):
            print "Estimated time left:"+str(datetime.timedelta(seconds=(time()-start)*length))
    print "selection of "+str(num_selections)+ " has been made."
    selection = sorted(prec_dict.iteritems(), key=itemgetter(0), reverse=True)[:num_selections]
    print "writing to file:" + filename
    file = open(filename,'w')
    for (f,prec) in selection:
        file.write("["+str(f) +"]:" + str(prec) + "\n")
    file.close()
    return selection
    
    
    
    
print "go:\n"
print "aantal authors:"+str(len(authors))

print "------------"



#print feature_selection("trigram_feature_selection_all.txt",chosenfeatures,pos_features(),1,4)


print "build classifier"
classifier1 = (chosenfeatures, train(corp,authors,pos_features()))
print "write to file..."
writetofile(classifier1,"classifier1.c")
#print test_features2(pos_features(),2)
#print test_features2(pos_features(),4)



#print "\nAverage length of sentences per author:"
#print SentenceLengths(corpus())

#print bigramsdistr(corp[:50],20) # print de 20 meest voorkomende bigrammen van de eerste auteur (eerste 50 teksten)
"""
tri = trigrams_dict(authors,corp,3)
for a in tri.keys():
    print "\n" +a + ":\n"
    print_list(tri[a])
"""

    
