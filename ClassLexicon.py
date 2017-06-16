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
##              Class Signature                                 ------- #
## -------                                                      ------- #

class Signature:
    def __init__(self,affixside="suffix",stems=None,affixes=None):
        self.type=affixside
        self.slots=list()
        self.slots.append(list())
        self.slots.append(list())
        self.name = "" 
        self.affix_side = affixside       
        if affixside == "suffix":
                if stems:
                    self.slot[0] = deepcopy(stems)
                else:
                    self.slot[0]= list()
                if affixes:
                    self.slot[1] = deepcopy(affixes)
                else:
                    self.slot[1] = list()
        if affixside == "prefix":
                if stems:
                    self.slot[1] = deepcopy(stems)
                else:
                    self.slot[1]= list()
                if affixes:
                    self.slot[0] = deepcopy(affixes)
                else:
                    self.slot[0] = list()
    def add_stem(self,stem):
        if self.affix_side == "suffix":
            self.slots[0].append(stem)
        else:
            self.slots[1].append(stem)
    def add_affix(self,affix):
        if self.affix_side == "suffix":
            self.slots[1].append(affix)
        else:
            self.slots[0].append(affix)

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
        self.Protostems= dict()
        self.WordToSig = {}
        self.StemToWord = {}
        self.StemToAffix = {}  # value is a Dict whose keys are affixes.
        self.StemToSignature = {}  # value is a list of pairs of the form (stem, sig-string) where the sig-string is a string with "=" as separator. This was changed June 2017 to allow more than one sig. 
        self.SignatureStringsToStems = {} 
        self.Signatures={} ; #key is string, value is a Signature object
        self.RawSignatures=dict(); # key is signature-string, and value is a string of stems. These signatures occur only once (or are bad for some other reason), and we want to find what's good inside them.
        self.UnexplainedContinuations = {}
        self.RemovedSignatureList = list()
        self.UnlikelyStems = {}
        self.StemCorpusCounts = {}
        self.Suffixes = {}
        self.PossibleSuffixes={}
        self.Prefixes = {}
        self.WordBiographies=dict()
        self.SignatureBiographies=dict()
        #self.MinimumStemsInSignature = 2
        #self.MinimumAffixesInaSignature = 2
        self.MinimumStemLength = 2
        self.MaximumAffixLength = 5

        self.TotalRobustInSignatures = 0

        self.total_word_count = 0
        self.word_letter_count = 0
        self.total_letters_in_stems = 0
        self.total_letters_in_analyzed_words = 0
        self.total_affix_length_in_signatures = 0
        self.number_of_analyzed_words =  0

    ## -------                                                      ------- #
    ##              Central signature computation                   ------- #
    ## -------                                                      ------- #

    # ----------------------------------------------------------------------------------------------------------------------------#  ------------------------------------------------------------------------------------------------------#
 

 



    # ----------------------------------------------------------------------------------------------------------------------------#
    def RebalanceSignatureBreaks(self, threshold, outfile, FindSuffixesFlag,verboseflag = True):
        # this version is much faster, and does not recheck each signature; it only changes stems.
        # NOTE! This needs to be updated to utilize CLexicon.Signatures 
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
                                del self.Parses[(stem, affix_t)]
                                newaffix = shiftingchunk + affix_t
                                self.Parses[(newstem, newaffix)] = 1
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
    def printSignatures(self,  encoding, FindSuffixesFlag, suffix = ""): 
 
        # NOTE! this needs to be updated to include Lexicon.Signatures
        # ----------------------------------------------------------------------------------------------------------------------------#
        suffix = "_" + suffix
        filename_txt = ["Log", "Signatures", "Signatures_2", "Signatures_svg_html", "Signatures_feeding", 
                  "SignatureDetails", "WordToSig", "StemToWords","SigExtensions", "Suffixes",   "StemsAndUnanalyzedWords"]
        filenames_html = [  "Signatures_html", "Index", "WordToSig_html"] 
        lxalogfile = open(self.outfolder + "Log", "w")

        
        outfile_signatures_1            = open(self.outfolder + "Signatures"+ suffix+".txt", "w")
        outfile_signatures_2            = open(self.outfolder + "Signatures_"+ suffix+"2.txt", "w")  
        outfile_signatures_svg_html     = open(self.outfolder + "Signatures_graphic"+ suffix+".html", "w") 
        outfile_signature_feeding       = open(self.outfolder + "Signature_feeding"+ suffix+".html", "w")  
        outfile_signatures_html         = open(self.outfolder + "Signatures"+ suffix+".html", "w")  
        outfile_signatures_details      = open(self.outfolder + "Signature_Details"+ suffix+".txt", "w")  
        outfile_index                   = open(self.outfolder + "Index"+ suffix+".html", "w")   

        outfile_wordstosigs             = open(self.outfolder + "WordToSig"+ suffix+".txt", "w")
        outfile_wordstosigs_html        = open(self.outfolder + "WordToSig"+ suffix+".html", "w")
        outfile_stemtowords             = open(self.outfolder + "StemToWords"+ suffix+".txt", "w")
        outfile_SigExtensions           = open(self.outfolder + "SigExtensions"+ suffix+".txt", "w")
        outfile_suffixes                = open(self.outfolder + "Suffixes"+ suffix+".txt", "w")
        outfile_stems_and_unanalyzed_words = open(self.outfolder + "StemsAndUnanalyzedWords"+ suffix+".txt", "w") 

        # 1  Create a list of signatures, sorted by number of stems in each. DisplayList is that list. Its 4-tuples   have the signature, the number of stems, and the signature's robustness, and a sample stem

        ColumnWidth = 35
        stemcountcutoff = 1
        SortedListOfSignatures = sorted(self.SignatureStringsToStems.items(), lambda x, y: cmp(len(x[1]), len(y[1])),
                                        reverse=True)

        DisplayList = []
        for sig, stems in SortedListOfSignatures:
            if len(stems) < stemcountcutoff:
                continue;
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

        initialize_files(self, outfile_signatures_1, singleton_signatures, doubleton_signatures, DisplayList)
        initialize_files(self, lxalogfile, singleton_signatures, doubleton_signatures, DisplayList)
        initialize_files(self, "console", singleton_signatures, doubleton_signatures, DisplayList)

        if False:
            for sig, stemcount, robustness in DisplayList:
                if len(self.SignatureStringsToStems[sig]) > 5:
                    self.Multinomial(sig, FindSuffixesFlag)
        # Print html index
        print_html_report(outfile_index, self, singleton_signatures,doubleton_signatures, DisplayList)

        # Print signatures (not their stems) sorted by robustness
        print_signature_list_1(outfile_signatures_1, DisplayList, stemcountcutoff, totalrobustness)
        
        # Print signatures to html file with svg
        print_signatures_to_svg (outfile_signatures_svg_html, DisplayList,self.SignatureStringsToStems,FindSuffixesFlag)

        # Print suffixes
        suffix_list = print_suffixes(outfile_suffixes, self.Suffixes)

        # Print stems
        print_stems(outfile_stemtowords, outfile_stems_and_unanalyzed_words, self,  suffix_list)

        # print the stems of each signature to html:
        print_signature_list_1_html(outfile_signatures_html, DisplayList, stemcountcutoff, totalrobustness)

        # print the stems of each signature:
        print_signature_list_2(outfile_signatures_2, outfile_signature_feeding, lxalogfile, self, DisplayList, stemcountcutoff,  totalrobustness, self.SignatureStringsToStems, self.StemCorpusCounts,  FindSuffixesFlag)

        # print WORDS of each signature:
        print_words(outfile_wordstosigs, outfile_wordstosigs_html, lxalogfile, self.Words, self.WordToSig, ColumnWidth)

        # print unlikely signatures:
        #print_unlikelysignatures(outfile_unlikelysignatures, self.UnlikelySignatureStringsToStems, ColumnWidth)

    
        # print signature extensions:

    # print_signature_extensions(outfile_SigExtensions, lxalogfile, DisplayList, self.SignatureStringsToStems)

 
 





    ## -------                                                      ------- #
    ##              Utility functions                               ------- #
    ## -------                                                      ------- #
    def PrintWordCounts(self):
        outfile = open(self.outfolder + "WordCount.txt", "w")
        formatstring = "{:20s} {:6d}"
        words = self.WordCounts.keys()
        words.sort()
        for word in words:
            print >> outfile, formatstring.format(word, self.WordCounts[word])

    def Multinomial(self, this_signature, FindSuffixesFlag):
        counts = dict()
        total = 0.0
        for affix in this_signature:
            counts[affix] = 0
            for stem in self.SignatureStringsToStems[this_signature]:
                if affix == "NULL":
                    word = stem
                elif FindSuffixesFlag:
                    word = stem + affix
                else:
                    word = affix + stem
            counts[affix] += self.WordCounts[word]
            total += self.WordCounts[word]
        frequency = dict()
        for affix in this_signature:
            frequency[affix] = counts[affix] / total
  # ----------------------------------------------------------------------------------------------------------------------------#



    # ----------------------------------------------------------------------------------------------------------------------------#
    def Compute_Lexicon_Size(self):
        reportlist = list()
        formatstring = "{0:20s}{1:20s}"
        reportlist.append ("Information from Lexicon")


        self.total_word_count = len(self.WordCounts)

        self.word_letter_count = 0
        for word in self.WordCounts:
            self.word_letter_count += len(word)

        self.number_of_analyzed_words =  len(self.WordToSig)


        self.total_letters_in_analyzed_words = 0
        for word in self.WordToSig:
            self.total_letters_in_analyzed_words += len(word)

        self.total_affix_length_in_signatures = 0
        self.total_letters_in_stems = 0


        for sig in self.SignatureStringsToStems:

            for affix in sig:
                if affix == "NULL":
                    continue
                self.total_affix_length_in_signatures += len(affix)
            StemListLetterLength = 0
            for stem in self.SignatureStringsToStems[sig]:
                self.total_letters_in_stems += len(stem)

            tempstemlength = 0

        return reportlist

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
    sig_string_list = sig.split("=")
    countofsig = len(sig_string_list)
    countofstems = len(stems)
    lettersinstems = 0
    lettersinaffixes = 0
    for stem in stems:
        lettersinstems += len(stem)
    for affix in sig_string_list:
	if affix == "NULL":
	  thislength = 1
	else: thislength = len(affix)
        lettersinaffixes += thislength
    robustness = lettersinstems * (countofsig - 1) + lettersinaffixes * (countofstems - 1) 
    print sig, "count:", countofsig, "stem count: ", countofstems, "letters in stems:", lettersinstems, "letters in affixes", lettersinaffixes, "robustness: ", robustness
    print "\n", stems
    # ----------------------------------------------------------------------------------------------------------------------------#
    return robustness


# ----------------------------------------------------------------------------------------------------------------------------#

# The following function is not used, and does the same as the one above. Delete it.
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
