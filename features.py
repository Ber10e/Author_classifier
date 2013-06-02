from help_functions import *

def features(fs, text):
    """ Calculates if a features is applicable to a text.
    Args:String (featurename), String (text)
    Returns: Boolean
    """
    if(fs=="f1"): # ----------------------first feature
        return (len(text) > 100)
    elif(fs=="f2"):# ----------------------second feature
        return ("chapter" in text)
    elif (fs=="f3"):# ----------------------third feature
        return (len(text) < 80)