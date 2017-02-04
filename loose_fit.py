from signaturefunctions import *

#----------------------------------------------------------------------------------------------------------------------------#
def loose_fit(Lexicon ,type = "suffix"):
#----------------------------------------------------------------------------------------------------------------------------#
        for sig in Lexicon.SignatureToStems:
                print  "\n\n", sig
                loose_fit_on_signature(sig, Lexicon)


#----------------------------------------------------------------------------------------------------------------------------#
def loose_fit_on_signature(Sig, Lexicon ,type = "suffix"):
#----------------------------------------------------------------------------------------------------------------------------#
    """
        This function takes a signature, and finds all tuples of words that *almost* satisfy the signature, where we say
        that a set of words W almost satisfies a signature if we can find a set of K stem strings such that one of those
        stems can be associated with one of the affixes in order to generate existing words, and where the stems agree with
        each other except for a final margin of 2 or 3 letters. 
    """
    Margin = 2  # The maximum difference permitted between stems for the same signature.


    #       Order the affixes of Sig by descending length
    if type != "suffix":
        print "Only suffixes for now. Exiting."
        return
    # Stems is a dict whose key is an affix and whose value is a pair: (stem, whole word including stem and affix)
    Stems = {}
    affixes = SortSignatureStringByLength(Sig)
    #print affixes
    affix = affixes.pop(0)
    print affix
    Stems[affix] = dict()
    for i in range(len(Lexicon.ReverseWordList)):
        word = Lexicon.ReverseWordList[i]
        if len(word) < len(affix):
            continue
        if word[-1*len(affix)] != affix:
            continue
        for j in range(i,len(Lexicon.ReverseWordList)):
            affixlen = len(affix)
            if word[-1*affixlen] == affix:
                wordlen= len(word)
                stem = word[:(wordlen-affixlen)]    
                Stems[affix][(stem,word)] = 1 
                print "\n", affix, Stems[affix]
        
    while (len(affixes)):
        affix = affixes.pop(0)





   	
