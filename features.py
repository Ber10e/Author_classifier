from help_functions import *

def features(fs, textU):
    """ Calculates if a features is applicable to a text.
    Args:String (featurename), String (text)
    Returns: Boolean
    """
    text = textU.lower()
    if(fs=="f1"): # ----------------------first feature
        return (occurs_in_text("legal",text) >0 )
        
    elif(fs=="f2"):# ----------------------second feature
        return (occurs_in_text("safety",text) >0 )
        
    elif (fs=="f3"):# ----------------------third feature
        return (occurs_in_text("bank",text) >2 )
        
    elif(fs=="f4"):# ----------------------second feature
        return (occurs_in_text("internet",text) >0 )
        
    elif(fs=="f5"):# ----------------------second feature
        return (occurs_in_text("mail",text) >1 )
        
    elif(fs=="f6"):# ----------------------second feature
        return (occurs_in_text("to",text) >5 )
        
    elif(fs=="f7"):# ----------------------second feature
        return (occurs_in_text("china",text) >1 )
        
    elif(fs=="f8"):# ----------------------second feature
        return (occurs_in_text("prague",text) >0 )
        
    elif(fs=="f9"):# ----------------------second feature
        return (occurs_in_text("british",text) >0 )

    elif(fs=="f10"):# ----------------------second feature
        return (occurs_in_text("crowns",text) >0 )

    elif(fs=="f11"):# ----------------------second feature
        return (occurs_in_text("million",text) >0 )

    elif(fs=="f12"):# ----------------------second feature
        return (occurs_in_text("court",text) >0 )
        