from signaturefunctions import *


def Dynamics(lex):
    corpus = lex.Corpus
    Signatures = dict()
    StemToSig = dict()
    FormatString1 = "{0:15s} {1:12s} {2:6s} "
    FormatString2 = "{0:10s}  {1:15s} "
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

            #print "(", stem, affix, ") [", knownsig_str, "]",
            print FormatString1.format(word, stem, affix),
            # Consider each analysis of the current word (analysis = stem plus signature).
            # First, if the stem has already appeared during this function:
            if stem in StemToSig:
                #print "Known stem.",
                # this notation sig_1 means that it is a reference to a CSignature object
                sig_1 = StemToSig[stem]
                #print "from (", sig_1.ReturnSignatureString(), ")",
                sig1_str = sig_1.ReturnSignatureString()
                #print FormatString2.format("Known stem", sig1_str),
                if sig_1.ContainsAffix(affix):
                    #print "Old word.",
                    print FormatString2.format("Known word", " "),
                    sig_1.IncrementObservedWord(stem, affix)
                    #sig_1.Display()
                    page_1.NewWord = word
                    page_1.GainingSignature = sig_1
                    page_1.LosingSignature = None

                else:
                    # or else the stem has NOT been seen yet in this analysis (i.e., with this suffix)
                    print FormatString2.format("Known stem", sig1_str),
                    print " Current sig:", sig1_str, ".",
                    newsig_str = AddAffixToSigString(affix, sig1_str)
                    print "New sig: (", newsig_str, ").",
                    print
                    if newsig_str not in Signatures:
                        # if that signature does not currently exist:
                        # print "New signature.",
                        NewSig_5 = CSignature(newsig_str)
                        StemToSig[stem] = NewSig_5
                        Signatures[newsig_str] = NewSig_5

                        # add stem to this sig
                        # make sure this sig has all the right affixes for this stem
                        NewSig_5.AddStem(stem)
                        NewSig_5.AddWord(stem, affix)
                        print StemToSig[stem].StemsToAffixToCorpusCount[stem]
                        page_1.NewWord = word
                        page_1.GainingSignature = NewSig_5
                        page_1.LosingSignature = sig_1
                        sig_1.RemoveStem(stem)
                        #                        del  sig_1.StemsToAffixToCorpusCount[stem]
                        FormatString3 = "new sig ({0:15})"
                        print FormatString3.format(NewSig_5)
                        #print "    new sig: ", NewSig_5.Display()
                        print "    old sig: ", sig_1.Display()

                    # or if that  signature does currently exist
                    else:
                        print "    This is a known signature.",
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
                    #print "Old sig: {", affix, ")"
                    print FormatString2.format("New sig", sig_4.Affixes_string)
                    # if the singleton signature of this affix exists:
                    sig_3 = Signatures[affix]
                    # print "    63 affix string in sig:", affix,  sig_3.Affixes_string
                    sig_3.StemsToAffixToCorpusCount[stem] = dict()
                    sig_3.StemsToAffixToCorpusCount[stem][affix] = 1
                    sig_3.LifetimeCorpusCount += 1
                    page_1.LosingSignature = None
                    page_1.GainingSignature = sig_3
                    StemToSig[stem] = sig_3
                    sig_3.Display()
                else:
                    # the singleton signature did not yet exist:
                    sig_4 = CSignature(affix)
                    sig_4.AddStem(stem)
                    sig_4.AddWord(stem, affix)
                    #print "New sig:: (", sig_4.Affixes_string, ")"
                    print FormatString2.format("New sig:", sig_4.Affixes_string)
                    Signatures[affix] = sig_4
                    StemToSig[stem] = sig_4
                    sig_4.Display()
                    # print "    70 Now we have sig-affixes: (", StemToSig[stem].Affixes_string, ") and stems", sig_4.ReturnStems()
                    page_1.LosingSignature = None
                    page_1.GainingSignature = sig_4

                    # page_1.UpdatePage(wordno)
                    # output_list = page_1.CreateSVG()

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
