from nltk import FreqDist
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize


def Generate_BoW(text):
    # generated bag of words of one text
    return FreqDist(word_tokenize(text))

    
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