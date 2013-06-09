from getcorpus import corpus
from classifier import train,classify,p_feat_cat,p_feature,features as feat
from help_functions import *
from time import time
import operator
import pickle
import datetime
from math import *

corp=corpus(2)
print "corpus loaded..."
authors = getauthors(corp)
print "authors extracted..."
features = ["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15"]  

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
        print "P("+str(f)+")=\t"+ str(p_feature(f,corp))
        for cat in dict.keys():
            print "P("+str(f)+"|"+str(cat)+")=\t"+ str(p_feat_cat(f,cat,corp))
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
    
    print "aantal features:"+ str(len(features))
    for i in range(0,num_rounds):
        data = split_train_test_data(authors, corp,40)
        testdata = data["test"]
        traindata = data["train"]
        trained_model = train(traindata, authors, features)
        
        for j in range(0,len(testdata)):
            text = testdata[j]
            if (classify(text[0],trained_model, features,authors,traindata)==text[1]):
                print correct[text[1]]
                correct[text[1]] +=1
                runs +=1
            else:
                incorrect +=1
                runs +=1          

    totalcorrect = 0
    for a in authors:
        totalcorrect += correct[a]
    print "correct:"+ str(totalcorrect)
    return float(totalcorrect)/runs

def pos_features(): # WERKT NIET!
    """
    Constructs a List of tuples of names and corresponding function (features)
    """
    trigrams1 = list(set([tri for (tri,num) in [x for sub in trigrams_dict(authors,corp,3).values() for x in sub]]))
    #wrds = list(set(['internet']))
    #minimal_wrd_occurence = [(("wrdoccurence:"+wrd+">"+str(num)),(lambda text: (wrd_occurs_in_text(wrd,text) >num ))) for wrd in wrds for num in range(0,2)]

    #minimal_trigram_occurence = [(("trigramoccurence:"+str(tri)+">"+str(num)),(lambda tex: (trigram_occurs_in_text(tri,tex) >num ))) for tri in trigrams1 for num in range(0,1)]
   # features = minimal_trigram_occurence
    features = [(f[0],f[1](f[2])(f[0]))for f in [(tri,(lambda n :lambda t: lambda x: (trigram_occurs_in_text(t,x) >n)),num) for tri in trigrams1 for num in range(0,1)]]

    return features
    


def feature_selection(filename,basefeatures,features,num_authors,num_rounds,num_selections):
    """
    test elke feature in een lijst van features (features), je kunt ook basefeatures toevoegen (deze worden niet getest, maar wel meegenomen).
    Ook moet je een aantal auteurs meegeven waarop je wilt testen, het aantal 'testronden', en het aantal te selecteren features.
    De features worden dan getest dmv testfeatures2, deze geeft een precision per feature, de hoogste n (n=num_selections) features worden naar het opgegeven bestand weggeschreven.
    Args:(String,List of features, List of features(string/naam, function), Integer, Integer, Integer)
    Returns: Ordered List of features + schrijft een textbestand
    """
    prec_dict = {}
    length = len(features) +1
    print "checking "+ str(length-1)+" features."
    for (name,f) in features:
        start = time()
        prec_dict[(name,f)] = test_features2((basefeatures+[f]),num_authors,num_rounds)
        #print name + str(prec_dict[(name,f)])
        length = length - 1
        if((length % 5) ==0):
            print "Estimated time left:"+str(datetime.timedelta(seconds=(time()-start)*length))
    print "selection of "+str(num_selections)+ " has been made."
    selection = sorted(prec_dict.iteritems(), key=itemgetter(1), reverse=True)[:num_selections]
    print "writing to file:" + filename
    file = open(filename,'w')
    for ((name,f),prec) in selection:
        file.write("["+name +"]:" + str(prec) + "\n")
    file.close()
    return selection
    
    
    
    
#print "go:\n"
#print pos_features()
#print "----"

for (x,y) in pos_features():
    print (x,y)
    print y(corp[0][0])
    #print trigram_occurs_in_text((",","''","said"),corp[3][0])

pos_features() 
print trigramsdistr(corp[:1],3)
#print feature_selection("featuretest.txt",[],pos_features(),5,10,15)
print test_features2([f for (x,f) in pos_features()],2,1)
#print testfeatures1([f for (x,f) in pos_features()],corp)

#testfeatures1(["f1","f11"],corp)
#print "\nAverage length of sentences per author:"
#print SentenceLengths(corpus())


#print bigramsdistr(corp[:50],20) # print de 20 meest voorkomende bigrammen van de eerste auteur (eerste 50 teksten)

tri = trigrams_dict(authors,corp,3)
for a in tri.keys():
    print "\n" +a + ":\n"
    print_list(tri[a])


    
