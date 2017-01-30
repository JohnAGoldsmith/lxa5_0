from signaturefunctions import *
from stringfunctions import *
#----------------------------------------------------------------------------------------------------------------------------#
def loose_fit(Lexicon ,type = "suffix"):
#----------------------------------------------------------------------------------------------------------------------------#
        for sig in Lexicon.SignatureToStems:
                #print  "\n\n7", sig
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
    affixlen = len(affix)
    #print "32", affix
    #Stems[affix] = list ()
    Stems[affix] =filter_by_suffix(affix, Lexicon.Words)
    #print "\n46", affix, Stems[affix]
    while (len(affixes)):
        affix = affixes.pop(0)
        #print "39", affix
        list2 = filter_by_suffix(affix, Lexicon.Words)
        #print "41", list2
        print "42", find_first_and_last_string_in_list(affix, list2)
