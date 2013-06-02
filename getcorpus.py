import pickle

def corpus():
    corpusfile = open('corpus.pkl','r')
    c = pickle.load(corpusfile)
    corpusfile.close()
    return c

