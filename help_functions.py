from nltk import FreqDist,bigrams
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
import random
from getcorpus import corpus
from operator import itemgetter



def printgeg(): # print wat gegevens over het corp
    wrds = corpus(5)
    print "type/token ratio vijf auteurs:"
    tt_ratio = float(len(wrds))/float(len(set(wrds)))
    print tt_ratio
    print "documentlengte/aantal woorden:"
    print len(wrds)

def Generate_BoW(text):
    # generated bag of words of one text
    return FreqDist(word_tokenize(text.lower()))

def split_train_test_data(classes, corp, num_train):
    """splitst het corp in een train deel (lengte te bepalen) en een testset
    """
    train_texts = []
    test_texts = []
    num_author = {}
    random.shuffle(corp,random.random)
    #print len(corp)
    for author in classes:
        num_author[author] = 0
    for (text,author) in corp:
        if (num_author[author]<num_train):
            train_texts += [(text,author)]
            num_author[author] += 1
        else:
            test_texts += [(text,author)]
    return {"test":test_texts,"train": train_texts} 

def print_list(list):
    """ prints a list"""
    for (x,y) in list:
        print x + "\t\t" + str(y)
               
def avglength(corp):
    count = 0
    number = 0
    for (text,y) in corp:
        count += len(word_tokenize(text))
        number += 1
    return float(count) / number
    
def SentenceLengths(corp):
    AverageLengths={}
    
    
    for (text,cat) in corp:
        AverageLengths[cat]=[]
    
    for (text,cat) in corp:
       sentences=[len(word_tokenize(t)) for t in sent_tokenize(text)]
       sentence_length_text = sum(sentences) / float(len(sentences))
       AverageLengths[cat].append(sentence_length_text)
      
    for cat in AverageLengths.keys():
        average_sentence_cat = sum(AverageLengths[cat])/float(len(AverageLengths[cat]))
        AverageLengths[cat] = average_sentence_cat
    
    return AverageLengths

def save_list_to_file(list,file):
    f = open(file,'w')
    for (x,y) in freqs:
        f.write(x +"\t\t" +y + "\n")
    f.close()
    
def numberoftexts_cat(author,texts):
    """counts the number of texts of a given author"""
    count = 0
    for (text,cat) in texts:
        if(cat == author):
            count +=1
    return count 

def occurs_in_text(word,text):
    """return the number of times the word occurs in the text"""
    count = 0
    for w in text.split():
        if(w==word):
            count +=1
    return count
    
def author_bow(author,corp):
    """for given author, builds a dictionary:
    keys: used words
    values: list of occurences in texts
    then calculates the weighed occurence of all words (number of times that word is used in one text)
    """

    author_freqd={}
    numb_texts=numberoftexts_cat(author,corp)
    
    for (text,cat) in corp:
        if cat==author:
            freqd=Generate_BoW(text)

            for word in freqd.keys():
                if word in author_freqd.keys():
                    author_freqd[word].append(freqd[word])
                else:
                    author_freqd[word]=[freqd[word]]
    
    for word in author_freqd.keys():
        weighed_occurence=float(sum(author_freqd[word]))/numb_texts
        author_freqd[word]=weighed_occurence

    return author_freqd

def getauthors(corp):
    authors =[]
    for (x,a) in corp:
        authors.append(a)
    return list(set(authors))

def compactcorpus(corp):
    dict = {}
    for (t,c) in corp:
        if not(c in dict.keys()):
            dict[c] = [(t,c)]
        else:
            dict[c].append((t,c))
    return dict

def variance(list):
    n = 0
    sum = 0
    sum_sqr = 0
 
    for x in list:
        n = n + 1
        sum = sum + x
        sum_sqr = sum_sqr + x*x
 
    variance = (sum_sqr - ((sum*sum)/n))/(n - 1)
    return variance

def bigramsdistr(corp,num):
    bigrams0 = []
    for (text,author) in corp:
        bigrams0 += bigrams(word_tokenize(text.lower()))
    return sorted(FreqDist(bigrams0).iteritems(), key=itemgetter(1), reverse=True) [:num]

def trigramsdistr(corp,num):
    trigrams0 = []
    for (text,author) in corp:
        trigrams0 += trigrams(word_tokenize(text.lower()))
    return sorted(FreqDist(trigrams0).iteritems(), key=itemgetter(1), reverse=True) [:num]

def bigrams_author(author,corp,num):
    ccorp = compactcorpus(corp)
    bigrams0 = []
    
    for (text,cat) in ccorp[author]:
        bigrams0 += bigrams(word_tokenize(text.lower()))

    return sorted(FreqDist(bigrams0).iteritems(), key=itemgetter(1), reverse=True) [:num]

def trigrams_author(author,corp,num):
    ccorp = compactcorpus(corp)
    trigrams0 = []
    
    for (text,cat) in ccorp[author]:
        trigrams0 += trigrams(word_tokenize(text.lower()))

    return sorted(FreqDist(trigrams0).iteritems(), key=itemgetter(1), reverse=True) [:num]
