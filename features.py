from help_functions import *
import re
print "features imported"

wordoccur = re.compile(r"^wrd:(.+)>(.+)$")
bioccur = re.compile(r"^bi:\((.+),(.+)\)>(.+)$")
trioccur = re.compile(r"^tri:\((.+),(.+),(.+)\)>(.+)$")
skipoccur = re.compile(r"^skip:\((.+),(.+),(.+)\)>(.+)$")


"""
features zijn strings van de vormen:
wrd:hallo>1
of
bi:(the,man)>2
of
tri:(the,man,said)>2
"""



def features(fs, text,bigrams,trigrams,skipgrams):
    """ Calculates if a features is applicable to a text.
    Args:String (featurename), String (text)
    Returns: Boolean
    """
    unigrams = text

    if(not(re.search(wordoccur,fs)==None)): # ----------------------word occurence features
        m = re.search(wordoccur,fs)
        return (m.groups()[0] in unigrams)
        #return (wrd_occurs_in_text(m.groups()[0],text) >int(m.groups()[1]) )
    elif(not(re.search(trioccur,fs)==None)):
        m = m = re.search(trioccur,fs)
        tuple =(m.groups()[0],m.groups()[1],m.groups()[2])
        return (tuple in trigrams)
        #return (trigram_occurs_in_text(tuple,text) >int(m.groups()[3]) )
    elif(not(re.search(bioccur,fs)==None)):
        m = re.search(bioccur,fs)
        tuple = (m.groups()[0],m.groups()[1])
        return (tuple in bigrams)
        #return (bigram_occurs_in_text(tuple,text) >int(m.groups()[2]) )
    elif(not(re.search(skipoccur,fs)==None)):
        m = m = re.search(skipoccur,fs)
        tuple =(m.groups()[0],m.groups()[1],m.groups()[2])
        return (tuple in skipgrams)
        #return (skipgram_occurs_in_text(tuple,text) >int(m.groups()[3]) )
    else:
        return (fs(text))
      

            
        
        