from getcorpus import corpus
from classifier import classify
from help_functions import *
from time import time

authors=["AaronPressman","AlanCrosby","AlexanderSmith","BenjaminKangLim","BernardHickey"]
features = ["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13"]  
corpus=corpus()

def test():
    start = time()
    #print "length testdata:" + str(len(testdata))
    #print "length traindata:" +str(len(traindata))
    correct = 0
    incorrect = 0
    runs = 0
    for i in range(0,5):
        data = split_train_test_data(authors, corpus,30)
        testdata = data["test"]
        traindata = data["train"]
        for j in range(0,len(testdata)):
            text = testdata[j]
            if (classify(text[0],traindata, features,authors)==text[1]):
                correct +=1
                runs +=1
            else:
                incorrect +=1
                runs +=1
                
    print "runs:" + str(runs)
    print "percentage correct:" + str(float(correct)/runs)
    print "runtime: " + str(time()-start) + " seconds"
    
    


test()

#print "\nAverage length of sentences per author:"
#print SentenceLengths(corpus())


"""
for a in authors:
    print "\n" +a + ":" 
    print_list(sorted(author_bow(a,corpus).items(), key=lambda x: x[1], reverse=True)[:30]) 
"""
    
    
    