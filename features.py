from help_functions import *

def features(fs, textU):
    """ Calculates if a features is applicable to a text.
    Args:String (featurename), String (text)
    Returns: Boolean
    """
    text = textU.lower()
    
    if(fs=="f1"): # ----------------------first feature
        return (occurs_in_text("market",text) >0 )
        
    elif(fs=="f2"):# ----------------------second feature
        return (occurs_in_text("internet",text) >0 )
        
    elif (fs=="f3"):# ----------------------third feature
        return (occurs_in_text("china",text) >0 )
        
    elif(fs=="f4"):# ----------------------second feature
        return (occurs_in_text("bank",text) >0 )
        
    elif(fs=="f5"):# ----------------------second feature
        return (occurs_in_text("british",text) >0 )
        
    elif(fs=="f6"):# ----------------------second feature
        return (occurs_in_text("prague",text) >0 )
        
    elif(fs=="f7"):# ----------------------second feature
        return (occurs_in_text("wang",text) >0 )
        
    elif(fs=="f8"):# ----------------------second feature
        return (occurs_in_text("beijing",text) >0 )
        
    elif(fs=="f9"):# ----------------------second feature
        return (occurs_in_text("million",text) >0 )

    elif(fs=="f10"):# ----------------------second feature
        return (occurs_in_text("australia",text) >0 )

    elif(fs=="f11"):# ----------------------second feature
        return (occurs_in_text("to",text) >13 )

    elif(fs=="f12"):# ----------------------second feature
        return (occurs_in_text("was",text) >3 )

    elif(fs=="f13"):# ----------------------second feature
        return (occurs_in_text("by",text) >3 )

    elif(fs=="f14"):# ----------------------second feature
        return (occurs_in_text("said",text) >4 )

    elif(fs=="f15"):# ----------------------second feature
        return (occurs_in_text("had",text) >3 )        
      

            
        
        