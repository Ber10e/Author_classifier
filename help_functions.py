from nltk import FreqDist,bigrams, trigrams, ngrams
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from nltk.corpus import stopwords
import random
import pickle
from getcorpus import corpus
from operator import itemgetter
import csv
import time
import winsound


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
    """ prints sorted frequency distributions"""
    for (x,y) in list:
        print str(x) + "\t\t" + str(y)
               
def avglength(corp):
    count = 0
    number = 0
    for (text,y) in corp:
        count += len(word_tokenize(text))
        number += 1
    return float(count) / number
    
def writetofile(struct,file):
    f = open(file,'wb')
    pickle.dump(struct,f)
    f.close
def getfromfile(file):
    f = open(file,'rb')
    struct = pickle.load(f)
    f.close
    return struct

def lengths(authors,corp):
    ccorp = compactcorpus(corp)
    lengths0={}

    for author in authors:
        concattext = ''
        for (text,cat) in ccorp[author]:
            concattext += text
        
        sentencelengths = [len(word_tokenize(t)) for t in sent_tokenize(concattext)]
        average_sentence = sum(sentencelengths)/float(len(sentencelengths))
        lengths0[author]=[average_sentence]

        wordlengths = [len(word) for word in word_tokenize(concattext)]
        average_word = sum(wordlengths)/float(len(wordlengths))
        lengths0[author].append(average_word)

        #print "\n"+author+"\n==============\n"+str(average_sentence)+"\n"+str(average_word)

    return lengths0

def save_list_to_file(list,file):
    f = open(file,'w')
    for x in list:
        f.write(str(x) + "\n")
    f.close()
    
def numberoftexts_cat(author,texts):
    """counts the number of texts of a given author"""
    count = 0
    for (text,cat) in texts:
        if(cat == author):
            count +=1
    return count 

def wrd_occurs_in_text(word,text):
    """return the number of times the word occurs in the text"""
    count = 0
    for w in text.split():
        if(w==word):
            count +=1
    return count
    
def bigram_occurs_in_text(bigram,text):
    """return the number of times the bigram occurs in the text"""
    count = 0
    textlist = word_tokenize(text.lower())
    for i in range(0,len(textlist)-2):
        if (textlist[i],textlist[i+1])==bigram:
            count +=1
    return count 
    
def trigram_occurs_in_text(trigram,text):
    """return the number of times the trigram occurs in the text"""
    count = 0
    textlist = word_tokenize(text.lower())
    for i in range(0,len(textlist)-3):
        if (textlist[i],textlist[i+1],textlist[i+2])==trigram:
            count +=1
    return count    
    
def common_but_unique(dict,uniqueness):
    pile = []
    for a in dict.keys():
        pile +=[x[0] for x in dict[a]]
    fdist = sorted(FreqDist(pile).iteritems(), key=itemgetter(1), reverse=False)
    return [feat for (feat,x) in fdist if x<uniqueness]
    
def getauthors(corp):
    authors =[]
    for (x,a) in corp:
        authors.append(a)
    return list(set(authors))

def compactcorpus(corp):
    """
    maakt een dictionary{auteur:[(text,auteur)]}
    """
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

   
def ngrams_author(n,author,compcorp,num,removestopwords):
    """ finds top n-grams for one author
    args: n for n-grams, author, compacted corpus, number top n-grams,boolean(removestopwords)
    returns: frequency distribution of n-grams for given author"""
    ngrams0=[]
    
    if n==1:
        for (text,cat) in compcorp[author]:
            if removestopwords:
                ngrams0 += remove_stopwords(word_tokenize(text.lower()))
            else:
                ngrams0 += word_tokenize(text.lower())
    
    else:
        for (text,cat) in compcorp[author]:
            if removestopwords:
                ngrams0 += ngrams(remove_stopwords(word_tokenize(text.lower())),n)
            else:
                ngrams0 += ngrams(word_tokenize(text.lower()),n)

    return sorted(FreqDist(ngrams0).iteritems(), key=itemgetter(1), reverse=True) [:num]


def ngrams_dict(n,authors,compcorp,num,removestopwords):
    """ finds top n-grams for all authors
    args: n for n-grams,list of authors,corpus,number top n-grams,boolean(removestopwords)
    returns: dictionary {author: [(ngram,occurence)]}"""
    #compcorp = compactcorpus(corp)
    dict={}
    
    for author in authors:
        if removestopwords:
            dict[author] = ngrams_author(n,author,compcorp,num,True)

        else:
            dict[author] = ngrams_author(n,author,compcorp,num,False)
    
    return dict
    
def remove_stopwords(list):
   """  filters english stopwords out of a list
        args: list
        returns: list not containing stopwords"""
   return([word for word in list if word not in stopwords.words('english')])
   
def lemmatizer(text):
    """lemmatizes all words.
    arg: text
    returns: lemmatized words where possible.
    """
    lmtzr = WordNetLemmatizer()
    for word in text:
        y = lmtzr.lemmatize(word,'v')
        return y
        
        
        
def zelda(): # sorry, dit moest even... :)
    winsound.Beep(210,200)
    winsound.Beep(225,200)
    winsound.Beep(238,200)
    winsound.Beep(250,200)

    winsound.Beep(210,200)
    winsound.Beep(225,200)
    winsound.Beep(238,200)
    winsound.Beep(250,200)

    winsound.Beep(225,180)
    winsound.Beep(238,180)
    winsound.Beep(250,180)
    winsound.Beep(262,180)

    winsound.Beep(225,180)
    winsound.Beep(238,180)
    winsound.Beep(250,180)
    winsound.Beep(262,180)

    winsound.Beep(238,150)
    winsound.Beep(250,150)
    winsound.Beep(262,150)
    winsound.Beep(275,150)

    winsound.Beep(238*2,150)
    winsound.Beep(250*2,150)
    winsound.Beep(262*2,150)
    winsound.Beep(275*2,160)
    time.sleep(1)
    winsound.Beep(210*4,150)
    winsound.Beep(225*4,150)
    winsound.Beep(238*4,150)
    winsound.Beep(250*4,1100)