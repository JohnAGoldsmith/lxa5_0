from signaturefunctions import *


def Dynamics( lex):
    corpus = lex.Corpus
    Signatures = dict()
    StemToSig = dict()

    page_1 = CPage()
    for word in corpus:

        if word not in lex.WordToSig:
            continue
        print "\n>> ", word,
        siglist_for_word = lex.WordToSig[word]

        for (stem, knownsig_str) in siglist_for_word:
            #print "20", stem, knownsig_str
            affixlength = len(word) - len(stem)
            if affixlength == 0:
                affix = "NULL"
            else:
                affix = word[-1 * affixlength:]

            print "\n    stem", stem, "; affix: ", affix, "; prior knowledge: ",  knownsig_str,
            #print "  Current knowledge: Known stems: ", StemToSig.keys()
            #print "  Known signatures: ", Signatures.keys()
            #signo= 1
            #for sig in Signatures.keys():
            #    print "  ",  signo,
            #    signo += 1
            #    Signatures[sig].Display()
            #print stem, affix, knownsig_str
            # Consider each analysis of the current word (analysis = stem plus signature).
            # First, if the stem has already appeared during this function:
            if stem in StemToSig:
                print "This is a known stem.",
                # this notation sig_1 means that it is a reference to a CSignature object
                sig_1 = StemToSig[stem]
                sig1_str = sig_1.ReturnSignatureString()
                #print "33", sig1_str
                #print "affix: ", affix, "sig_1 suffixes", sig_1.Affixes_string
                if sig_1.ContainsAffix(affix):
                    #print "    28 So the seen affix is in the known signature."
                    print "Word repetition."
                    sig_1.IncrementObservedWord( stem, affix)

                    # if we have already seen this stem and this affix together:
                    #sig_1.Affixes[affix] += 1
                    #sig_1.Stems[stem] += 1
                    #sig_1.StemToWordCount[stem][affix] += 1
                    page_1.NewWord = word
                    page_1.GainingSignature = sig_1
                    page_1.LosingSignature = None
                else:
                    # or else the stem has NOT been seen yet in this analysis (i.e., with this suffix)
                    print " But new affix; currently sig is ", sig1_str, ".",
                    newsig_str = AddAffixToSigString(affix, sig1_str)
                    #print "58 is this an affix?" , affix
                    print "    New sig is", newsig_str, ".",
                    if newsig_str not in Signatures:
                        # if that signature does not currently exist:
                        print "    This is a new signature."
                        NewSig_5 = CSignature(newsig_str)
                        Signatures[newsig_str] = NewSig_5
                        page_1.NewWord = word
                        page_1.GainingSignature = NewSig_5
                        page_1.LosingSignature = sig_1
                        NewSig_5.StemsToAffixToCorpusCount[stem]= sig_1.StemsToAffixToCorpusCount[stem]
                        NewSig_5.StemsToAffixToCorpusCount[stem][affix] = 1
                        del  sig_1.StemsToAffixToCorpusCount[stem]
                        #print "  We delete ", stem, "from its old sig", sig_1.Affixes_string, "and add it to ", newsig_str

                        #check is this right?
                        StemToSig[stem] = NewSig_5
                    # or if that  signature does currently exist
                    else:
                        print "    This is a known signature."
                        sig_2 = Signatures[newsig_str]
                        MoveStem(stem, affix, sig_1, sig_2)
                        page_1.LosingSignature = None
                        page_1.GainingSignature = sig_2
                        StemToSig[stem] = sig_2

            # Or else the stem has not  been seen yet in this function:
            else:
                print "New stem.",
                # we need a singleton siganature for this stem.   "affix" here *means* a singleton signature consisting of this affix.
                if affix in Signatures:
                    print "This is a known singleton signature, though: ", affix
                    # if the singleton signature of this affix exists:
                    sig_3 = Signatures[affix]
                    #print "    63 affix string in sig:", affix,  sig_3.Affixes_string
                    sig_3.StemsToAffixToCorpusCount[stem] = dict()
                    sig_3.StemsToAffixToCorpusCount[stem][affix] = 1
                    page_1.LosingSignature = None
                    page_1.GainingSignature = sig_3
                    StemToSig[stem]= sig_3
                else:
                    # the singleton signature did not yet exist:
                    sig_4 = CSignature(affix)
                    print "Creating new singleton signature: (", sig_4.Affixes_string, ")."
                    Signatures[affix] = sig_4
                    StemToSig[stem] = sig_4
                    sig_4.StemsToAffixToCorpusCount[stem]=dict()
                    sig_4.StemsToAffixToCorpusCount[stem][affix] = 1
                    # print "    70 Now we have sig-affixes: (", StemToSig[stem].Affixes_string, ") and stems", sig_4.ReturnStems()
                    page_1.LosingSignature = None
                    page_1.GainingSignature = sig_4
        #page_1.UpdatePage(wordno)
        #output_list = page_1.CreateSVG()

    for sig in Signatures.keys():
        Signatures[sig].Display()


class CPage:
    def __init__(self):
        self.Rows= dict()  # key is an integer (the number of affixes in a signature); the value is a list of CSignatures
        self.NumberOfWords = 0 #number of word tokens processed so far

    def AddWord(self, new_word, gaining_signature, losing_siganture):
        self.GainingSignature = gaining_signature
        self.LosingSignature = losing_signature
        self.NewWord = new_word


    def CreateSVG(self):
        output_list = list()




class CSignature:

    def __init__(self, affix_string):
        self.Affixes_string = affix_string
        self.StemsToAffixToCorpusCount = dict() # key is a stem-string, value is dict; and key of that dict is an affix, and its value is the corpus-count of that stem-affix combination.
        self.LifetimeCorpusCount = 0 #this keeps track of the number of corpus counts of words that have been in this signature;
        self.LifetimeWordCount = 0 # this keeps track of the number of distinct words that have ever been in this signature.

    def ReturnStems(self):
        return self.StemsToAffixToCorpusCount.keys()

    def ReturnSignatureString(self):
        return self.Affixes_string

    def ReturnAffixList(self): # deprecatted ........
        return  MakeSignatureListFromSignatureString(self.Affixes_string)

    def ReturnSignatureString(self):
        return self.Affixes_string

    def ContainsAffix(self, affix):
        if affix in self.Affixes_string.split("="):
            return True
        else:
            return False


    def AddStem(self, stem_str, new_affix_str,  losing_signature):
        self.StemsToAffixToCorpusCount[stem_str] = dict()
        LosingSignatureAffixes = losing_signature.ReturnSignatureString().split("=")
        for affix in LosingSignatureAffixes:
            #print "162 affix is ", affix, "in losing sig:" ,losing_signature.ReturnSignatureString()
            self.StemsToAffixToCorpusCount[stem_str][affix]  =losing_signature.StemsToAffixToCorpusCount[stem_str][affix]
        self.StemsToAffixToCorpusCount[stem_str][new_affix_str] = 1
        self.LifetimeCorpusCount += 1
        self.LifetimeWordCount += 1


    def RemoveStem(self, stem_str):
        del self.StemsToAffixToCorpusCount[stem_str]
        #print "  Removing stem from losing signature. (", stem_str, ")"



    def IncrementObservedWord(self, stem_str, affix_str):
        #print "    Word repetition. Stem:", stem_str, "affix:", affix_str, "in sig: ",self.ReturnSignatureString()
        self.StemsToAffixToCorpusCount[stem_str][affix_str] += 1
        self.LifetimeCorpusCount += 1

    def Display(self):
        print "sig: ", self.Affixes_string
        for stem in self.StemsToAffixToCorpusCount.keys():
            print "   ", stem, ":", self.StemsToAffixToCorpusCount[stem].keys()


def MoveStem(stem, new_affix, from_sig, to_sig):
    #print "181", stem, new_affix
    to_sig.AddStem(stem, new_affix, from_sig)
    from_sig.RemoveStem(stem)
