from getcorpus import corpus
from classifier import train,classify,p_feat_cat,p_feature
from help_functions import *
from time import time
import pickle

corp=corpus(1)
authors = getauthors(corp)
features = ["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15"]  


def test():
    start = time()
    #print "length testdata:" + str(len(testdata))
    #print "length traindata:" +str(len(traindata))
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
    
#test()
def testfeatures(features,corp):
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

    
#testfeatures(["f1","f11"],corp)
#print "\nAverage length of sentences per author:"
#print SentenceLengths(corpus())


print bigramsdistr(corp[:50],20) # print de 20 meest voorkomende bigrammen van de eerste auteur (eerste 50 teksten)



 
    
    
