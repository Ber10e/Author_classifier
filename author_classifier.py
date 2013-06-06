from getcorpus import corpus
from classifier import train,classify,p_feat_cat,p_feature
from help_functions import *
from time import time
import pickle
import datetime
from math import *

corp=corpus(50)
print "corpus loaded..."
authors = getauthors(corp)
print "authors extracted..."
features0 = ["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15"]  
features = ["f1",(lambda x:(occurs_in_text(".",x)>4))]

def test():
    start = time()
    correct = {}
    for a in authors:
        correct[a]=0
    incorrect = 0
    runs = 0
    
    for i in range(0,10):
        data = split_train_test_data(authors, corp,49)
        testdata = data["test"]
        traindata = data["train"]
        trained_model = train(traindata, authors, features)
        
        for j in range(0,len(testdata)):
            text = testdata[j]
            if (classify(text[0],trained_model, features,authors,traindata)==text[1]):
                correct[text[1]] +=1
                runs +=1
                
            else:
                incorrect +=1
                runs +=1
        print runs       
    
    totalcorrect = 0
    for a in authors:
        print a+str(correct[a])
        totalcorrect += correct[a]
    print "runs:" + str(runs)
    print "percentage correct:" + str(float(totalcorrect)/runs)
    print "runtime: " + str(time()-start) + " seconds"
    

def testfeatures1(features,corp):
    """
    Calculates the P(feature), P(feature|category) for every category, and the variance.
    """
    dict = compactcorpus(corp)
    print "------------"
    for f in features:
        cat_feat_list=[]
        print "\n"
        print "P("+f+")=\t"+ str(p_feature(f,corp))
        for cat in dict.keys():
            print "P("+f+"|"+str(cat)+")=\t"+ str(p_feat_cat(f,cat,corp))
            cat_feat_list.append(p_feat_cat(f,cat,corp))
        print "variance"+"("+str(f)+")=\t\t"+ str(variance(cat_feat_list))
    print "------------"   

def test_features2(features,num_authors,num_rounds):
    """
    Tests the classifier on a set of features, returning it's precision
    """
    corp = corpus(num_authors)
    authors = getauthors(corp)
    correct = {}
    for a in authors:
        correct[a]=0
    incorrect = 0
    runs = 0
    
    for i in range(0,num_rounds):
        data = split_train_test_data(authors, corp,49)
        testdata = data["test"]
        traindata = data["train"]
        trained_model = train(traindata, authors, features)
        
        for j in range(0,len(testdata)):
            text = testdata[j]
            if (classify(text[0],trained_model, features,authors,traindata)==text[1]):
                correct[text[1]] +=1
                runs +=1
            else:
                incorrect +=1
                runs +=1          
    
    totalcorrect = 0
    for a in authors:
        totalcorrect += correct[a]
    return float(totalcorrect)/runs

def pos_features():
    """
    Constructs a List of tuples of names and corresponding function
    """
    minimal_wrd_occurence = [(("wrdoccurence:"+wrd+">"+str(num)),(lambda text: (occurs_in_text(wrd,text) >num ))) for wrd in ["internet","to", "by","at"] for num in range(0,10)]
    features = minimal_wrd_occurence
    return features

def feature_selection(basefeatures,features,num_authors,num_rounds,num_selections):
    prec_dict = {}
    length = len(features) +1
    print "checking "+ str(length-1)+" features."
    for (name,f) in features:
        start = time()
        prec_dict[(name,f)] = test_features2((basefeatures+[f]),num_authors,num_rounds)
        print name + str(prec_dict[(name,f)])
        length = length - 1
        if((length % 5) ==0):
            print "Estimated time left:"+str(datetime.timedelta(seconds=(time()-start)*length))
    print "selection of "+str(num_selections)+ " has been made."
    selection = sorted(prec_dict.iteritems(), key=itemgetter(1), reverse=True)[:num_selections]
    return selection
    
    
    
    
print "go:\n"

print feature_selection([],pos_features(),5,1,10)
#test_features2(features,10,10)


#testfeatures1(["f1","f11"],corp)
#print "\nAverage length of sentences per author:"
#print SentenceLengths(corpus())


#print bigramsdistr(corp[:50],20) # print de 20 meest voorkomende bigrammen van de eerste auteur (eerste 50 teksten)



 
    
    
