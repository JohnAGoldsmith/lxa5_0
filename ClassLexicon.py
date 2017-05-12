import math
import sys

from printing_to_files import *
from signaturefunctions import *


# This is just part of documentation:
# A signature is a tuple of strings (each an affix).
# Signatures is a map: its keys are signatures.  Its values are *sets* of stems.
# StemToWord is a map; its keys are stems.       Its values are *sets* of words.
# StemToSig  is a map; its keys are stems.       Its values are individual signatures.
# WordToSig  is a Map. its keys are words.       Its values are *lists* of signatures.
# StemCorpusCounts is a map. Its keys are words.   Its values are corpus counts of stems.
# SignatureStringsToStems is a dict: its keys are tuples of strings, and its values are dicts of stems.



def splitsignature(signature, maxlength):
    affixes = signature.split('=')
    line = list()
    length = 0
    outlist = list()
    for affix in affixes:
        line.append(affix)
        length += len(affix) + 1
        if length > maxlength:
            outlist.append("=".join(line) + "...")
            line = list()
            length = 0
    outlist.append("=".join(line))
    return outlist


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

            # not currently used

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

        #static variable:
        reportnumber = 1

        self.Corpus = list()
        self.Parses = dict()
        self.WordList = CWordList()
        self.Words = list()
        self.WordCounts = dict()
        self.ReverseWordList = list()
        self.WordToSig = {}
        self.StemToWord = {}
        self.StemToAffix = {}  # value is a Dict whose keys are affixes.
        self.StemToSignature = {}  # value is a string with hyphens
        self.SignatureStringsToStems = {}
        self.UnlikelySignatureStringsToStems = {}
        self.UnlikelyStems = {}
        self.StemCorpusCounts = {}
        self.Suffixes = {}
        self.Prefixes = {}
        self.WordBiographies=dict()
        self.MinimumStemsInaSignature = 5
        self.MinimumAffixesInaSignature = 2
        self.MinimumStemLength = 3
        self.MaximumAffixLength = 5
        self.MaximumNumberOfAffixesInASignature = 100
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
    def MakeSignatures(self, lxalogfile, outfile_Rebalancing_Signatures, outfile_unlikelysignatures,
                       outfile_subsignatures, FindSuffixesFlag, MinimumStemLength, verboseflag = False):
        # ----------------------------------------------------------------------------------------------------------------------------#

        verboseflag = True
        formatstring1 = "  {:50s}{:>10,}"
        formatstring2 = "  {:50s}"
        formatstring3 = "{:40s}{:10,d}"
        print formatstring2.format("The MakeSignatures function")

        # Protostems are candidate stems made during the algorithm, but not kept afterwards.
        Protostems = dict()
        self.NumberOfAnalyzedWords = 0
        self.LettersInAnalyzedWords = 0
        self.NumberOfUnanalyzedWords = 0
        self.LettersInUnanalyzedWords = 0

        AnalyzedWords = dict()
        # Lexicon.TotalLetterCountInWords = 0

        self.TotalRobustnessInSignatures = 0
        self.LettersInStems = 0
        self.TotalLetterCostOfAffixesInSignatures = 0
        self.LettersInStems = 0
        self.TotalLetterCostOfAffixesInSignatures = 0
        if FindSuffixesFlag:
            Affixes = self.Suffixes
        else:
            Affixes = self.Prefixes

        # 1 --------------------------------------------------------------------

        Step = 1
        maximumstemlength = 100
        self.FindProtostems(self.WordList.mylist, Protostems, self.MinimumStemLength, FindSuffixesFlag,verboseflag,Step,maximumstemlength)
        print formatstring1.format("1. Finished finding proto-stems.", len(Protostems))

        # 2 and 3 --------------------------------------------------------------------
        Step = 2
        self.AssignAffixesAndWordsToStems(Protostems, FindSuffixesFlag,Step,verboseflag )
        print formatstring1.format("2 and 3. Finished finding affixes for protostems.",
                                   len(self.Suffixes) + len(self.Prefixes))
        # file 2 is fine
        # file 3 is fine.
        # problem already exists, of having both NULL and null with emerge? not on 3 parse pair list though.???
        # --------------------------------------------------------------------
        # 4  Assign signatures to each stem This is in a sense the most important step.        -------
        Step = 3
        self.AssignSignaturesToEachStem(FindSuffixesFlag,verboseflag,Step)
        print  formatstring1.format("4. Finished first pass of finding stems, affixes, and signatures.",
                                    len(self.SignatureStringsToStems))
        # --------------------------------------------------------------------
        # 3  Find good signatures inside signatures that don't have enough stems to be their own signatures.
        # We make a temporary list of signatures called GoodSignatures, which have enough stems. 
        # We check all sigs in SignaturesToStems to see if they have enough stems. If they do not,
        # we look to see if we can find a Good Signature inside it. If not, we delete it; and we delete
        # the analyses that were not handled by the Good Signature. 

        print  formatstring1.format("3. Looking for good signatures inside bad ones.", len(self.SignatureStringsToStems))

        Step += 1
        self.FindGoodSignaturesInsideBad(outfile_subsignatures, FindSuffixesFlag,verboseflag, Step);

        print formatstring2.format("4. Thinning out stems with too few affixes:")
        N = 1
        Step += 1
        self.RemoveAllSignaturesWithOnly_N_affixes(N,verboseflag, Step)
        print formatstring2.format("4. Finished; we will reassign signature structure.")
        print formatstring2.format("6. Recompute signature structure.")
        Step += 1
        self.AssignSignaturesToEachStem(FindSuffixesFlag, verboseflag,Step)

        # --------------------------------------------------------------------
        # 4 Rebalancing now, which means:                  -------
        # We look for a stem-final sequence that appears on all or almost all the stems, and shift it to affixes.
        # Make changes in Lexicon.SignatureStringsToStems, and .StemToSig, and .WordToSig, and .StemToWord, and .StemToAffix  and signature_tuples....

        print formatstring2.format("5. Find shift stem/affix boundary when appropriate.")
        threshold = 0.80

        if False:

            count = self.RebalanceSignatureBreaks(threshold, outfile_Rebalancing_Signatures, FindSuffixesFlag,Step)
            print formatstring2.format("5. Completed.")
            print formatstring2.format("6. Recompute signature structure.")
            self.AssignSignaturesToEachStem(FindSuffixesFlag,Step)

        # --------------------------------------------------------------------
        # 5  ------- compute robustness
        self.ComputeRobustness()
        print  formatstring2.format("6. Computed robustness")

        # 6  ------- Print
        print >> lxalogfile, formatstring3.format("Number of analyzed words", self.NumberOfAnalyzedWords)
        print >> lxalogfile, formatstring3.format("Number of unanalyzed words", self.NumberOfUnanalyzedWords)
        print >> lxalogfile, formatstring3.format("Letters in stems", self.LettersInStems)
        print >> lxalogfile, formatstring3.format("Letters in affixes", self.AffixLettersInSignatures)
        print >> lxalogfile, formatstring3.format("Total robustness in signatures", self.TotalRobustnessInSignatures)

        return

    # ----------------------------------------------------------------------------------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------------------------#
    def RemoveAllSignaturesWithOnly_N_affixes(self, N, verboseflag, Step):
        ListOfStemsToRemove = list()
        if verboseflag:
            print "\n\n Removing all signatures with only", N, "affixes."
        for stem in self.StemToAffix:
            if len(self.StemToAffix[stem]) <= N:
                ListOfStemsToRemove.append(stem)

        for stem in ListOfStemsToRemove:
            if verboseflag:
                print "\tstem"
            del self.StemToWord[stem]
            del self.StemToAffix[stem]
        if verboseflag:
            print "End of removing signatures with too few affixes."
        # ----------------------------------------------------------------------------------------------------------------------------#
        # -------------------------------------------------------verboseflag,Step---------------------------------------------------------------------#

    def AssignSignaturesToEachStem(self, FindSuffixesFlag,verboseflag,Step):
        """ This assumes StemToWord and StemToAffix, and creates:
            Affixes
            SignatureStringsToStems
            StemToSignature
            StemCorpusCounts
            WordToSig """


        self.StemCorpusCounts = dict()
        # This creates StemToWord; StemToAffixes; Affixes; 
        self.Affixes = dict()
        self.SignatureStringsToStems = dict()
        self.StemToSignature = dict()
        self.StemCorpusCounts = dict()
        self.StemToWord = dict()
        self.WordToSig = dict()
        self.StemToAffix = dict()
        formatstring2 = "{0:15s} {1:15s}"
        formatstring3 = "\n{0:15s} {1:15s} {2:10s} "
        formatstring4 = "\n{0:15s} {1:15s} {2:10s} {3:20s}"


  # --------              Part One     ----------------- Collect each affix a stem has.
        if verboseflag:
                filename = "4_stems_and_their_affix_sets.txt"
                headerlist = [ "Link stems to the set of their affixes."]
                contentlist = list()

                formatstring = "{0:20s}  {1:15s} {2:20s}{3:10s}"
                formatstring1 = "{0:32s}"


        if verboseflag:
            print "Assign affix sets to each stem: Part 1\n Find affixes for each protostem"
        ParseList = list()


        if FindSuffixesFlag:
            for stem,affix in self.Parses:
                ParseList.append((stem,affix))
            ParseList.sort(key=lambda (x,y) : x+" "+y)
            #for stem, affix in self.Parses:
            for stem,affix in ParseList:
                if stem not in self.StemToWord:

                    self.StemToWord[stem] = dict()
                    self.StemToAffix[stem] = dict()
                if affix == "NULL":
                    word = stem
                else:
                    word = stem + affix

                self.StemToWord[stem][word] = 1
                self.StemToAffix[stem][affix] = 1
                if affix not in self.Suffixes:
                    self.Suffixes[affix] = 0
                self.Suffixes[affix] += 1
                #print "\n258", word , stem, affix
                self.WordBiographies[word].append(str(Step) + " This split:" + stem + "=" + affix)

            if verboseflag:
                    stemlist = self.StemToWord.keys()
                    stemlist.sort()
                    for stem in stemlist:
                        affixset = self.StemToAffix[stem].keys()
                        affixset.sort()
                        reportline = formatstring2.format(stem, "=".join(affixset) )
                        contentlist.append(reportline)


            if verboseflag:
                print_report(filename, headerlist, contentlist)

        # --------              Part Two      ----------------- Remove stems that have two few affixes
        if verboseflag:
                filename = "5_delete_bad_protostems.txt"
                headerlist = [ "Delete bad protostems"]
                contentlist = list()


        if FindSuffixesFlag:


            StemsToDelete = list()
            for stem in self.StemToWord:
                if len(self.StemToAffix[stem]) < self.MinimumAffixesInaSignature:
                    StemsToDelete.append(stem)
                    if verboseflag:
                        contentlist.append(formatstring3.format(stem, "too few affixes in sig.", self.StemToAffix[stem]))
            for stem in StemsToDelete:
                #print "we are deleting this stem:", stem
                for word in self.StemToWord[stem]:
                    self.WordBiographies[word].append(" This stem was deleted: " + stem)
                del self.StemToWord[stem]
                del self.StemToAffix[stem]

            if verboseflag:
                print_report(filename, headerlist, contentlist)


        # --------              Part Three       -----------------

 # Now we create signatures: StemToSignature; WordToSig; StemToWord, SignatureStringsToStems



            if verboseflag:
                filename = "6_stems_and_their_affix_sets.txt"
                headerlist = [ "6. Assign a single signature to each stem."]
                contentlist = list()

                formatstring = "{0:20s}  {1:15s} {2:20s}{3:10s}"
                formatstring1 = "{0:32s}"

            stemlist = self.StemToAffix.keys()
            stemlist.sort()

            if verboseflag:
                print "\n\nPart 2\nAssign a single signature to each stem\n"
            #for stem in self.StemToAffix:
            for stem in stemlist:
                  # we go through this three times. the first time emerge is fine; but the 2nd and 3rd it's bad.
                #print "314", stem, (self.StemToAffix[stem]) # emerge is OK here.
                signature_string = MakeSignatureStringFromAffixDict(self.StemToAffix[stem])

                #print "315", stem, (self.StemToAffix[stem]), signature_string
                self.StemToSignature[stem] = signature_string
                #if verboseflag:
                #    print formatstring2.format( stem, signature_string)
                self.StemCorpusCounts[stem] = 0
                for word in self.StemToWord[stem]:
                    if word not in self.WordToSig:
                        self.WordToSig[word] = list()
                    if signature_string not in self.WordToSig[word]:
                        self.WordToSig[word].append((stem, signature_string))
                    self.StemToWord[stem][word] = 1
                    self.StemCorpusCounts[stem] += self.WordCounts[word]
                if signature_string not in self.SignatureStringsToStems:
                    self.SignatureStringsToStems[signature_string] = dict()
                self.SignatureStringsToStems[signature_string][stem] = 1
                #print "332", signature_string
            if verboseflag:
                print "\nEnd of assigning a signature to each stem."


            # ----------------------------------------------------------------------------------------------------------------------------#
            # ----------------------------------------------------------------------------------------------------------------------------#
            # This is apparently not used anymore.

    def RemoveSignaturesWithTooFewStems(self):
        for sig in self.SignatureStringsToStems:
            if len(self.SignatureStringsToStems[sig]) < self.MinimumStemsInaSignature:
                for stem in self.SignatureStringsToStems[sig]:
                    del self.StemToSignature[stem]
                    for word in self.StemToWord[stem]:
                        if len(self.WordToSig[word]) == 1:
                            del self.WordToSig[word]
                        else:
                            self.WordToSig[word].remove(sig)
                    del self.StemToWord[stem]

                # ----------------------------------------------------------------------------------------------------------------------------#




                # -----------------------------------------------------------------------------------------------------------------------------#

    def FindProtostems(self, wordlist, Protostems, minimum_stem_length, FindSuffixesFlag,verboseflag,Step, maximum_stem_length=-1):
        # A "maximum_stem_length" is included here so that we can use this function to explore
        # for stems shorter than the minimum that was assumed on an earlier iteration.
        if verboseflag:
            filename = "1_FindProtoStems.txt"
            headerlist = [ "Find proto-stems"]
            contentlist = list()
            formatstring = "{0:20s} Comparison span: {1:4s} {2:20s} {3:20s}."

            print "Finding protostems.", "Maximum stem length: ", maximum_stem_length
            formatstring2 = "{0:15s} {1:15s}"
            formatstring1 = "{0:20s} {1:5n} {2:20s}{3:32s}"
        previousword = ""
        if FindSuffixesFlag:
            for i in range(len(wordlist)):
                word = wordlist[i].Key
                differencefoundflag = False
                if previousword == "":  # only on first iteration
                    previousword = word
                    continue
                begin=minimum_stem_length
                if maximum_stem_length > 0:
                    end = min(len(word), len(previousword), maximum_stem_length)
                else:
                    end = min(len(word), len(previousword))
                for j in range(end):

                    if word[j] != previousword[j]:  # will a stem be found in the very first word?
                        differencefoundflag = True
                        stem = word[:j]
                        if len(stem) >= minimum_stem_length:
                            self.WordBiographies[word].append(str(Step) + " Found stem " + stem)
                            if stem not in Protostems:
                                Protostems[stem] = 1
                                if verboseflag:
                                    reportline = formatstring1.format(word,  end, stem, "New stem.")
                                    contentlist.append(reportline)
                            else:
                                if verboseflag:
                                    reportline = formatstring1.format(word,   end, stem, "Known stem.")
                                    contentlist.append(reportline)
                                Protostems[stem] += 1
                        else:
                            if verboseflag:
                                reportline = formatstring1.format(word,  end, stem, "Too small.")
                                contentlist.append(reportline)
                        previousword = word
                        break
                if differencefoundflag:
                    continue
                else:  # there no were differences between this word and the preceding word, on the length that they both shared.

                    if (len(word)) >= len(previousword):
                        if len(previousword) >= minimum_stem_length:
                            if (previousword not in Protostems):
                                if verboseflag:
                                    reportline = formatstring1.format(word,   end, previousword, "New stem.")
                                    contentlist.append(reportline)
                                Protostems[previousword] = 1
                                self.WordBiographies[previousword].append(str(Step) + " This word is a stem.")
                            else:
                                Protostems[previousword] += 1
                                if verboseflag:
                                   reportline = formatstring1.format(word,   end, stem, "Known stem.")
                                   contentlist.append(reportline)
                        else:
                            if verboseflag:
                                reportline = formatstring1.format(word,   end, "", "Too short.")
                                contentlist.append(reportline)
                    previousword = word






        else:
            # print "prefixes"
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
                for i in range(1, span, ):
                    if word[-1 * i] != previousword[-1 * i]:
                        differencefoundflag = True
                        stem = word[-1 * i + 1:]
                        if len(stem) >= minimum_stem_length:
                            if stem not in Protostems:
                                Protostems[stem] = 1
                            else:
                                Protostems[stem] += 1
                                # print previousword, word, stem
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



        if verboseflag:
            print_report(filename, headerlist, contentlist)

                # ----------------------------------------------------------------------------------------------------------------------------#

    def AssignAffixesAndWordsToStems(self, Protostems, FindSuffixesFlag,Step, verboseflag = False):
        # This function creates the pairs in Parses. Most words have multiple appearances.
        if verboseflag:
            print "Assign affixes and words to stems."
            filename = "2_All_initial_word_splits.txt"
            headerlist = [ "Assign affixes and words to stems"]
            contentlist = list()
            linelist = list()
            formatstring = "{0:20s}   {1:20s} {2:10s} {3:20s}"
        wordlist = self.WordList.mylist
        MinimumStemLength = self.MinimumStemLength
        MaximumAffixLength = self.MaximumAffixLength
        column_no = 0
        NumberOfColumns = 8
        formatstring4 = "{0:15s} {1:15s} {2:10} {3:12}"
        if FindSuffixesFlag:
            for i in range(len(wordlist)):
                if i % 5000 == 0:
                    if verboseflag == False:
                        print "{:7,d}".format(i),
                        sys.stdout.flush()
                        column_no += 1
                        if column_no % NumberOfColumns == 0:
                            column_no = 0
                            print "\n" + " " * 4,
                word = wordlist[i].Key
                #if verboseflag:
                #            contentlist.append("510 "+word)
                WordAnalyzedFlag = False
                for i in range(len(word), MinimumStemLength - 1, -1):  # the first was len(word) - 1
                    if FindSuffixesFlag:
                        stem = word[:i]
                        #if verboseflag:
                        #    contentlist.append("514 "+stem)
                    else:
                        stem = word[-1 * i:]
                    if stem in Protostems:
                        if FindSuffixesFlag:
                            suffix = word[i:]
                            if len(suffix) > MaximumAffixLength:
                                self.WordBiographies[word].append(str(Step) + " The split "+stem+ " / " + suffix + "bad; suffix too long.")
                                if verboseflag:
                                    reportline = formatstring.format(word,stem,suffix, "suffix too long.")
                                    contentlist.append(reportline)
                                continue
                            if len(suffix) == 0:
                                suffix = "NULL"
                            if verboseflag:
                                reportline = formatstring.format(word,stem,suffix, " suffix is good.")
                                contentlist.append(reportline)
                            self.WordBiographies[word].append(str(Step) + " The split "+stem+ " / " + suffix + " is good.")
                            self.Parses[(stem, suffix)] = 1
                            if stem in self.WordCounts:
                                self.Parses[(stem, "NULL")] = 1
                        else:
                            j = len(word) - i
                            prefix = word[:j]
                            if len(prefix) > MaximumAffixLength:
                                continue
                            self.Parses[(prefix, stem)] = 1
                            if stem in self.WordCounts:
                                self.Parses[("NULL", stem)] = 1
            if verboseflag:
                print_report(filename, headerlist, contentlist)


        if verboseflag:
            filename = "3_parse_pairs.txt"
            headerlist = [ "List of parse pairs"]
            contentlist = list()
            linelist = list()
            formatstring = "{0:20s}   {1:20s} {2:10s} {3:20s}"
            templist=list()
            print_report(filename, headerlist, contentlist)
            for item in self.Parses:
                #print  "583", item , item[0], item[1]
                if FindSuffixesFlag:
                    stem = item[0]
                    affix = item[1]
                templist.append (stem +' ' + affix )
                if affix == "NULL":
                    word = stem
                else:
                    word = stem + affix
                self.WordBiographies[word].append(str(Step) + " "+ item[0] + " " + item[1])
            templist.sort()
            for item in templist:
                    contentlist.append(item)
            print_report(filename, headerlist, contentlist)


    # ----------------------------------------------------------------------------------------------------------------------------#
    def RebalanceSignatureBreaks(self, threshold, outfile, FindSuffixesFlag,verboseflag = True):
        # this version is much faster, and does not recheck each signature; it only changes stems.
        # ----------------------------------------------------------------------------------------------------------------------------#
        if verboseflag:
            print "Rebalance signature breaks."
            filename = "6_Rebalance_signature_breaks.txt"
            headerlist = [ " "]
            contentlist = list()
            linelist = list()
            formatstring = "{0:20s}   {1:20s} {2:10s} {3:20s}"
        count = 0
        MinimumNumberOfStemsInSignaturesCheckedForRebalancing = 5
        SortedListOfSignatures = sorted(self.SignatureStringsToStems.items(), lambda x, y: cmp(len(x[1]), len(y[1])),
                                        reverse=True)
        maximumlengthofsignature = 0
        for (sig_string, wordlist) in SortedListOfSignatures:
            if len(sig_string) > maximumlengthofsignature:
                maximumlengthofsignature = len(sig_string)
        for (sig_string, wordlist) in SortedListOfSignatures:
            sig_list = MakeSignatureListFromSignatureString(sig_string)
            numberofstems = len(self.SignatureStringsToStems[sig_string])

            if numberofstems < MinimumNumberOfStemsInSignaturesCheckedForRebalancing:
                print >> outfile, "       Too few stems to shift material from suffixes", sig_string, numberofstems
                continue
            # print >>outfile, "{:20s} count: {:4d} ".format(sig_string,   numberofstems),
            shiftingchunk, shiftingchunkcount = TestForCommonEdge(self.SignatureStringsToStems[sig_string], outfile,
                                                                  threshold, FindSuffixesFlag)

            if shiftingchunkcount > 0:
                print >> outfile, sig_string, " " * (maximumlengthofsignature - len(sig_string)),
                print >> outfile, "Stem count: {:4d} {:5s} count: {:5d}".format(numberofstems, shiftingchunk,
                                                                                shiftingchunkcount)
            else:
                print >> outfile, sig_string, " " * (maximumlengthofsignature - len(sig_string)),
                print >> outfile, "Stem count: {:4d}.".format(numberofstems)
            if len(shiftingchunk) > 0:
                count += 1
                chunklength = len(shiftingchunk)
                newsignature = list()
                for affix in sig_list:
                    if FindSuffixesFlag:
                        newaffix = shiftingchunk + affix
                    else:
                        newaffix = affix + shiftingchunk
                    newsignature.append(newaffix)

                if shiftingchunkcount >= numberofstems * threshold:
                    ChangeFlag = True
                    stems_to_change = list(self.SignatureStringsToStems[sig_string])
                    for stem in stems_to_change:
                        if FindSuffixesFlag:
                            if stem[-1 * chunklength:] != shiftingchunk:
                                continue
                        else:
                            if stem[:chunklength] != shiftingchunk:
                                continue

                        if FindSuffixesFlag:
                            newstem = stem[:len(stem) - chunklength]
                            for affix in sig_list:

                                if affix == "":
                                    affix_t = "NULL"
                                else:
                                    affix_t = affix
                                #print "612", stem, affix_t
                                del self.Parses[(stem, affix_t)]
                                newaffix = shiftingchunk + affix_t
                                self.Parses[(newstem, newaffix)] = 1
                                #print "615 {0:20s} {1:20s} {2:20s} {3:20s}".format(stem, affix, newstem,  newaffix )
                        else:
                            newstem = stem[chunklength:]
                            for affix in sig_list:
                                del self.Parses[(affix, stem)]
                                newaffix = affix + shiftingchunk
                                self.Parses[(newaffix, newstem)] = 1

        outfile.flush()
        print_report(filename, headerlist, contentlist)

        return count

    # --------------------------------------------------------------------------------------------------------------------------#
    def printSignatures(self, lxalogfile, outfile_signatures, outfile_unlikelysignatures, outfile_wordstosigs,
                        outfile_stemtowords, outfile_stemtowords2, outfile_SigExtensions, outfile_suffixes, encoding,
                        FindSuffixesFlag):
        # ----------------------------------------------------------------------------------------------------------------------------#

        print "   Print signatures from within Lexicon class."
        # 1  Create a list of signatures, sorted by number of stems in each. DisplayList is that list. Its 4-tuples   have the signature, the number of stems, and the signature's robustness, and a sample stem

        ColumnWidth = 35
        stemcountcutoff = self.MinimumStemsInaSignature
        SortedListOfSignatures = sorted(self.SignatureStringsToStems.items(), lambda x, y: cmp(len(x[1]), len(y[1])),
                                        reverse=True)

        DisplayList = []
        for sig, stems in SortedListOfSignatures:
            if len(stems) < stemcountcutoff:
                continue;
            # print 464, sig, stems
            if sig in self.SignatureStringsToStems:
                stems = self.SignatureStringsToStems[sig].keys()
                DisplayList.append((sig, len(stems), getrobustness(sig, stems), stems[0]))
        DisplayList.sort

        singleton_signatures = 0
        doubleton_signatures = 0

        for sig, stemcount, robustness, stem in DisplayList:
            if stemcount == 1:
                singleton_signatures += 1
            elif stemcount == 2:
                doubleton_signatures += 1

        totalrobustness = 0
        for sig, stemcount, robustness, stem in DisplayList:
            totalrobustness += robustness

        initialize_files(self, outfile_signatures, singleton_signatures, doubleton_signatures, DisplayList)
        initialize_files(self, lxalogfile, singleton_signatures, doubleton_signatures, DisplayList)
        initialize_files(self, "console", singleton_signatures, doubleton_signatures, DisplayList)

        if False:
            for sig, stemcount, robustness in DisplayList:
                if len(self.SignatureStringsToStems[sig]) > 5:
                    self.Multinomial(sig, FindSuffixesFlag)

        # Print signatures (not their stems) sorted by robustness
        print_signature_list_1(outfile_signatures, DisplayList, stemcountcutoff, totalrobustness)

        # Print suffixes
        suffix_list = print_suffixes(outfile_suffixes, self.Suffixes)

        # Print stems
        print_stems(outfile_stemtowords, outfile_stemtowords2, self.StemToWord, self.StemToSignature, self.WordCounts,
                    suffix_list)

        # print the stems of each signature:
        print_signature_list_2(outfile_signatures, lxalogfile, DisplayList, stemcountcutoff, totalrobustness,
                               self.SignatureStringsToStems, self.StemCorpusCounts, FindSuffixesFlag)

        # print WORDS of each signature:
        print_words(outfile_wordstosigs, lxalogfile, self.WordToSig, ColumnWidth)

        # print unlikely signatures:
        print_unlikelysignatures(outfile_unlikelysignatures, self.UnlikelySignatureStringsToStems, ColumnWidth)


        # print signature extensions:

    # print_signature_extensions(outfile_SigExtensions, lxalogfile, DisplayList, self.SignatureStringsToStems)



    # ----------------------------------------------------------------------------------------------------------------------------#
    def FindGoodSignaturesInsideBad(self, outfile, FindSuffixesFlag, verboseflag, Step):
        # ----------------------------------------------------------------------------------------------------------------------------#
        if verboseflag:
            print "Find good signatures inside bad.."
            filename = "6_good_signatures_inside_bad.txt"
            headerlist = [ "Find good signatures inside bad ones."]
            contentlist = list()
            linelist = list()
            formatstring = "{0:20s}   {1:20s} {2:10s} {3:20s}"
            contentlist.append("Good signature              Bad signature")

        GoodSignatures = list()
        Transactions = list()
        SignatureList = self.SignatureStringsToStems.keys()
        SignatureList.sort()
        for sig_string in SignatureList:
            #print "784", sig_string
            sig_list = MakeSignatureListFromSignatureString(sig_string)
            #print "786", sig_list
            if len(self.SignatureStringsToStems[sig_string]) > self.MinimumStemsInaSignature:
                GoodSignatures.append(sig_string)
                if verboseflag:
                    contentlist.append (sig_string)
            elif verboseflag:
                if len(sig_string) < 50 :
                    contentlist.append(" "*20 + sig_string)
                else:
                    sig_list = splitsignature(sig_string,40)
                    for item in sig_list:
                        contentlist.append(" "*20 + item )
        if verboseflag:
            contentlist.append("\n\n Working on bad signatures\n ")


        for sig_string in self.SignatureStringsToStems.keys():

            sig_list = MakeSignatureListFromSignatureString(sig_string)
            if verboseflag:
                contentlist.append(sig_string + " " +  "=".join(sig_list))
            if sig_string in GoodSignatures:
                continue
            good_sig = FindGoodSignatureInsideAnother(sig_list, GoodSignatures)
            #print "800", sig_list, good_sig
            for affix in sig_list:
                if len(affix) == 0:
                    print "803", sig_list
                    print self.SignatureStringsToStems[sig_string]
            transaction = dict()
            Transactions.append(transaction)
            transaction["sig"] = sig_string
            if (good_sig):
                transaction["subsig"] = good_sig
                good_sig_list = MakeSignatureListFromSignatureString(good_sig)
                for stem in self.SignatureStringsToStems[sig_string]:
                    for affix in good_sig_list:
                        #print  "812", good_sig_list, affix
                        if FindSuffixesFlag:
                            good_parse = (stem, affix)
                        else:
                            good_parse = (affix, stem)
                        self.Parses[good_parse] = 1

                remaining_affixes = set(sig_list) - set(good_sig_list)

                unlikelysignature = list(remaining_affixes)
                unlikelysignature.sort()
                unlikelysignature = '='.join(unlikelysignature)
                self.UnlikelySignatureStringsToStems[unlikelysignature] = dict()
                transaction["badsig"] = unlikelysignature
                for stem in self.SignatureStringsToStems[sig_string]:

                    self.UnlikelySignatureStringsToStems[unlikelysignature][stem] = 1
                    for affix in remaining_affixes:

                        if FindSuffixesFlag:
                            if affix == "":
                                affix = "NULL"

                            bad_parse = (stem, affix)
                        else:
                            bad_parse = (affix, stem)
                        del self.Parses[bad_parse]

            else:
                transaction["badsig"] = sig_string
                #print "839", sig_string
                for stem in self.SignatureStringsToStems[sig_string]:
                    for affix in sig_list:
                        if len(affix)==0:
                            bad_parse=(stem, "NULL")
                        else:
                            bad_parse = (stem, affix)
                        del self.Parses[bad_parse]
        Successes = list()
        maxlength = 0
        for transaction in Transactions:
            if "subsig" in transaction and len(transaction["subsig"]) > maxlength:
                maxlength = len(transaction["subsig"])

        for transaction in Transactions:
            if "subsig" in transaction:
                sig_list = MakeSignatureListFromSignatureString(transaction["subsig"])
                if len(sig_list) < 2:
                    continue
                Successes.append(transaction)
            # Successes.sort(key = lambda L:len(L["subsig"])  )
        Successes.sort(key=lambda L: L["subsig"])

        if verboseflag:
            print_report(filename, headerlist, contentlist)

        maxlength = 0
        for transaction in Successes:
            if len(transaction["subsig"]) > maxlength:
                maxlength = len(transaction["subsig"])

        for transaction in Successes:
            print >> outfile, transaction["subsig"] + " " * (maxlength - len(transaction["subsig"])) + transaction[
                "badsig"]

        self.AssignSignaturesToEachStem(FindSuffixesFlag,verboseflag,Step)

    ## -------                                                      ------- #
    ##              Utility functions                               ------- #
    ## -------                                                      ------- #
    def PrintWordCounts(self, outfile):
        formatstring = "{:20s} {:6d}"
        words = self.WordCounts.keys()
        words.sort()
        for word in words:
            print >> outfile, formatstring.format(word, self.WordCounts[word])

    def Multinomial(self, this_signature, FindSuffixesFlag):
        counts = dict()
        total = 0.0
        # print "{:45s}".format(this_signature),
        for affix in this_signature:
            # print "affix", affix
            counts[affix] = 0
            for stem in self.SignatureStringsToStems[this_signature]:
                # print "stem", stem
                if affix == "NULL":
                    word = stem
                elif FindSuffixesFlag:
                    word = stem + affix
                else:
                    word = affix + stem
            # print stem,":", affix, "::", word
            # print "A", counts[affix], self.WordCounts[word]
            counts[affix] += self.WordCounts[word]
            total += self.WordCounts[word]
        frequency = dict()
        for affix in this_signature:
            frequency[affix] = counts[affix] / total
            # print "{:12s}{:10.2f}   ".format(affix, frequency[affix]),
            # print

    def ComputeRobustness(self):
        self.NumberOfAnalyzedWords = len(self.WordToSig)
        self.NumberOfUnanalyzedWords = self.WordList.GetCount() - self.NumberOfAnalyzedWords
        for sig in self.SignatureStringsToStems:
            numberofaffixes = len(sig)
            mystems = self.SignatureStringsToStems[sig]
            numberofstems = len(mystems)
            AffixListLetterLength = 0
            for affix in sig:
                if affix == "NULL":
                    continue
                AffixListLetterLength += len(affix)
            StemListLetterLength = 0
            for stem in mystems:
                StemListLetterLength += len(stem)

            self.TotalRobustnessInSignatures += getrobustness(mystems, sig)
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
        self.Affixes = tuple(signature_string.split("="))
        self.StartStateIndex = CSignature.count
        self.MiddleStateIndex = CSignature.Count + 1
        self.EndStateIndex = CSignature.count + 2
        self.count += 3
        self.StemCount = 1
        self.LetterSize = len(signature_string) - len(self.Affixes)
        self.Stems = dict()  # key is stem and value is corpus count of the stem
        self.StemToWordCount = dict()  # key is stem and value is a dict; key of that dict is an affix and value is corpus count of that stem+affix

    def Display(self):
        returnstring = ""
        affixes = list(self.Affixes)
        affixes.sort()
        return "=".join(affixes)

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
            this_string = chunk.morph + "="
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
def TestForCommonEdge(stemlist, outfile, threshold, FindSuffixesFlag):
    # ----------------------------------------------------------------------------------------------------------------------------#
    WinningString = ""
    WinningCount = 0
    MaximumLengthToExplore = 6
    ExceptionCount = 0
    proportion = 0.0
    FinalLetterCount = {}
    NumberOfStems = len(stemlist)
    WinningStringCount = dict()  # key is string, value is number of stems
    # print "926", stemlist
    for length in range(1, MaximumLengthToExplore):
        FinalLetterCount = dict()
        for stem in stemlist:
            if len(stem) < length + 2:
                continue
            if FindSuffixesFlag:
                commonstring = stem[-1 * length:]
            else:
                commonstring = stem[:length]
            if not commonstring in FinalLetterCount.keys():
                FinalLetterCount[commonstring] = 1
            else:
                FinalLetterCount[commonstring] += 1
        if len(
                FinalLetterCount) == 0:  # this will happen if all of the stems are of the same length and too short to do this.
            continue
        sorteditems = sorted(FinalLetterCount, key=FinalLetterCount.get, reverse=True)  # sort by value
        CommonLastString = sorteditems[0]
        CommonLastStringCount = FinalLetterCount[CommonLastString]
        WinningStringCount[CommonLastString] = CommonLastStringCount

        if CommonLastStringCount >= threshold * NumberOfStems:
            Winner = CommonLastString
            WinningStringCount[Winner] = CommonLastStringCount
            continue

        else:
            if length > 1:
                WinningString = Winner  # from last iteration
                WinningCount = WinningStringCount[WinningString]
            else:
                WinningString = ""
                WinningCount = 0
            break

    # ----------------------------------------------------------------------------------------------------------------------------#
    return (WinningString, WinningCount)


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

def MakeStringFromAlternation(s1, s2, s3, s4):
    if s1 == "":
        s1 = "nil"
    if s2 == "NULL":
        s2 = "#"
    if s3 == "":
        s3 = "nil"
    if s4 == "NULL":
        s4 = "#"

    str = "{:4s} before {:5s}, and {:4s} before  {:5s}".format(s1, s2, s3, s4)
    return str

# ----------------------------------------------------------------------------------------------------------------------------#
