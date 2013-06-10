from getcorpus import corpus
from classifier import train,p_feat_cat,p_feature
from features import *
from help_functions import *
from time import time
from nltk import NaiveBayesClassifier
import nltk
import operator
import pickle
import datetime
from math import *
import winsound


corp=corpus(50)
compactcorpus = compactcorpus(corp)
authors = compactcorpus.keys()


def document_features(document): 
    features = {}
    for word in word_features:
        features[word] = (word in document)
    return features
    
def pos_features():
    """
    Hier staan alle features die op dit moment gebruikt 
    """
    start=time()
    bigrams = common_but_unique(bigrams_dict(authors,corp,20),3)
    trigrams = common_but_unique(trigrams_dict(authors,corp,20),3)

    wrds = list(set())
    minimal_wrdoccurence = ["wrd:"+wrd+">"+str(num) for wrd in wrds for num in range(0,1)]
    minimal_trigram_occurence = ["tri:("+str(tri[0])+","+str(tri[1])+","+str(tri[2])+")>"+str(num) for tri in trigrams for num in range(0,1)]
    minimal_bigram_occurence = ["bi:("+str(bi[0])+","+str(bi[1])+")>"+str(num) for bi in bigrams for num in range(0,1)]

    features = minimal_trigram_occurence + minimal_bigram_occurence
    print "pos feat in:"+str(time()-start)
    return features
    
    
def feat_dict(pos_feat,text):
    """
    Geeft het dictionary van alle features toegepast in een text.
    """
    dict = {}
    
    for feat in pos_feat:
        dict[feat]=features(feat,text)
    return dict    
    
def classifynltk():
    pos_feat = pos_features()
    print "aantal features:"+str(len(pos_feat))
    winsound.Beep(2000,2000)
    data = split_train_test_data(authors, corp,45)
    print "data splitted"
    start = time()
    train_set = [(feat_dict(pos_feat,d), c) for (d, c) in data["train"]]
    print "train set build in "+str(time()-start)+" seconds"
    writetofile(train_set,"train_set_superveelfeat.pkl")
    winsound.Beep(2000,2000)
    print "written to file"
    test_set = [(feat_dict(pos_feat,d), c) for (d, c) in data["test"]]
    print "test set build"
    winsound.Beep(2000,2000)
    classifier1 = NaiveBayesClassifier.train(train_set)
    print "classifier build"
    print nltk.classify.accuracy(classifier1,test_set)
    



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

def test_features2(features,num_rounds,file):
    """
    Tests the classifier on a set of features, returning it's precision
    """
    correct = {}
    for a in authors:
        correct[a]=0
    runs = 0
    print "aantal features:" + str(len(features))
    print "testfeature:"+ str(features)
    for i in range(0,num_rounds):
        
        start = time()
        data = split_train_test_data(authors, corp,45)
        testdata = data["test"]
        traindata = data["train"]
        if(file==""):
            trained_model = train(traindata, authors, features)
            print "model trained in:" + str(time()-start) + "seconds"
        else:
            trained_model = getfromfile(file)[1]
            writetofile((features,trained_model),"classifier2.c")
            print "trained model extracted from" + file
        print "number of runs:"+str(len(testdata))
        winsound.Beep(2000,500)
        print "starting with classifications..."
        for j in range(0,len(testdata)):
            start=time()
            if (classify(testdata[j][0],trained_model, features,authors,traindata)==testdata[j][1]):
                correct[testdata[j][1]] +=1
                runs +=1
            else:
                runs +=1
            print "runtime:" + str(time()-start)
    print "runs:"+str(runs)
    totalcorrect = 0
    for a in authors:
        totalcorrect += correct[a]
    print "correct:"+ str(totalcorrect)
    return float(totalcorrect)/runs

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
        prec_dict[f] = test_features2((basefeatures+[f]),num_rounds,"")
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
    
    
    
    
print "go:"
print "aantal authors:"+str(len(authors))
print "------------"



classifynltk()


    
