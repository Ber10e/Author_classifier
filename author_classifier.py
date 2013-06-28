from getcorpus import corpus
from classifier import train,p_feat_cat,p_feature
from features import *
from help_functions import *
import time
from nltk import NaiveBayesClassifier
import nltk
import operator
import pickle
import datetime
from math import *
import winsound
from time import time,sleep
import webbrowser
import os

corp=corpus(50)
#corp = lemmatize_corpus(corp0)
#writetofile(corp,"lemmatized_corpus.pkl")
compactcorpus = compactcorpus(corp)

print "corpus build"
authors = compactcorpus.keys()

def document_features(document): 
    features = {}
    for word in word_features:
        features[word] = (word in document)
    return features
    
def pos_features(compactcorpus):
    """
    Hier staan alle features die op dit moment gebruikt 
    """
    start=time()
    
    wrds = common_but_unique(ngrams_dict(1,authors,compactcorpus,25,False),8)
    bigrams = common_but_unique(ngrams_dict(2,authors,compactcorpus,25,False),8)
    trigrams = common_but_unique(ngrams_dict(3,authors,compactcorpus,25,False),8)
    #tag_bigrams =common_but_unique(ngrams_dict(2,authors,compact_to_tag(compactcorpus),20,False),15) #PAS OP Duurt erg lang om te gebruiken (dus ook nog niet getest...ivm tijd)
    skipgrams = common_but_unique(skipgrams_dict(authors,compactcorpus,10),10)

    minimal_wrdoccurence = ["wrd:"+wrd+">"+str(num) for wrd in wrds for num in range(0,1)]
    minimal_trigram_occurence = ["tri:("+str(tri[0])+","+str(tri[1])+","+str(tri[2])+")>"+str(num) for tri in trigrams for num in range(0,1)]
    minimal_bigram_occurence = ["bi:("+str(bi[0])+","+str(bi[1])+")>"+str(num) for bi in bigrams for num in range(0,1)]
    #minimal_skipgram_occurence = ["skip:("+str(skip[0])+","+str(skip[1])+","+str(skip[2])+")>"+str(num) for skip in skipgrams for num in range(0,1)]

    features = minimal_bigram_occurence +  minimal_wrdoccurence + minimal_trigram_occurence #+ minimal_skipgram_occurence
    print "pos feat in:"+str(time()-start)
    return features
        
def feat_dict(pos_feat,text):
    """
    Geeft het dictionary van alle features toegepast in een text.
    """
    dict = {}
    bigrams = ngrams(word_tokenize(text),2)
    trigrams = ngrams(word_tokenize(text),3)
    
    for feat in pos_feat:
        dict[feat]=features(feat,text,bigrams,[],[])
    return dict    
    
def classifynltk():
    pos_feat = pos_features(compactcorpus)
    print "aantal features:"+str(len(pos_feat))
    print "aantal auteurs:" + str(len(authors))
    data = split_train_test_data(authors, corp,45)
    print "data splitted"
    start = time()
    print "starting with training...good luck.. enjoy some nice music!"
    #webbrowser.open("http://radioplayer.omroep.nl/radio4-default/",2)    
    train_set = [(feat_dict(pos_feat,d), c) for (d, c) in data["train"]]
    print "train set build in "+str(time()-start)+" seconds"
    test_set = [(feat_dict(pos_feat,d), c) for (d, c) in data["test"]]
    print "test set build"
    classifier1 = NaiveBayesClassifier.train(train_set)
    writetofile((classifier1,pos_feat),"classifiertest.pkl")
    print "classifier build"
    print "written to file 'classifiertest.pkl'"
    
    classified=[]
    actual=[]
    correctcounter = 0

    for (text,cat) in data["test"]:
        feats = feat_dict(pos_feat,text)
        classified.append(classifier1.classify(feats))
        actual.append(cat)
        if classifier1.classify(feats) == cat:
            correctcounter+=1

    print "Runtime: "+str(time()-start)
    print "\n==============="
    print "Accuracy: "+str(correctcounter/float(len(classified)))
    print "===============\n"

    #confusion matrix
    cm = nltk.ConfusionMatrix(actual,classified)
    matrixfile="errormatrix"+str(time())+".txt"
    print "Writing error matrix to: "+matrixfile
    f = open(matrixfile,"w")
    f.write(cm.pp())
    f.close()
    os.startfile(matrixfile)
    
    
    #print nltk.classify.accuracy(classifier1,test_set)
    #zelda()
    classifier1.show_most_informative_features(10) 
    winsound.Beep(2000,1000)

    
def optimalize():
    """
    test gegeven een lijst testparameters (check) de prestatie van de classifier
    """ 
    start = time()
    max = 0
    maxn=2
    maxm=3
    check = [(n,m) for n in range(24,30) for m in range(3,20)]
    dict = {}
    print "start optimalization of: bigram-features,uniqueness"
    for n,m in check:
        score=0
        print ">lem>>n(uniqueness):"+str(n)
        print ">lem>>m(commonness):"+str(m)
        wrds = common_but_unique(ngrams_dict(1,authors,compactcorpus,n,False),m)
        bigrams = common_but_unique(ngrams_dict(2,authors,compactcorpus,n,False),m)
        trigrams = common_but_unique(ngrams_dict(3,authors,compactcorpus,n,False),m)
        #pos_feat = ["wrd:"+wrd+">"+str(num) for wrd in wrds for num in range(0,1)]
        pos_feat = ["bi:("+str(bi[0])+","+str(bi[1])+")>"+str(num) for bi in bigrams for num in range(0,1)] + ["wrd:"+wrd+">"+str(num) for wrd in wrds for num in range(0,1)] + ["tri:("+str(tri[0])+","+str(tri[1])+","+str(tri[2])+")>"+str(num) for tri in trigrams for num in range(0,1)]

        print "number of features AFTER selection:" + str(len(pos_feat))
        for x in range(0,4):
            data = split_train_test_data(authors, corp,45)
            train_set = [(feat_dict(pos_feat,d), c) for (d, c) in data["train"]]
            train_set = [(feat_dict(pos_feat,d), c) for (d, c) in data["train"]]
            test_set = [(feat_dict(pos_feat,d), c) for (d, c) in data["test"]]
            classifier1 = NaiveBayesClassifier.train(train_set)
            acc = nltk.classify.accuracy(classifier1,test_set)
            print "accuracy:"+str(acc)
            score +=acc
        print "time elapsed: "+str(time()-start)
        print "score(" + str(n) +")="+str(score/4)
        classifier1.show_most_informative_features(8)
        dict[(n,m)]=(score/4)
        if(score/4)>max:
            max = (score/4)
            maxn =n
            maxm = m
    print "max score="+str(max)
    print "where n = "+str(maxn)
    print "where m = "+str(maxm)
    print "time:"+str(time()-start)
    writetofile(dict,"optimalizedict_commonwrdsandbigrams_latest_lem.pkl")


   
def test_features1(features):
    """
    for the homemade classifier:
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
    Tests the (homemade)classifier on a set of features, returning it's precision
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
    voor de home made classifier:
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
#print "aantal authors:"+str(len(authors))
print "------------"


classifynltk()
#optimalize()

"""    
test = "BOSTON, June 6 (Reuters) - Investors may have overreacted recently to the possibility of the U.S. Federal Reserve winding down its asset-buying stimulus, a top U.S. central bank official said on Thursday. U.S. bond and stock markets abruptly sold off on May 22 when Fed Chairman Ben Bernanke told a congressional committee that the central bank's $85 billion in monthly purchases could be reduced 'in the next few meetings' of the Fed's policy committee if the economy continues to gain traction."
test2 = "NEW YORK (Reuters) - Barry Rosenstein's JANA Partners liked grocery chain Supervalu Inc in a big way in the first quarter, while Philippe Laffont's Coatue Management lost its stomach for the company's shares. Regulatory filings revealed that JANA, a hedge fund with $5.5 billion in assets, picked up some 14 million shares of Supervalu in the quarter ended March 31. For Laffont's 9$.5 billion firm, however, it was a different story, as the hedge fund dumped all of its roughly 10 million shares."
testc = (test)
go = feat_dict(pos_features(compactcorpus),test2)
classifier0 = getfromfile("classifier_lem_1247feat_0,776ac.pkl")

thing = classifier0.prob_classify(go)
for sample in thing.samples():
    print sample + "\t :"+ str(thing.prob(sample))

print "classified as:"
print classifier0.classify(go)
"""
