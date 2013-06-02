from getcorpus import corpus
from classifier import classify
from help_functions import *
from time import time
import pickle


authors=["AaronPressman","AlanCrosby","AlexanderSmith","BenjaminKangLim","BernardHickey"]
features = ["f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12","f13","f14","f15"]  
corpus=corpus()

def test():
    start = time()
    #print "length testdata:" + str(len(testdata))
    #print "length traindata:" +str(len(traindata))
    correct = {}
    for a in authors:
        correct[a]=0
    incorrect = 0
    runs = 0
    
    for i in range(0,8):
        data = split_train_test_data(authors, corpus,45)
        testdata = data["test"]
        traindata = data["train"]
        
        for j in range(0,len(testdata)):
            text = testdata[j]
            if (classify(text[0],traindata, features,authors)==text[1]):
                correct[text[1]] +=1
                runs +=1
                print runs
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
    
    


test()

#print "\nAverage length of sentences per author:"
#print SentenceLengths(corpus())
"""
def save_to_file(list,file):
    f = open(file,'w')
    for (x,y) in freqs:
        f.write(x +"\t\t" +y + "\n")
    f.close()
freqs = []
for a in authors:
    print "\n" +a + ":" 
    freqs += [("Author:\t\t",str(a))]
    print_list(sorted(author_bow(a,corpus).items(), key=lambda x: x[1], reverse=True)[:20]) 
    freqs+= [(str(x),str(y)) for (x,y) in (sorted(author_bow(a,corpus).items(), key=lambda x: x[1], reverse=True)[:20])]
save_to_file(freqs,"freqs.txt")
"""

 
    
    