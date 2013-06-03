import pickle

def corpus(num):
    corpusfile = open('corpus.pkl','r')
    c = pickle.load(corpusfile)
    corpusfile.close()
    return c[0:(num*50)]

