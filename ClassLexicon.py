import math
import sys
import enum
import operator
from printing_to_files import *
from signaturefunctions import *
from family import family

# This is just part of documentation:
# A signature is a tuple of strings (each an affix).
# Signatures is a map: its keys are signatures.  Its values are *sets* of stems.
# StemToWord is a map; its keys are stems.       Its values are *sets* of words.
# StemToSig  is a map; its keys are stems.       Its values are individual signatures.
# WordToSig  is a Map. its keys are words.       Its values are *lists* of signatures.
# StemCorpusCounts is a map. Its keys are words.   Its values are corpus counts of stems.
# SignatureStringsToStems is a dict: its keys are tuples of strings, and its values are dicts of stems.

def get_affix_count(x): return x.count("=")

def join(stem, affix, affix_type):
    if affix == "NULL" or not affix:
        return stem
    else:
        if affix_type == "suffix":
            return stem + affix
        else:
            return affix + stem
def join_with_separator(stem, affix, affix_type):
    if affix == "NULL" or not affix:
        return stem
    else:
        if affix_type == "suffix":
            return stem + "=" +  affix
        else:
            return affix + "=" + stem
class Affix_type(enum.Enum):
    prefix = 1
    suffix = 2

def splitsignature(signature, maxlength=80):
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

class family_collection:
    def __init__(self):
        self.m_families = dict() # key is signature_string and value is a family
    def nucleus_to_children(self, sigstring):
        return self.m_families[sigstring]   #this is a *list*
    def add_family(self, nucleus_sig):
        #nucleus_sig_list = nucleus_sig.get_affix_list()
        nucleus_sig_string = nucleus_sig.get_affix_string()
        new_family = family(nucleus_sig_string)
        self.m_families[nucleus_sig_string] = new_family
    def get_family(self, nucleus_string):
        return self.m_families[nucleus_string]
    def add_signature(self, signature):
        sigstring = signature.get_affix_string()
        for this_family in self.m_families:
            #print "  >>62," "checking each nucleus family: ", this_family
            if contains(sigstring, this_family):
                #print "  >>65 adding ",  sigstring, "to this family."
                self.m_families[this_family].add_signature(signature)
            else:
                pass
                #print "  >>68 does not contain."
        #print "  >>end of 'add_signature' "
    def print_families(self, this_file):
        for this_family in self.m_families:
            #print 63, this_family
            self.m_families[this_family].print_family(this_file)


class Buckle:
    """
    A Buckle is a pair of stems in which the first is a prefix of the second.
    """
    m_stem1 = ""
    m_stem2 = ""
    m_sigstring1 = ""
    m_sigstring2 = ""
    m_difference = ""
    m_affix_type = ""
    def __init__(self, stem1, stem2,sigstring1, sigstring2, affix_type):
       self.m_stem1 = stem1
       self.m_stem2 = stem2
       self.m_sigstring1 = sigstring1
       self.m_sigstring2 = sigstring2
       self.m_difference = stem2[len(stem1):]
       self.m_affix_type = affix_type


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
    def __init__(self,affix_side,signature_string):
        self.affix_side = affix_side
        self.affixes_list = signature_string_to_signature_list(signature_string)
        self.stem_counts = dict()
        #if stems:
        #    for stem in stems:
        #        self.stem_counts[stem] = 1
        self.affixes_count_dict = dict()
        self.robustness = 0
        self.robustness_clean = False
        self.affixes_list.sort()
        self.name = ""
        if self.affix_side != affix_side:
            return None

    def add_stem(self,stem, count = 1):
        if not self.stem_counts:
            self.stem_counts = dict()
        self.stem_counts[stem] = count
    def add_affix(self,affix):
        if affix in self.affixes_list:
            return
        self.affixes_list.append(affix)
    def get_affix_length(self):
        return len(self.affixes_list)
    def get_stems(self):
        return sorted(self.stem_counts.keys())
    def get_affix_list(self):
        return self.affixes_list
    def get_affix_string(self):
        #print 142, make_signature_string_from_signature_list(self.affixes_list)
        return make_signature_string_from_signature_list(self.affixes_list)
    def get_affix_count(self, affix):
        return len(self.affixes_dict[affix])
    def get_internal_robustness(self):
        if self.robustness_clean:
	    #print 145, self.robustness
            return self.robustness
        else:
            robustness = 0
            affixes_length = 0
            for affix in self.affixes_list:
                if affix == "NULL":
                    affixes_length += 1
                else:
                    affixes_length += len(affix)
            robustness += affixes_length * (len(self.stem_counts) - 1)
            stems_length = 0
            for stem in self.stem_counts:
                stems_length += len(stem)
            robustness += stems_length * (len(self.affixes_list) - 1)
            self.robustness = robustness
            self.robustness_clean = True
	    #print 162, self.robustness
            return robustness
## -------                                                      ------- #
##              Class Lexicon                                   ------- #
## -------                                                      ------- #
class CLexicon:
    def __init__(self):

        #static variable:
        reportnumber = 1
        self.Corpus = list()
        self.Families = family_collection()
        self.LongestWordLength = 0
        self.MinimumStemLength = 3
        self.MaximumStemLength = 100
        self.MaximumAffixLength = 15
        self.Parses = dict()
        self.Prefixes = {}
        self.Protostems= dict()
        self.PrefixToStem = dict()
        self.RawSignatures=dict(); # key is signature-string, and value is a string of stems. These signatures occur only once.
        self.RawSuffixes = dict(); #key is a raw suffix (just a continuaton) and value is a list of its protostems
        self.ReverseWordList = list()
        self.RemovedSignatureList = list()
        self.Signatures=dict() ; #key is string, value is a Signature object
        self.Signatures_containment = dict() # key is signature string, value is list of subsignature strings
        self.SignatureBiographies=dict()
        self.StemCorpusCounts = {}
        self.StemToSignature = {}  # value is a list of pairs of the form (stem, sig-string) where the sig-string is a string with "=" as separator.
        self.StemToWord = {}
        self.StemToAffix_dict = {}  # value is a Dict whose keys are affixes.
        self.Suffixes = {}
        self.SuffixToStem= dict()
        self.TotalRobustInSignatures = 0
        self.UnexplainedContinuations = {}
        self.UnlikelyStems = dict()
        self.WordToSig = dict()
        self.Word_list_forward_sort = list()
        self.Word_list_reverse_sort=list()
        self.Words_sort_clean_flag=False
        self.Word_counts_dict = dict()
        self.WordBiographies=dict()
        self.total_word_count = 0
        self.word_letter_count = 0
        self.total_letters_in_stems = 0
        self.total_letters_in_analyzed_words = 0
        self.total_affix_length_in_signatures = 0
        self.number_of_analyzed_words =  0


    def get_stems(self):
        return sorted(self.StemToSignature.keys())
    def get_number_of_stems():
        return len(self.StemToSignatures)



    ## -------                                                      ------- #
    ##              Central signature computation                   ------- #
    ## -------                                                      ------- #

    def accept_stem_and_signature(self, affix_side, stem, signature_string):
            if signature_string not in self.Signatures:

                this_signature = Signature(affix_side, signature_string)
                self.Signatures[signature_string] = this_signature
            else:
                this_signature = self.Signatures[signature_string]

            if stem not in self.StemToSignature:
                self.StemToSignature[stem] = list()
            self.StemToSignature[stem].append(signature_string)
            self.StemCorpusCounts[stem] = 0
            return this_signature

    # not currently used, probably get rid of.
    def clear_memory_of_analysis_except_parses_and_affixes(self):

        self.Prefixes = dict()
        self.PrefixToStem = dict()
        self.Signatures = dict()
        self.Signatures_containment = dict()
        self.StemCorpusCounts = dict()
        self.StemToSignature =  dict()
        self.StemToAffix =  dict()
        self.StemToWord = dict()
        self.Suffixes = dict()
        self.SuffixToStem = dict()
        self.WordToSig.clear()
        self.Word_list_forward_sort = list()
        self.Word_list_reverse_sort = list()
        self.Word_sort_clean_flag = False

        self.word_letter_count = 0
        self.number_of_analyzed_words = 0
        self.total_letters_in_analyzed_words = 0
        self.total_affix_length_in_signatures = 0
        self.total_letters_in_stems = 0
    def clear_parses(self):
        self.Parses.clear()

    def get_signatures_sorted_by_affix_count(self, affix_type):
        return sorted(self.Signatures.keys(), key = get_affix_count,reverse=True)

    def get_signatures_sorted_by_robustness(self):
	return sorted(self.Signatures.items(),key= lambda f: get_robustnessf[1], reverse=True)

    def sort_words(self):
        self.Word_list_forward_sort.sort()
        self.Word_list_reverse_sort.sort(key = lambda x: x[::-1])
        self.Word_sort_clean_flag = True

    def get_words_end_with(self,suffix):
        if not self.Words_sort_clean_flag:
            self.sort_words()
        start = -1
        end = -1
        for i in range(len(self.Word_list_reverse_sort)):
            if not self.Word_list_reverse_sort[i].endswith(suffix):
                continue
            start = i
            for j in range(i,len(self.Word_list_reverse_sort)):
                if not self.Word_list_reverse_sort[j].endswith(suffix):
                    end = j-1
                    return ((start,end))
        return (0,0)

    def get_words_start_with(self,prefix):
        if not self.Words_sort_clean_flag:
            self.sort_words()
        start = -1
        end = -1
        for i in range(len(self.Words)):
            if not self.Words[i].startswith(prefix):
                continue
            start = i
            for j in range(i,len(self.Words)):
                if not self.Words[j].startswith(prefix):
                    end = j-1
                    break
        return ((start,end))

    def find_signatures_containment(self, affix_type):
        for sig in self.get_signatures_sorted_by_affix_count(affix_type):
            siglist = MakeSignatureListFromSignatureString(sig)
            sig_length = get_affix_count(sig)
            for subsig in self.Signatures:
                if get_affix_count(subsig) >= sig_length:
                    #print 229, "***"
                    continue
                subsiglist = MakeSignatureListFromSignatureString(subsig)
                #if all(affix in siglist for affix in subsiglist):
                #    print 225, "\t" , sig, subsig
    def break_word_by_suffixes(self, word):
        current_left_edge = 0
        broken_word = ""
        for i in range(len(word)):
            if word[:i] in self.StemToWord:
                #print  ":",   word[:i],
                piece = word[current_left_edge:i]
                broken_word =  broken_word + " "+ piece
                current_left_edge = i
                #print >> outfile, piece,
        broken_word += " " + word[current_left_edge:]
        #print "\n", 249, word, broken_word
        return broken_word
    def find_nuclear_signatures(self):
        """
        A nuclear signature is one whose robustness is greater than that of
        any signature just above or just below it on the lattice.

        """

        #for sig in self.Signatures:



    # Delete this, no longer used.
    def PutSignaturesIntoLattice(self,thisSigLattice):
	i = 0
        for sig_string in self.Signatures.keys():
	    #print (167, i, sig_string)
 	    i=i+1
            sig_list = MakeSignatureListFromSignatureString(sig_string)
            thisSigLattice.deposit(sig_list)
	#thisSigLattice.lattice_print()

    # ----------------------------------------------------------------------------------------------------------------------------#
    def add_stem_to_raw_suffix(self, suffix, stem):
        if suffix not in self.RawSuffixes:
            self.RawSuffixes[suffix] = dict()
        self.RawSuffixes[suffix][stem] = 1
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

            if numberofstems < MinimumNumberOfStemsInSignaturesChAssignSignaturesToEachStem_crabeckedForRebalancing:
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
    def printSignatures(self,  encoding, affix_type, prefix = "", suffix = ""):
        if affix_type == "prefix":
            FindSuffixesFlag = True
        else:
            FindSuffixesFlag = False
        # NOTE! this needs to be updated to include Lexicon.Signatures
        # ----------------------------------------------------------------------------------------------------------------------------#
        suffix = "_" + suffix
        filename_txt = ["Log", "Signatures", "Signatures_2", "Signatures_svg_html", "Signatures_feeding",
                  "SignatureDetails", "WordToSig", "StemToWords","SigExtensions", "Suffixes",   "StemsAndUnanalyzedWords"]
        filenames_html = [  "Signatures_html", "Index", "WordToSig_html"]
        lxalogfile = open(self.outfolder + "Log", "w")


        outfile_signatures_1            = open(self.outfolder + prefix + "Signatures_iter"+ suffix+".txt", "w")
        outfile_signatures_svg_html     = open(self.outfolder + prefix + "Signatures_graphic_iter"+ suffix+".html", "w")
        outfile_signature_feeding       = open(self.outfolder + prefix + "Signature_feeding_iter"+ suffix+".html", "w")
        outfile_signatures_html         = open(self.outfolder + prefix + "Signatures_iter"+ suffix+".html", "w")
        outfile_index                   = open(self.outfolder + prefix + "Index_iter"+ suffix+".html", "w")
        outfile_words = open(self.outfolder + prefix + "Words"+ suffix + ".txt", "w")
        outfile_wordstosigs             = open(self.outfolder + prefix + "WordToSig_iter"+ suffix+".txt", "w")
        outfile_wordstosigs_html        = open(self.outfolder + prefix + "WordToSig_iter"+ suffix+".html", "w")
        outfile_stemtowords             = open(self.outfolder + prefix + "StemToWords_iter"+ suffix+".txt", "w")
        outfile_suffixes                = open(self.outfolder + prefix + "Suffixes_iter"+ suffix+".txt", "w")
        outfile_stems_and_unanalyzed_words = open(self.outfolder + prefix + "StemsAndUnanalyzedWords_iter"+ suffix+".txt", "w")
        outfile_parses = open (self.outfolder + prefix + "_parses" + suffix+ ".txt", "w")

        # 1  Create a list of signatures, sorted by number of stems in each. DisplayList is that list. Its 4-tuples   have the signature, the number of stems, and the signature's robustness, and a sample stem

        ColumnWidth = 35
        #stemcountcutoff = 1

        SortedListOfSignatures = sorted(self.Signatures.items(),
                                        key = lambda x: len(x[1].get_stems()),
                                        reverse=True)


        DisplayList = []
        totalrobustness = 0
        singleton_signatures = 0
        doubleton_signatures = 0

        for sig, signature in SortedListOfSignatures:
            stems = sorted(signature.get_stems())
            exemplar_stem = stems[0]
            stem_count = len(stems)
            robustness = get_robustness (sig,stems)
            DisplayList.append((sig, len(stems), robustness, exemplar_stem))
            if stem_count == 1:
                singleton_signatures += 1
            elif stem_count == 2:
                doubleton_signatures += 1
            totalrobustness += robustness

        DisplayList.sort()

        initialize_files(self, outfile_signatures_1, singleton_signatures, doubleton_signatures, DisplayList)
        initialize_files(self, lxalogfile, singleton_signatures, doubleton_signatures, DisplayList)
        initialize_files(self, "console", singleton_signatures, doubleton_signatures, DisplayList)

        # Print html index
        print_html_report(outfile_index, self, singleton_signatures,doubleton_signatures, DisplayList)

        # Print signatures sorted by robustness
        print_signature_list_1(outfile_signatures_1,
                               self,
                               DisplayList,
                               totalrobustness,
                               lxalogfile,
                               affix_type)

        # Print signatures to html file with svg
        print_signatures_to_svg (outfile_signatures_svg_html, DisplayList,self.Signatures,FindSuffixesFlag)

        # Print suffixes
        suffix_list = print_suffixes(outfile_suffixes, self.Suffixes, self.RawSuffixes)

        # Print stems
        print_stems(outfile_stemtowords, outfile_stems_and_unanalyzed_words, self,  suffix_list)

        # print the stems of each signature to html:
        print_signature_list_1_html(outfile_signatures_html, DisplayList, totalrobustness)

        # print signature feeding structures:
        print_signature_list_2(outfile_signature_feeding, lxalogfile, self, DisplayList, totalrobustness,  FindSuffixesFlag)

        # print WORDS of each signature:
        print_words(self, outfile_words, outfile_wordstosigs, outfile_wordstosigs_html, lxalogfile,   ColumnWidth)

        print_parses(outfile_parses, self)

        # print unlikely signatures:
        #print_unlikelysignatures(outfile_unlikelysignatures, self.UnlikelySignatureStringsToStems, ColumnWidth)

    ## -------  widen_scope_of_affixes                              ------- #
    def widen_scope_of_affixes(self, affix_type, minimum_stem_length=1):
        if affix_type == "suffix":
            for suffix in self.Suffixes:
                suffix_length = len(suffix)
                self.SuffixToStem[suffix] = dict()
                (first_word, last_word) = self.get_words_end_with (suffix)
                for i in range(first_word,last_word):
                    word = self.Word_list_reverse_sort[i]
                    stem_length = len(word) - suffix_length
                    if stem_length < minimum_stem_length:
                        continue
                    new_stem = word[:stem_length]
                    self.SuffixToStem[suffix][new_stem] = 1

        else:
            for prefix in self.Prefixes:
                prefix_length = len(prefix)
                self.PrefixToStem[prget_signatures_sorted_by_affix_countefix] = dict()
                (first_word, last_word) = self.get_words_start_with (prefix)
                for i in range(first_word,last_word):
                    word = Words[i]
                    stem_length = word.len() - prefix_length
                    if stem_length < minimum_stem_length:
                        continue
                    new_stem = self.Words[i][:stem_length]
                    self.PrefixToStem[prefix][new_stem] = 1
                    print 422, prefix, Word, new_stem



    ## -------                                                      ------- #
    ##              Utility functions                               ------- #
    ## -------                                                      ------- #
    def PrintWordCounts(self):
        outfile = open(self.outfolder + "WordCount.txt", "w")
        formatstring = "{:20s} {:6d}"
        self.sort_words()
        #words = self.Word_counts_dict.keys()
        #words.sort()
        for word in self.Word_list_forward_sort:
            print >> outfile, formatstring.format(word, self.Word_counts_dict[word])

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
            counts[affix] += self.Word_counts_dict[word]
            total += self.Word_counts_dict[word]
        frequency = dict()
        for affix in this_signature:
            frequency[affix] = counts[affix] / total
  # ----------------------------------------------------------------------------------------------------------------------------#



    # ----------------------------------------------------------------------------------------------------------------------------#
    def produce_lexicon_report(self):

        # remove this first part that uses member variables in Lexicon.
        reportlist = list()
        formatstring = "{0:20s}{1:20s}"
        reportlist.append ("Information from Lexicon")

        self.total_word_count = len(self.Word_counts_dict)
        self.word_letter_count = 0
        for word in self.Word_counts_dict:
            self.word_letter_count += len(word)
        self.number_of_analyzed_words =  len(self.WordToSig)
        self.total_letters_in_analyzed_words = 0
        for word in self.WordToSig:
            self.total_letters_in_analyzed_words += len(word)
        self.total_affix_length_in_signatures = 0
        self.total_letters_in_stems = 0
        for (sig, signature) in self.Signatures.items():
            for affix in splitsignature(sig):
                if affix == "NULL":
                    continue
                self.total_affix_length_in_signatures += len(affix)
            StemListLetterLength = 0
            for stem in signature.get_stems():
                self.total_letters_in_stems += len(stem)
            tempstemlength = 0

        word_letter_count = 0
        for word in self.Word_counts_dict:
            word_letter_count += len(word)
        total_letters_in_analyzed_words = 0
        for word in self.WordToSig:
            total_letters_in_analyzed_words += len(word)
        total_affix_length_in_signatures = 0
        total_stem_length_in_signatures = 0
        for (sig, signature) in self.Signatures.items():
            for affix in splitsignature(sig):
                if affix == "NULL":
                    continue
                total_affix_length_in_signatures += len(affix)
            StemListLetterLength = 0
            for stem in signature.get_stems():
                total_stem_length_in_signatures += len(stem)
            tempstemlength = 0

        reportlist.append("Total word count:" + str(len(self.Word_counts_dict)))
        reportlist.append("Total word letter count:" + str(word_letter_count))
        reportlist.append("Number of analyzed words:" +  str(len(self.WordToSig)))
        reportlist.append("Total analyzed word letter count:" + str(total_letters_in_analyzed_words))
        reportlist.append("total_affix_length_in_signatures:" + str(total_affix_length_in_signatures))
        reportlist.append("total_stem_length_in_signatures:" + str(total_affix_length_in_signatures))
        return reportlist

class Word:
    def __init__(self, key):
        self.Key = key
        self.leftindex = -1
        self.rightindex = -1



def byWordKey(word):
    return word.Key


class CSignature:
    count = 0

    def __init__(self, signature_string):
        self.Index = 0
        self.Affixes = tuple(signature_string.split("="))
        self.StartStateIndex = CSignature.count
        self.MiddleStateIndex = CSignature.count + 1
        self.EndStateIndex = CSignature.count + 2
        self.count += 3
        self.StemCount = 1
        self.LetterSize = len(signature_string) - len(self.Affixes)
        self.Stems = dict()  # key is stem and value is corpus count of the stem
        self.StemToWordCount = dict()  # key is stem and value is a dict;
            # key of that dict is an affix and value is corpus count of that stem+affix

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
        returnstring = "parseChunk: morph: "
        if len(self.morph) > 0:
            returnstring += self.morph
        else:
            returnstring += "NULL"
        if self.remainingString == "":
            returnstring += ", no remaining string",
        else:
            returnstring += "remaining string is " + self.remainingString
        if self.edge:
            return "-(" + str(self.fromState.index) + ")" + self.morph + "(" + str(
                self.toState.index) + ") -" + "remains:" + returnstring
        else:
            return returnstring + ". " + self.morph + "no edge on this parsechunk"


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
        returnstring = "["
        for i in range(len(self.my_chain)):
            chunk = self.my_chain[i]
            returnstring += chunk.morph + "-"
            if chunk.edge:
                returnstring += str(chunk.edge.toState.index) + "-"
        return returnstring + "]"


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
def get_robustness(sig, stems):
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
    #print sig, "count:", countofsig, "stem count: ", countofstems, "letters in stems:", lettersinstems, "letters in affixes", lettersinaffixes, "robustness: ", robustness
    #print "\n", stems
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
