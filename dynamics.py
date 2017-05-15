from signaturefunctions import *


def Dynamics(lex):
    corpus = lex.Corpus
    Signatures = dict()
    StemToSig = dict()
 
    FormatString4 = "{0:15s} {1:15s} {2:6s} {3:20s}  "
    FormatString5 = "{0:15s} {1:15s} {2:6s} {3:10s}{4:10s}  "
    FormatString7 = "{0:15s} {1:15s} {2:6s} {3:10s}{4:10s} {5:10s} {6:10s}  "
    FormatString7a = "{0:15s} {1:15s} {2:6s} {3:10s}{4:10s}            {5:10s} {6:10s}  "
    page_1 = CPage()
    for word in corpus:

        if word not in lex.WordToSig:
            continue
        #print  "\n\n>> ", word,
        siglist_for_word = lex.WordToSig[word]

        for (stem, knownsig_str) in siglist_for_word:
            affixlength = len(word) - len(stem)
            if affixlength == 0:
                affix = "NULL"
            else:
                affix = word[-1 * affixlength:]

            #print FormatString1.format(word, stem, affix),
            if stem in StemToSig:                            
                sig_1 = StemToSig[stem]                
                sig1_str = sig_1.ReturnSignatureString()         
                if sig_1.ContainsAffix(affix):
                    print FormatString4.format(word, stem, affix, "Known word."  )
                    sig_1.IncrementObservedWord(stem, affix)
                    page_1.NewWord = word
                    page_1.GainingSignature = sig_1
                    page_1.LosingSignature = None

                else:
                    
                    newsig_str = AddAffixToSigString(affix, sig1_str)
                    if newsig_str not in Signatures:
                        NewSig_5 = CSignature(newsig_str)
                        StemToSig[stem] = NewSig_5
                        Signatures[newsig_str] = NewSig_5

                        # add stem to this sig
                        NewSig_5.AddStem(stem)
                        NewSig_5.AddWord(stem, affix)
                        page_1.NewWord = word
                        page_1.GainingSignature = NewSig_5
                        page_1.LosingSignature = sig_1
                        sig_1.RemoveStem(stem)
                        print FormatString7a.format(word, stem, affix, "old sig:", sig1_str, "new sig:", newsig_str)

                    # or if that  signature does currently exist
                    else:
                        print FormatString7.format(word, stem, affix, "old sig:", sig1_str, "known sig:", newsig_str)
                        sig_2 = Signatures[newsig_str]
                        MoveStem(stem, affix, sig_1, sig_2)
                        page_1.LosingSignature = None
                        page_1.GainingSignature = sig_2
                        StemToSig[stem] = sig_2
                        print FormatString7.format(word, stem, affix, "old sig:", sig1_str, "known sig:", newsig_str)



            # Or else the stem has not  been seen yet in this function:
            else:
                # we need a singleton siganature for this stem.   "affix" here *means* a singleton signature consisting of this affix.
                if affix in Signatures:
                    sig_3 = Signatures[affix]
                    sig_3.StemsToAffixToCorpusCount[stem] = dict()
                    sig_3.StemsToAffixToCorpusCount[stem][affix] = 1
                    sig_3.LifetimeCorpusCount += 1
                    page_1.LosingSignature = None
                    page_1.GainingSignature = sig_3
                    StemToSig[stem] = sig_3
                    print FormatString5.format(word, stem, affix, "New stem. Old mono-sig:", affix)
                else:
                    # the singleton signature did not yet exist:
                    sig_4 = CSignature(affix)
                    sig_4.AddStem(stem)
                    sig_4.AddWord(stem, affix)
                    print FormatString5.format(word, stem, affix, "New stem. New mono-sig:", affix)
                    Signatures[affix] = sig_4
                    StemToSig[stem] = sig_4
                    page_1.LosingSignature = None
                    page_1.GainingSignature = sig_4

    for sig in Signatures.keys():
        Signatures[sig].Display()


class CPage:
    def __init__(self):
        self.Rows = dict()  # key is an integer (the number of affixes in a signature); the value is a list of CSignatures
        self.NumberOfWords = 0  # number of word tokens processed so far

    def AddWord(self, new_word, gaining_signature, losing_siganture):
        self.GainingSignature = gaining_signature
        self.LosingSignature = losing_signature
        self.NewWord = new_word

    def CreateSVG(self):
        output_list = list()


class CSignature:
    def __init__(self, affix_string):
        self.Affixes_string = affix_string
        self.StemsToAffixToCorpusCount = dict()  # key is a stem-string, value is dict; and key of that dict is an affix, and its value is the corpus-count of that stem-affix combination.
        self.LifetimeCorpusCount = 0  # this keeps track of the number of corpus counts of words when they were in this signature;
        self.LifetimeWordCount = 0  # this keeps track of the number of distinct words that have ever been in this signature.

    def CurrentCorpusCount(self):
        total = 0
        for stem in self.StemsToAffixToCorpusCount:
            for affix in self.StemsToAffixToCorpusCount[stem]:
                total += self.StemsToAffixToCorpusCount[stem][affix]
        return total

    def ReturnStability(self):
        # print "\n    ----------------------------"
        # print "\n    Signature stability." ,
        # print  "    Number of stems",  len(self.StemsToAffixToCorpusCount)
        # for stem in self.StemsToAffixToCorpusCount:
        #    print "    Stem:", stem, self.StemsToAffixToCorpusCount[stem]
        #   # for affix in self.StemsToAffixToCorpusCount[stem]:
        #   #     print "affix:", affix, self.StemsToAffixToCorpusCount[stem][affix]
        # print "    --------------------------"
        num = float(self.CurrentCorpusCount())
        denom = float(self.LifetimeCorpusCount)
        stability = num / denom
        return stability

    def ReturnStems(self):
        return self.StemsToAffixToCorpusCount.keys()

    def ReturnSignatureString(self):
        return self.Affixes_string

    def ReturnAffixList(self):  # deprecatted ........
        return self.Affixes_string.split("=")

    #    def ReturnSignatureString(self):
    #        return self.Affixes_string

    def ContainsAffix(self, affix):
        if affix in self.Affixes_string.split("="):
            return True
        else:
            return False

    def AddStem(self, stem):
        # if stem_str not in self.StemsToAffixToCorpusCount:
        self.StemsToAffixToCorpusCount[stem] = dict()
        for affix in self.Affixes_string.split("="):
            self.StemsToAffixToCorpusCount[stem][affix] = 0

    def AddWord(self, stem, affix):
        self.StemsToAffixToCorpusCount[stem][affix] = 1
        self.LifetimeCorpusCount += 1
        self.LifetimeWordCount += 1

    def RemoveStem(self, stem_str):
        del self.StemsToAffixToCorpusCount[stem_str]

    def IncrementObservedWord(self, stem_str, affix_str):
        #print self.StemsToAffixToCorpusCount[stem_str]
        self.StemsToAffixToCorpusCount[stem_str][affix_str] += 1
        self.LifetimeCorpusCount += 1

    def Display(self):
        DisplaySignatureFlag = False
        if DisplaySignatureFlag == False:
            return
        tab = 4
        columnsize = 10
        print "\n    ---------------------------------------------------------------"
        print "    >>sig: ", self.Affixes_string, "Stability: ", self.ReturnStability(), "Current corpus count", self.CurrentCorpusCount(), "Lifetime corpus count", self.LifetimeCorpusCount
        print " " * (tab + columnsize),
        for affix in self.Affixes_string.split("="):
            print  "{:>10s}".format(affix),
        print
        for stem in self.StemsToAffixToCorpusCount.keys():
            print " " * tab + stem + " " * (columnsize - len(stem)),
            for affix in self.Affixes_string.split("="):
                print  "{:10d}".format(self.StemsToAffixToCorpusCount[stem][affix]),
            print
        print "    ---------------------------------------------------------------"


def MoveStem(stem, new_affix, from_sig, to_sig):
    # print "181", stem, new_affix
    to_sig.AddStem(stem)
    from_sig.RemoveStem(stem)
