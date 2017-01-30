import sys
import math
from signaturefunctions import *
from printing_to_files import *
 
# This is just part of documentation:
# A signature is a tuple of strings (each an affix).
# Signatures is a map: its keys are signatures.  Its values are *sets* of stems.
# StemToWord is a map; its keys are stems.       Its values are *sets* of words.
# StemToSig  is a map; its keys are stems.       Its values are individual signatures.
# WordToSig  is a Map. its keys are words.       Its values are *lists* of signatures.
# StemCounts is a map. Its keys are words.   Its values are corpus counts of stems.
# SignatureToStems is a dict: its keys are tuples of strings, and its values are dicts of stems.

class CWordList:
    def __init__(self):
        self.mylist = list()
       
    def GetCount(self):
        return len(self.mylist)
    def AddWord(self, word):
        self.mylist.append(Word(word))

    def at(self, n):
        return self.mylist[n]

    def sort(self):
        self.mylist.sort(key=lambda item: item.Key)
        # for item in self.mylist:
        #   print item.Key
        for i in range(len(self.mylist)):
            word = self.mylist[i]
            word.leftindex = i
        templist = list()
        for word in self.mylist:
            thispair = (word.Key[::-1], word.leftindex)
            templist.append(thispair)
        templist.sort(key=lambda item: item[0])
        for i in range(len(self.mylist)):
            (drow, leftindex) = templist[i]
            self.mylist[leftindex].rightindex = i
            
        #not currently used
    def PrintXY(self, outfile):
        Size = float(len(self.mylist))
        for word in self.mylist:
            x = word.leftindex / Size
            y = word.rightindex / Size
            print >> outfile, "{:20s}{8i} {:9.5} {:9.5}".format(word.Key, x, y)


## -------                                                      ------- #
##              Class Lexicon                                   ------- #
## -------                                                      ------- #
class CLexicon:
    def __init__(self):
        self.WordList = CWordList()
        self.Words = list()
        self.WordCounts = dict()
        self.ReverseWordList = list()
        #self.Signatures = {}        #not currently used...
        self.SignatureToStems = {}
        self.WordToSig = {}
        self.StemToWord = {}
        self.StemToAffix = {}
        self.StemCounts = {}
        self.StemToSignature = {}
        self.Suffixes={}
        self.Prefixes = {}
        self.MinimumStemsInaSignature =2
        self.MinimumStemLength = 3
        self.MaximumAffixLength =4
        self.MaximumNumberOfAffixesInASignature = 10
        self.NumberOfAnalyzedWords = 0
        self.LettersInAnalyzedWords = 0
        self.NumberOfUnanalyzedWords = 0
        self.LettersInUnanalyzedWords = 0
        self.TotalLetterCountInWords = 0
        self.LettersInStems = 0
        self.AffixLettersInSignatures = 0
        self.TotalRobustInSignatures = 0


## -------                                                      ------- #
##              Central signature computation                   ------- #
## -------                                                      ------- #

# ----------------------------------------------------------------------------------------------------------------------------#
    def MakeSignatures(self, lxalogfile,outfile_Rebalancing_Signatures, FindSuffixesFlag, MinimumStemLength):
# ----------------------------------------------------------------------------------------------------------------------------#
        formatstring1 =  "  {:50s}{:>10,}"
        formatstring2 =  "  {:50s}"
        formatstring3 =  "{:40s}{:10,d}"
        print formatstring2.format("The MakeSignatures function")

        # Protostems are candidate stems made during the algorithm, but not kept afterwards.
        Protostems = dict()
        self.NumberOfAnalyzedWords      = 0
        self.LettersInAnalyzedWords     = 0
        self.NumberOfUnanalyzedWords    = 0
        self.LettersInUnanalyzedWords   = 0
    
        AnalyzedWords = dict()
        #Lexicon.TotalLetterCountInWords = 0

        self.TotalRobustnessInSignatures            = 0
        self.LettersInStems                         = 0
        self.TotalLetterCostOfAffixesInSignatures   = 0
    
        # 1 -------
        self.FindProtostems(self.WordList.mylist, Protostems, self.MinimumStemLength, FindSuffixesFlag)
        print formatstring1.format("1a. Finished finding proto-stems.", len(Protostems)) 

        self.FindAffixes( Protostems,  FindSuffixesFlag)
        print formatstring1.format("1b. Finished finding affixes for protostems.", len(self.Suffixes)+ len(self.Prefixes))  

        # 2 It is possible for a stem to have only one affix at this point. We must eliminate those analyses.  -------
        ListOfStemsToRemove = list()
        for stem in self.StemToAffix:
            if len(self.StemToAffix[stem]) < 2:
                ListOfStemsToRemove.append(stem)
        print formatstring1.format("2. Number of stems to remove due to mono-fixivity:", len(ListOfStemsToRemove))     

        for stem in ListOfStemsToRemove:
            del self.StemToWord[stem]
            del self.StemToAffix[stem]


        # 3  Execute Stems-to-signatures. This is in a sense the most important step.        -------
        
        self.LettersInStems                         =0
        self.TotalLetterCostOfAffixesInSignatures   =0
        self.StemsToSignatures(FindSuffixesFlag)

        print  formatstring1.format("3. Finished first pass of finding stems, affixes, and signatures.", len(self.SignatureToStems))  
              
        # 4 Rebalancing now, which means:                  -------
        # We look for a stem-final sequence that appears on all or almost all the stems, and shift it to affixes.
        # Make changes in Lexicon.SignatureToStems, and .StemToSig, and .WordToSig, and .StemToWord, and .StemToAffix  and signature_tuples....

        threshold = 0.80
        count = self.RebalanceSignatureBreaks2 (threshold, outfile_Rebalancing_Signatures, FindSuffixesFlag) 
        print formatstring1.format("4. Find signature structure function.",count) 

        if FindSuffixesFlag:
            Affixes = self.Suffixes
        else:
            Affixes = self.Prefixes
        self.FindSignatureStructure (FindSuffixesFlag, lxalogfile, Affixes, affix_threshold=3)
         

        # 5  ------- compute robustness
        self.ComputeRobustness()
        print  formatstring2.format("5. Computed robustness")  

        #8  ------- Print
        print >> lxalogfile, formatstring3.format("Number of analyzed words", self.NumberOfAnalyzedWords)
        print >> lxalogfile, formatstring3.format("Number of unanalyzed words", self.NumberOfUnanalyzedWords)
        print >> lxalogfile, formatstring3.format("Letters in stems", self.LettersInStems)
        print >> lxalogfile, formatstring3.format("Letters in affixes", self.AffixLettersInSignatures)
        print >> lxalogfile, formatstring3.format("Total robustness in signatures", self.TotalRobustnessInSignatures)
    
        return
# ----------------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------------#
    def StemsToSignatures(self,FindSuffixesFlag):
        if FindSuffixesFlag:
            Affixes = self.Suffixes
        else:
            Affixes = self.Prefixes

        #  Iterate through each stem, get its affixes and count them, and create signatures. 
        for stem in self.StemToWord:
            self.LettersInStems += len(stem)
            signature = list(self.StemToAffix[stem])
            signature.sort()
            signature_string = "-".join(signature)
            for affix in signature:
                if affix not in Affixes:
                    Affixes[affix] = 0
                Affixes[affix] += 1
            if signature_string not in self.SignatureToStems:
                self.SignatureToStems[signature_string] = dict()
                for affix in signature:
                    self.TotalLetterCostOfAffixesInSignatures += len(affix)
            self.SignatureToStems[signature_string][stem] = 1
            self.StemToSignature[stem] = signature_string
            for word in self.StemToWord[stem]:
                if word not in self.WordToSig:
                    self.WordToSig[word] = list()
                self.WordToSig[word].append(signature_string)
        for sig in self.SignatureToStems: 
            if len(self.SignatureToStems[sig]) < self.MinimumStemsInaSignature:
                for stem in self.SignatureToStems[sig]:
                    del self.StemToSignature[stem]
                    for word in self.StemToWord[stem]:
                        if len( self.WordToSig[word] ) == 1:                     
                            del self.WordToSig[word]
                        else:
                            self.WordToSig[word].remove(sig)
                    del self.StemToWord[stem]

# ----------------------------------------------------------------------------------------------------------------------------#
    def FindSignatureStructure (self, FindSuffixesFlag, outfile, Affixes = None, affix_threshold = 1):

    # This function assumes that we have the set of stems already in Lexicon.SignatureToStems. It does the rest.

            StemList = self.StemToWord.keys()
            self.StemToSig = {}
            self.StemToAffix = {}# ok
            self.StemToWord = dict()# ok
            self.Signatures = {}
            self.SignatureToStems = {}
            self.WordToSig = {}
            self.StemCounts = {}

            NumberOfColumns = 8
            number_of_affixes_per_line = 10
            #  Signatures with way too many affixes are spurious.
            # If we have already run this function before, we have a set of affixes ranked by frequency,
            # and we can use these now to eliminate low frequency suffixes from signatures with
            # just one affix. 
            # Lexicon.MaximumNumberOfAffixesInASignature
            # Number of affixes we are confident in:
            formatstring1 =  "       {:50s}{:>10,}"
            formatstring2 =  "       {:50s}"
            formatstring3 =  "\n       Top {:>10,}  affixes retained for use now (out of {:>5} )"


            print formatstring2.format("Inside Find_Signature_Structure.")
            print formatstring2.format("i. Finding affixes we are confident about.")


            # -----------------------------------------------------------------#
            # Block 1. This block defines affixes, confident affixes, and signatures.
            # -----------------------------------------------------------------#            
            if len (Affixes ) ==0:
                if FindSuffixesFlag:
                    print "No suffixes found yet."
                else:
                    print "No prefixes found yet." 
            else:
                ConfidentAffixes = dict()
                NumberOfConfidentAffixes = 50
                NumberOfAffixes = len(Affixes.keys())
                if NumberOfConfidentAffixes > NumberOfAffixes:
                    NumberOfConfidentAffixes = NumberOfAffixes          
                SortedAffixes = list(Affixes.keys())
                SortedAffixes.sort(key=lambda affix:Affixes[affix], reverse=True)
                
                print formatstring3.format(NumberOfConfidentAffixes, len(SortedAffixes))   
                count = 0
                print " "*6,
                for affixno in range(NumberOfConfidentAffixes):
                    ConfidentAffixes[SortedAffixes[affixno]]=1
                    print  "{:6s} ".format(SortedAffixes[affixno]),
                    count += 1
                    if count % number_of_affixes_per_line == 0:
                        print 
                        print "      ",
                if (False): # not used currently
                        for sig in self.SignatureToStems:
                            stems = self.SignatureToStems[sig]
                            newsig = list()
                            if len(stems) == 1:         
                                for affix in sig:
                                    if affix in ConfidentAffixes:
                                        newsig.append(affix)
                print 

            #-----------------------------------------------------------------#
            # Block 2: This block loops through all words
            # -----------------------------------------------------------------#              
             
            # Creates Lexicon.StemToWord, Lexicon.StemToAffix. 
            column_no = 0
            print 
            print formatstring2.format("ii.  Reanalyzing words, finding both stems and affixes.")
            if True:
                print " "*12 + "Word number:",
                for i in range(len(self.WordList.mylist)): 
                    if i % 2500 == 0:
                        print "{:7,d}".format(i),           
                        sys.stdout.flush()
                        column_no += 1
                        if column_no % NumberOfColumns == 0:
                            column_no = 0
                            print "\n" + " "*11,               
                    word = self.WordList.mylist[i].Key
                    WordAnalyzedFlag = False
                    for i in range(len(word)-1 , self.MinimumStemLength-1, -1):   # loop on positions in the word, left to right
                        if FindSuffixesFlag:
                            stem = word[:i]
                        else:
                            stem = word[-1*i:]  
                        if stem in StemList:  
                            affixlength = len(word)-i
                            if FindSuffixesFlag:
                                affix = word[i:]
                            else:
                                affix = word[:affixlength]  
                            if len(affix) > self.MaximumAffixLength:
                                continue
                            # the next line involves putting a threshold on frequencies of affixes.
                            if Affixes and affix in Affixes and Affixes[affix] < affix_threshold:
                                continue                        
                            #print stem, suffix          
                            if stem not in self.StemToWord:
                                self.StemToWord[stem] = dict()
                            self.StemToWord[stem][word]=1
                            if stem not in self.StemToAffix:
                                self.StemToAffix[stem] = dict()
                            self.StemToAffix[stem][affix] = 1 
                            if stem in self.WordCounts: # this is for the case where the stem is a free-standing word also 
                                self.StemToWord[stem][stem] = 1
                                self.StemToAffix[stem]["NULL"] = 1
                            if stem not in self.StemCounts:
                                self.StemCounts[stem] = 0
                            self.StemCounts[stem]+= self.WordCounts[word]
                     
            print 
            self.LettersInStems =0
            self.TotalLetterCostOfAffixesInSignatures =0         


            # --------------------------------------------------------------------
            if (False):
                for stem in self.StemToAffix:
                    if len(self.StemToAffix[stem]) > self.MaximumNumberOfAffixesInASignature: 
                        for sig in self.SignatureToStems:
                            stems = self.SignatureToStems[sig]
                            newsig = list()
                            if len(stems) == 1:         
                                for affix in sig:
                                    if affix in ConfidentAffixes:
                                        newsig.append(affix)
                     

            # --------------------------------------------------------------------
            print "       iii. Finding a set of signatures."
            self.StemsToSignatures(FindSuffixesFlag)

            # Print output --------------------------------------------------------
            print  " "* 6, "iv.  Signatures (count): ", len(self.SignatureToStems) 
            print formatstring2.format("v.  Finished redoing structure")
            print >>outfile, formatstring2.format("iv.  Finished redoing structure\n")
            print >>outfile, "Number of sigs: ", len(self.SignatureToStems)
                     
             




#-----------------------------------------------------------------------------------------------------------------------------#
    def FindProtostems(self, wordlist, Protostems,minimum_stem_length, FindSuffixesFlag ,maximum_stem_length = -1):
            # A "maximum_stem_length" is included here so that we can use this function to explore
            # for stems shorter than the minimum that was assumed on an earlier iteration.
            previousword = ""
            if FindSuffixesFlag:
                for i in range(len(wordlist)):
                    word = wordlist[i].Key
                    differencefoundflag = False
                    if previousword == "":  # only on first iteration
                        previousword = word
                        continue
                    if maximum_stem_length > 0:
                        span = min(len(word), len(previousword), maximum_stem_length)
                    else:
                        span = min(len(word), len(previousword))
                    for i in range(span):
                        if word[i] != previousword[i]: #will a stem be found in the very first word?
                            differencefoundflag = True
                            stem = word[:i]
                            if len(stem) >= minimum_stem_length :
                                if stem not in Protostems:
                                    Protostems[stem] = 1
                                else:
                                    Protostems[stem] += 1
                            previousword = word
                            break
                    if differencefoundflag:
                        continue
                    if len(previousword) > i + 1:
                        previousword = word
                        continue
                    if (len(word)) >= i:
                        if len(previousword) >= minimum_stem_length:
                            if (previousword not in Protostems):
                                Protostems[previousword] = 1
                            else:
                                Protostems[previousword] += 1
                    previousword = word

            else:
                #print "prefixes"
                ReversedList = list()
                TempList = list()
                for word in wordlist:
                    key = word.Key
                    key = key[::-1]
                    TempList.append(key)
                TempList.sort()
                for word in TempList:
                    ReversedList.append(word[::-1])
                for i in range(len(ReversedList)):
                    word = ReversedList[i]
                    differencefoundflag = False
                    if previousword == "":  # only on first iteration
                        previousword = word
                        continue
                    span = min(len(word), len(previousword))
                    for i in range(1,span,):
                        if word[-1*i] != previousword[-1*i]:
                            differencefoundflag = True
                            stem = word[-1*i+1:]                        
                            if len(stem) >= minimum_stem_length:
                                if stem not in Protostems:
                                    Protostems[stem] = 1
                                else:
                                    Protostems[stem] += 1
                                #print previousword, word, stem
                            previousword = word
                            break
                    if differencefoundflag:
                        continue
                    if len(previousword) > i + 1:
                        previousword = word
                        continue
                    if (len(word)) >= i:
                        if len(previousword) >= minimum_stem_length:
                            if (previousword not in Protostems):
                                Protostems[previousword] = 1
                            else:
                                Protostems[previousword] += 1
                    previousword = word

#----------------------------------------------------------------------------------------------------------------------------#
    def FindAffixes(self, Protostems,  FindSuffixesFlag):

        wordlist=self.WordList.mylist
        MinimumStemLength = self.MinimumStemLength
        MaximumAffixLength = self.MaximumAffixLength
        if FindSuffixesFlag:  
            for i in range(len(wordlist)):
                word = wordlist[i].Key
                WordAnalyzedFlag = False
                #print (word)
                for i in range(len(word)-1 , MinimumStemLength-1, -1):
                    stem = word[:i]
                    if stem in Protostems:
                        suffix = word[i:]
                        if len(suffix) > MaximumAffixLength:
                            continue
                        if stem not in self.StemToWord:
                                self.StemToWord[stem] = dict()
                        self.StemToWord[stem][word]=1
                        if stem not in self.StemToAffix:
                            self.StemToAffix[stem] = dict()
                        self.StemToAffix[stem][suffix] = 1 
                        if stem in self.WordCounts:
                            self.StemToWord[stem][stem] = 1
                            self.StemToAffix[stem]["NULL"] = 1
                            self.Suffixes[suffix]=1 

            else:
                for i in range(len(wordlist)):
                    word = wordlist[i].Key
                    WordAnalyzedFlag = False
                    for i in range(MinimumStemLength-1, len(word)-1):
                        stem = word[-1*i:]
                        if stem in Protostems:
                            j = len(word) - i 
                            prefix = word[:j]
         
                            if len(prefix) > MaximumAffixLength:
                                continue
                            if stem not in self.StemToWord:
                                self.StemToWord[stem] = dict()
                            self.StemToWord[stem][stem]=1   
                            if stem not in self.StemToAffix:
                                self.StemToAffix[stem] = dict() 
                            self.StemToAffix[stem][prefix]=1        
                            if stem in self.WordCounts:
                                    self.StemToWord[stem][word] = 1
                                    self.StemToAffix[stem]["NULL"]=1
                            self.Prefixes[prefix]=1
         
# ----------------------------------------------------------------------------------------------------------------------------#
    def RebalanceSignatureBreaks2 (self, threshold, outfile, FindSuffixesFlag):
# this version is much faster, and does not recheck each signature; it only changes stems.
# ----------------------------------------------------------------------------------------------------------------------------#
            count=0
            MinimumNumberOfStemsInSignaturesCheckedForRebalancing = 5
            SortedListOfSignatures = sorted(self.SignatureToStems.items(), lambda x, y: cmp(len(x[1]), len(y[1])),
                                            reverse=True)        
            for (sig,wordlist) in SortedListOfSignatures:
                sigstring="-".join(sig)
                numberofstems=len(self.SignatureToStems[sig])
                 
                if numberofstems <MinimumNumberOfStemsInSignaturesCheckedForRebalancing:                
                    print >>outfile, "       Too few stems to shift material from suffixes", sigstring, numberofstems       
                    continue
                print >>outfile, "{:20s} count: {:4d} ".format(sigstring,   numberofstems),
                shiftingchunk, shiftingchunkcount  = TestForCommonEdge(self.SignatureToStems[sig], outfile, threshold, FindSuffixesFlag) 

                if shiftingchunkcount > 0:
                    print >>outfile,"{:5s} count: {:5d}".format(shiftingchunk,   shiftingchunkcount)
                else:
                    print >>outfile, "no chunk to shift"  
         
                if len(shiftingchunk) >0: 
                    count +=1                
                    chunklength = len(shiftingchunk)
                    newsignature = list()   
                    sigstring2 = ""
                    for affix in sig:
                        if affix == "NULL":
                            affix = ""
                        if FindSuffixesFlag:
                            newaffix = shiftingchunk + affix
                            sigstring2 += newaffix + " - "
                            shiftpair = (affix, newaffix)
                            sigstring2 = sigstring2[:-2] ##????
                        else:
                            newaffix = affix + shiftingchunk
                            sigstring2 += "-" + newaffix
                            shiftpair = (affix, newaffix)
                            sigstring2 = sigstring2[2:] ##???
                        newsignature.append(newaffix)
                    formatstring = "{:30s} {:10s} {:35s}  Number of stems {:5d} Number of shifters {:5d}"
                    print >>outfile, formatstring.format(sigstring, shiftingchunk, sigstring2, numberofstems, shiftingchunkcount)
                     
                    if shiftingchunkcount >= numberofstems * threshold  :
                        ChangeFlag = True
                
                        stems_to_change = list(self.SignatureToStems[sig])
                        for stem in stems_to_change:
                            if FindSuffixesFlag: 
                                if stem[-1*chunklength:] != shiftingchunk:
                                    continue
                            else:
                                if stem[:chunklength] != shiftingchunk:
                                    continue
                            if FindSuffixesFlag:                    
                                newstem = stem[:len(stem)-chunklength]
                            else:
                                newstem = stem[chunklength:]
         
                            if newstem not in self.StemToWord:
                                self.StemToWord[newstem] = dict()
                            for word in self.StemToWord[stem]:          
                                self.StemToWord[newstem][word] = 1
                            del self.StemToWord[stem] #  is this too general?                   
                            
                            if newstem not in self.StemToAffix:
                                self.StemToAffix[newstem] = {}              
                            for affix in newsignature:
                                self.StemToAffix[newstem][affix] = 1
                            del self.StemToAffix[stem]

                            if newstem not in self.StemToSignature:
                                self.StemToSignature[newstem]=dict()
                            self.StemToSignature[newstem]=[newsignature]
                            del self.StemToSignature[stem]
                        
            outfile.flush()
            return count



#--------------------------------------------------------------------------------------------------------------------------#
    def printSignatures(self, lxalogfile, outfile_signatures, outfile_wordstosigs, outfile_stemtowords, outfile_stemtowords2, outfile_SigExtensions, outfile_suffixes, encoding,
                    FindSuffixesFlag):
# ----------------------------------------------------------------------------------------------------------------------------#

        print "   Print signatures from within Lexicon class."
        # 1  Create a list of signatures, sorted by number of stems in each. DisplayList is that list. Its triples have the signature, the number of stems, and the signature's robustness.

        ColumnWidth = 35
        stemcountcutoff = self.MinimumStemsInaSignature
        SortedListOfSignatures = sorted(self.SignatureToStems.items(), lambda x, y: cmp(len(x[1]), len(y[1])),
                                        reverse=True)

        DisplayList = []
        for sig, stems in SortedListOfSignatures:
            #print "486 ", sig
            if len(stems) < stemcountcutoff:
                continue;
            DisplayList.append((sig, len(stems), getrobustness(sig, stems)))
        DisplayList.sort
 
        singleton_signatures = 0
        doubleton_signatures = 0

        for sig, stemcount, robustness in DisplayList:
            if stemcount == 1:
                singleton_signatures += 1
            elif stemcount == 2:
                doubleton_signatures += 1

        totalrobustness = 0
        for sig, stemcount, robustness in DisplayList:
            totalrobustness += robustness

        initialize_files(self, outfile_signatures,singleton_signatures,doubleton_signatures,DisplayList ) 
        initialize_files(self, lxalogfile,singleton_signatures,doubleton_signatures,DisplayList ) 
        initialize_files(self, "console",singleton_signatures,doubleton_signatures,DisplayList ) 

        if False:
            for sig, stemcount, robustness in DisplayList:
                if len(self.SignatureToStems[sig]) > 5:
                    self.Multinomial(sig,FindSuffixesFlag)
     
 

        # Print signatures (not their stems) sorted by robustness
        print_signature_list_1(outfile_signatures, DisplayList, stemcountcutoff,totalrobustness)

        # Print suffixes
        suffix_list = print_suffixes(outfile_suffixes,self.Suffixes  )

        # Print stems
        print_stems(outfile_stemtowords, outfile_stemtowords2, self.StemToWord, self.StemToSignature, self.WordCounts, suffix_list)

        # print the stems of each signature:
        print_signature_list_2(outfile_signatures, DisplayList, stemcountcutoff,totalrobustness, self.SignatureToStems, self.StemCounts, FindSuffixesFlag)

        # print WORDS of each signature:
        print_words(outfile_wordstosigs, lxalogfile, self.WordToSig,ColumnWidth )  
 
        # print signature extensions:
        print_signature_extensions(outfile_SigExtensions, lxalogfile, DisplayList, self.SignatureToStems)  
 

## -------                                                      ------- #
##              Utility functions                               ------- #
## -------                                                      ------- #
    def PrintWordCounts(self, outfile):
            formatstring = "{:20s} {:6d}"
            words = self.WordCounts.keys()
            words.sort()
            for word in words:
                    print >>outfile, formatstring.format(word, self.WordCounts[word])

    def Multinomial(self,this_signature,FindSuffixesFlag):
        counts = dict()
        total = 0.0
        #print "{:45s}".format(this_signature), 
        for affix in this_signature:
            #print "affix", affix            
            counts[affix]=0
            for stem in self.SignatureToStems[this_signature]:      
                #print "stem", stem  
                if affix == "NULL":
                    word = stem
                elif FindSuffixesFlag:
                    word = stem + affix
                else:
                    word= affix + stem
            #print stem,":", affix, "::", word
            #print "A", counts[affix], self.WordCounts[word]
            counts[affix] += self.WordCounts[word]
            total += self.WordCounts[word]
        frequency = dict()
        for affix in this_signature:
            frequency[affix] = counts[affix]/total
            #print "{:12s}{:10.2f}   ".format(affix, frequency[affix]),
        #print 

    def ComputeRobustness(self): 
        self.NumberOfAnalyzedWords= len(self.WordToSig)
        self.NumberOfUnanalyzedWords= self.WordList.GetCount() - self.NumberOfAnalyzedWords  
        for sig in self.SignatureToStems:
            numberofaffixes = len(sig)
            mystems = self.SignatureToStems[sig]
            numberofstems = len(mystems)
            AffixListLetterLength = 0
            for affix in sig:
                if affix == "NULL":
                        continue
                AffixListLetterLength += len(affix)
            StemListLetterLength = 0
            for stem in mystems:
                StemListLetterLength += len(stem)

            self.TotalRobustnessInSignatures +=  getrobustness(mystems,sig)
            self.AffixLettersInSignatures += AffixListLetterLength
    

class Word:
    def __init__(self, key):
        self.Key = key
        self.leftindex = -1
        self.rightindex = -1

def makeword(stem, affix, sideflag):
    if sideflag == True:
        return stem + affix
    else: 
        return affix + stem

def byWordKey(word):
    return word.Key


class CSignature:
    count = 0

    def __init__(self, signature_string):
        self.Index = 0
        self.Affixes = tuple(signature_string.split("-"))
        self.StartStateIndex = CSignature.count
        self.MiddleStateIndex = CSignature.Count + 1
        self.EndStateIndex = CSignature.count + 2
        self.count += 3
        self.StemCount = 1
        self.LetterSize = len(signature_string) - len(self.Affixes)
        print "710 ", signature_string, self.LetterSize

    def Display(self):
        returnstring = ""
        affixes = list(self.Affixes)
        affixes.sort()
        return "-".join(affixes)

        # ------------------------------------------------------------------------------------------##------------------------------------------------------------------------------------------#


class parseChunk:
    def __init__(self, thismorph, rString, thisedge=None):
        # print "in parsechunk constructor, with ", thismorph, "being passed in "
        self.morph = thismorph
        self.edge = thisedge
        self.remainingString = rString
        if (self.edge):
            self.fromState = self.edge.fromState
            self.toState = self.edge.toState
        else:
            self.fromState = None
            self.toState = None
            # print self.morph, "that's the morph"
            # print self.remainingString, "that's the remainder"

    def Copy(self, otherChunk):
        self.morph = otherChunk.morph
        self.edge = otherChunk.edge
        self.remainingString = otherChunk.remainingString

    def Print(self):
        returnstring = "morph: " + self.morph
        if self.remainingString == "":
            returnstring += ", no remaining string",
        else:
            returnstring += "remaining string is " + self.remainingString
        if self.edge:
            return "-(" + str(self.fromState.index) + ")" + self.morph + "(" + str(
                self.toState.index) + ") -" + "remains:" + returnstring
        else:
            return returnstring + "!" + self.morph + "no edge on this parsechunk"


            # ----------------------------------------------------------------------------------------------------------------------------#


class ParseChain:
    def __init__(self):
        self.my_chain = list()

    def Copy(self, other):
        for parsechunk in other.my_chain:
            newparsechunk = parseChunk(parsechunk.morph, parsechunk.remainingString, parsechunk.edge)
            self.my_chain.append(newparsechunk)

    def Append(self, parseChunk):
        # print "Inside ParseChain Append"
        self.my_chain.append(parseChunk)

    def Print(self, outfile):
        returnstring = ""
        columnwidth = 30
        for i in range(len(self.my_chain)):
            chunk = self.my_chain[i]
            this_string = chunk.morph + "-"
            if chunk.edge:
                this_string += str(chunk.edge.toState.index) + "-"
            returnstring += this_string + " " * (columnwidth - len(this_string))
        print >> outfile, returnstring,
        print >> outfile

    def Display(self):
        returnstring = ""
        for i in range(len(self.my_chain)):
            chunk = self.my_chain[i]
            returnstring += chunk.morph + "-"
            if chunk.edge:
                returnstring += str(chunk.edge.toState.index) + "-"
        return returnstring




# ----------------------------------------------------------------------------------------------------------------------------#
def RemakeSignatures(WordToSig, SignatureToStems, StemToWord, StemToAffix, StemToSig):
    # ----------------------------------------------------------------------------------------------------------------------------#
    return ""





# ----------------------------------------------------------------------------------------------------------------------------#
def TestForCommonEdge(stemlist, outfile,  threshold, FindSuffixesFlag):
# ----------------------------------------------------------------------------------------------------------------------------#
    WinningString = ""
    WinningCount = 0
    MaximumLengthToExplore = 6
    ExceptionCount = 0
    proportion = 0.0
    FinalLetterCount = {}
    NumberOfStems = len(stemlist) 
    WinningStringCount = dict() #key is string, value is number of stems
    for length in range(1,MaximumLengthToExplore):
        FinalLetterCount = dict()
        for stem in stemlist:            
            if len(stem) < length + 2:
                continue
            if FindSuffixesFlag:
                commonstring = stem[-1*length:]
            else:
                commonstring= stem[:length]
            if not commonstring in FinalLetterCount.keys():
                FinalLetterCount[commonstring] = 1
            else:
                FinalLetterCount[commonstring] += 1
        if len(FinalLetterCount) == 0:  # this will happen if all of the stems are of the same length and too short to do this.
            continue
        sorteditems = sorted(FinalLetterCount, key=FinalLetterCount.get, reverse=True)  # sort by value
        CommonLastString = sorteditems[0]
        CommonLastStringCount = FinalLetterCount[CommonLastString]
        WinningStringCount[CommonLastString]=CommonLastStringCount
        
        if  CommonLastStringCount >= threshold * NumberOfStems:
            Winner = CommonLastString
            WinningStringCount[Winner]=CommonLastStringCount
            continue

        else:
            if length > 1:           
                WinningString = Winner # from last iteration
                WinningCount = WinningStringCount[WinningString]
            else:
                WinningString = ""
                WinningCount = 0
            break
         
        
    # ----------------------------------------------------------------------------------------------------------------------------#
    return (WinningString, WinningCount )


# ----------------------------------------------------------------------------------------------------------------------------#


 








#
def getrobustness(sig, stems):
    # ----------------------------------------------------------------------------------------------------------------------------#
    countofsig = len(sig)
    countofstems = len(stems)
    lettersinstems = 0
    lettersinaffixes = 0
    for stem in stems:
        lettersinstems += len(stem)
    for affix in sig:
        lettersinaffixes += len(affix)
    # ----------------------------------------------------------------------------------------------------------------------------#
    return lettersinstems * (countofsig - 1) + lettersinaffixes * (countofstems - 1)


# ----------------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------#
def FindSignature_LetterCountSavings(Signatures, sig):
	affixlettercount = 0
	stemlettercount = 0
	numberOfAffixes = len(sig)
	numberOfStems = len(Signatures[sig])
	for affix in sig:
		affixlettercount += len(affix) + 1
	for stem in Signatures[sig]:
		stemlettercount += len(stem) + 1
	lettercountsavings = affixlettercount * (numberOfStems - 1) + stemlettercount * (numberOfAffixes - 1)
	return lettercountsavings

# ----------------------------------------------------------------------------------------------------------------------------#
 
# --
# ----------------------------------------------------------------------------------------------------------------------------#

def MakeStringFromAlternation(s1,s2,s3,s4):
	if s1== "":
		s1 = "nil"
	if s2== "NULL":
		s2 = "#"
	if s3== "":
		s3 = "nil"
	if s4== "NULL":
		s4 = "#"

	str = "{:4s} before {:5s}, and {:4s} before  {:5s}".format(s1,s2,s3,s4)
	return str

# ----------------------------------------------------------------------------------------------------------------------------#
