from nltk import FreqDist
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize


def Generate_BoW(text):
    # generated bag of words of one text
    return FreqDist(word_tokenize(text.lower()))

    
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
    
def numberoftexts_cat(author,texts):
    """counts the number of texts of a given author"""
    count = 0
    for (text,cat) in texts:
        if(cat == author):
            count +=1
    return count 

def author_bow(author,corpus):
    """for given author, builds a dictionary:
    keys: used words
    values: list of occurences in texts
    then calculates the weighed occurence of all words (number of times that word is used in one text)
    """

    author_freqd={}
    numb_texts=numberoftexts_cat(author,corpus)
    
    for (text,cat) in corpus:
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
