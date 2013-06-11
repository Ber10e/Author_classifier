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

def bigrams_author(author,compcorp,num):
    """
    berekent gegeven een auteur en een compactcorpus (andere functie) een geordende lijst van tuples (bigram,aantal voorkomens) 
    """
    bigrams0 = []
    for (text,cat) in compcorp[author]:
        bigrams0 += bigrams(word_tokenize(text.lower()))

    return sorted(FreqDist(bigrams0).iteritems(), key=itemgetter(1), reverse=True) [:num]

def trigrams_author(author,compcorp,num):
    """
    """
    trigrams0 = []
    for (text,cat) in compcorp[author]:
        trigrams0 += trigrams(word_tokenize(text.lower()))

    return sorted(FreqDist(trigrams0).iteritems(), key=itemgetter(1), reverse=True) [:num]

def bigrams_dict(authors,corp,num):
    """builds a dictionary of num most frequent bigrams in the corpus per author
    args: list of strings, list of tuples (string,string), int
    returns dictionary{string:[(bigram,string)]}
    """
    compcorp = compactcorpus(corp)
    dict={}
    for author in authors:
        dict[author] = bigrams_author(author,compcorp,num)
    return dict 

def trigrams_dict(authors,corp,num):
    """builds a dictionary of num most frequent trigrams in the corpus per author
    args: list of strings, list of tuples (string,string), int
    returns dictionary{string:[(trigram,string)]}
    """
    compcorp = compactcorpus(corp)
    dict={}
    for author in authors:
        dict[author] = trigrams_author(author,compcorp,num)
    return dict

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