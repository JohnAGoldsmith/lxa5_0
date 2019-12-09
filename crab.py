#import math
import sys

from printing_to_files import *
from signaturefunctions import *
from ClassLexicon import *
#from ClassLexicon import Signature
from SigLattice import *


    ## -------                                                      ------- #
    ##              Central signature computation                   ------- #
    ## -------                                                      ------- #

# ------------------------------------------------------------------------#
def MakeSignatures_Crab_1(Lexicon, affix_type, verboseflag = False):
# ------------------------------------------------------------------------#
        lxalogfile = open(Lexicon.outfolder + "lxalog.txt", "w")
        outfile_Rebalancing_Signatures = open(Lexicon.outfolder + "Rebalancing_Signatures.txt", "w")
        outfile_subsignatures = open(Lexicon.outfolder + "Subsignatures.txt", "w")
        MinimumStemLength = Lexicon.MinimumStemLength
        verboseflag = True
        formatstring1 = "  {:50s}{:>10,}"
        formatstring2 = "  {:50s}"
        if verboseflag:
            print formatstring2.format("The MakeSignatures function")

        Lexicon.NumberOfAnalyzedWords = 0
        Lexicon.LettersInAnalyzedWords = 0
        Lexicon.NumberOfUnanalyzedWords = 0
        Lexicon.LettersInUnanalyzedWords = 0
        Lexicon.TotalRobustnessInSignatures = 0
        Lexicon.TotalLetterCostOfAffixesInSignatures = 0
        Lexicon.TotalLetterCostOfAffixesInSignatures = 0

        if affix_type in ("suffixes", "suffix"):
            Affixes = Lexicon.Suffixes
            FindSuffixesFlag = True
        else:
            Affixes = Lexicon.Prefixes
            FindSuffixesFlag = False
        # 1 --------------------------------------------------------------------
        #Step = 1
        maximumstemlength = 100

        find_protostems_crab(Lexicon, affix_type, verboseflag)
        if verboseflag:
            print formatstring1.format("1. Finished finding proto-stems.", len(Lexicon.Protostems))

        # 2 --------------------------------------------------------------------
        #Step += 1
        create_stem_affix_pairs(Lexicon, affix_type, verboseflag)
        # 3 --------------------------------------------------------------------
        assign_affixes_to_each_stem_crab(Lexicon, affix_type, verboseflag)
        if verboseflag:
            print  "     Finished finding affixes for protostems."

        # 4 --------------------------------------------------------------------
        # Assign signatures to each stem.
        MinimumStemCountInSignature = 2
        assign_affixes_to_each_stem_crab(Lexicon, affix_type, verboseflag, MinimumStemCountInSignature)
        assign_signatures_to_each_stem_crab (Lexicon, affix_type, verboseflag,MinimumStemCountInSignature)

        if verboseflag:
            print  formatstring1.format("5. Finished first pass of finding stems, affixes, and signatures.",
                len(Lexicon.Signatures) )
        report = Lexicon.produce_lexicon_report()

# Crab Part 2
        #Report has not yet been printed -- print it now.
        #widen_scope_of_signatures(Lexicon, affix_type)




        #Lexicon.find_signatures_containment(affix_type)

# ------------------------------------------------------------------------#
def MakeSignatures_Crab_2(Lexicon, affix_type, prefix, suffix, verboseflag = False):
# ------------------------------------------------------------------------#

    replace_parse_pairs_from_current_signature_structure_crab(Lexicon,  affix_type )

    widen_scope_of_signatures(Lexicon, affix_type, Lexicon.MinimumStemLength)

    print   "6. Number of parses", len(Lexicon.Parses)

    assign_affixes_to_each_stem_crab(Lexicon,
                                    affix_type,
                                     verboseflag)

    MinimumStemCountInSignature = 1

    assign_signatures_to_each_stem_crab (Lexicon,
                                         affix_type,
                                         verboseflag,
                                         MinimumStemCountInSignature,
                                         prefix)

#-----------------------------------------------------------------------------#
#          Widen stems in sigantures: Crab2
#-----------------------------------------------------------------------------#
def widen_scope_of_signatures(Lexicon, affix_type, minimum_stem_length):
    """
    Find all stems that go with each affix.
    Sort signatures by number of affixes, in decreasing order.
    For each signature, find stems that satisfy all the affixes in
    a signature; but don't allow a stem to be in more than
    one such signature (the longest is the best)
    """
    Lexicon.widen_scope_of_affixes(affix_type, minimum_stem_length)
    signatures = Lexicon.get_signatures_sorted_by_affix_count(affix_type)
    stems_assigned_to_signatures = dict()
    if affix_type == "prefix":
            return

    thisfile = open("tempfile.txt", "w ")

    for sig in signatures:
        print >>thisfile, "\n", sig
        sig_list = sort_signature_string_by_length(sig)
        affix_1 = sig_list[0]
        stem_collection = dict(Lexicon.SuffixToStem[affix_1])
        for stem in stems_assigned_to_signatures:
            if stem in stem_collection:
                del stem_collection[stem]
        for i in range(1,len(sig)):
            for affix  in sig_list:
                new_stem_dict = dict()
                if affix == "NULL":
                    for stem in stem_collection:
                        if stem in Lexicon.Word_counts_dict:
                            new_stem_dict[stem] = 1
                    stem_collection = new_stem_dict
                else:
                    for stem in stem_collection:
                        if stem in Lexicon.SuffixToStem[affix]:
                            new_stem_dict[stem] = 1
                    stem_collection = new_stem_dict
        for stem in stem_collection:
                if stem in Lexicon.StemToSignature:
                    print >>thisfile,  "Old:", stem
                    pass
                else:
                    print >>thisfile,  "New:", stem
                    for affix in sig_list:
                        Lexicon.Parses[(stem, affix)] = 1
                        print >>thisfile,  stem, affix,
                    print >>thisfile
                    stems_assigned_to_signatures[stem] = 1
    print >>thisfile,  "Number of parses:", len(Lexicon.Parses)

    thisfile.close()





#-----------------------------------------------------------------------------#
def add_prefixal_stem_to_protostems1(Lexicon, contentlist,   verboseflag, previous_word, word, stem):
        formatstring1 = "{0:20s}{1:20s} {2:20s}{3:32s}"
        Lexicon.WordBiographies[word].append(" Found stem " + stem)
        if stem not in Lexicon.Protostems:
            Lexicon.Protostems[stem] = 1
            if verboseflag:
                reportline = formatstring1.format(previous_word, word, stem, "" )
                contentlist.append(reportline)
        else:
            if verboseflag:
                reportline = formatstring1.format(previous_word, word,   stem, "Known stem.")
                contentlist.append(reportline)
        Lexicon.Protostems[stem] += 1
#---------------------------------------------------------------------------------------------------------------------#
def add_suffixal_stem_to_protostems2(Lexicon,contentlist,  verboseflag, stem):
        formatstring1 = "{0:20s}  {1:20s}"
        if verboseflag:
            reportline = formatstring1.format(word,     "New stem.")
            contentlist.append(reportline)
        Lexicon.Protostems[stem] = 1
#---------------------------------------------------------------------------------------------------------------------#
def add_suffixal_stem_to_protostems1(Lexicon, contentlist, verboseflag,  word, stem):
    formatstring1 = "{0:20s} {1:20s}{2:32s}"
    Lexicon.WordBiographies[word].append(" Found stem " + stem)
    if stem not in Lexicon.Protostems:
             Lexicon.Protostems[stem] = 1
             if verboseflag:
                 reportline = formatstring1.format(word,  stem, "New stem.")
                 contentlist.append(reportline)
    else:
        if verboseflag:
            reportline = formatstring1.format(word, stem, "Known stem.")
            contentlist.append(reportline)
    Lexicon.Protostems[stem] += 1
#---------------------------------------------------------------------------------------------------------------------#

def find_protostems_crab(Lexicon, affix_type,verboseflag, maximum_stem_length=-1):
        formatstring1 = "{0:20s}{1:20s} {2:32s}"
        minimum_stem_length = Lexicon.MinimumStemLength
        if verboseflag:
            filename = "1_FindProtoStems.txt"
            headerlist = [ "Find proto-stems"]
            contentlist = list()

        previous_word = ""
        if affix_type == "suffix":
            for i in range(1,len(Lexicon.Word_list_forward_sort)):
                word = Lexicon.Word_list_forward_sort[i]
                for j in range(len(word)):
                    if ( j == len(previous_word) or
                        word[j] != previous_word[j]) :  # will a stem be found in the very first word?
                        if j < minimum_stem_length:
                            if verboseflag:
                                reportline = formatstring1.format(word,  "", "Too short.")
                                contentlist.append(reportline)
                            previous_word = word
                            continue
                        stem = word[:j]
                        add_suffixal_stem_to_protostems1(
                                    Lexicon,
                                    contentlist,
                                    verboseflag,
                                    word,
                                    stem)
                        previous_word = word
                        break
                previous_word = word
                continue
        else: #affix_type == "prefix"
            for i in range(1,len(Lexicon.Word_list_reverse_sort)):
                word = Lexicon.Word_list_reverse_sort[i]
                for j in range(1,len(word)):
                    if ( j == len(previous_word)+1 or
                        word[-1*j] != previous_word[-1*j]):
                        if j < minimum_stem_length + 2:
                            previous_word = word
                            continue
                        stem = word[-1*j+1:]
                        add_prefixal_stem_to_protostems1(
                                    Lexicon,
                                    contentlist,
                                    verboseflag,
                                    previous_word,
                                    word,
                                    stem)
                        previous_word = word
                        break
                previous_word = word
                continue


        if verboseflag:
            print_report(filename, headerlist, contentlist)


# ---------------------------------------------------------------------------#
def verbose_report_on_stem_affix_pairs(Lexicon,affix_type):
            filename = "3_parse_pairs.txt"
            headerlist = [ "List of parse pairs"]
            contentlist = list()
            linelist = list()
            formatstring = "{0:20s}   {1:20s} {2:10s} {3:20s}"
            templist=list()
            print_report(filename, headerlist, contentlist)
            affix =  ""
            for item in Lexicon.Parses:
                if affix_type == "suffix":
                    stem = item[0]
                    affix = item[1]
                    templist.append (stem +' ' + affix )
                    word = join(stem, affix, affix_type)
                    Lexicon.WordBiographies[word].append(" "+ stem + "=" + affix)
                else: # affix_type = "prefix"
                    affix = item[0]
                    stem= item[1]
                    templist.append (affix + ' ' + stem)
                    word = join(stem, affix, affix_type)
                    Lexicon.WordBiographies[word].append(" "+ affix +   "=" + stem)
            templist.sort()
            for item in templist:
                    contentlist.append(item)
            print_report(filename, headerlist, contentlist)
# ---------------------------------------------------------------------------#
def create_stem_affix_pairs(Lexicon,  affix_type, verboseflag):
        # This function creates the pairs in Parses. Most words have multiple appearances.
        # Step = 2.
        formatstring4 = "{0:15s} {1:15s} {2:10} {3:12}"
        if verboseflag:
            print "  2. Assign affixes and words to stems."
            filename = "2_All_initial_word_splits.txt"
            headerlist = [ "Assign affixes and words to stems"]
            contentlist = list()
            linelist = list()
            formatstring = "{0:20s}   {1:20s} {2:10s} {3:20s}"
        wordlist = deepcopy(Lexicon.Word_counts_dict.keys())
        wordlist.sort()
        column_no = 0
        NumberOfColumns = 8
        for i in range(len(wordlist)):
                if i % 5000 == 0:
                    if verboseflag == False:
                        print "{:7,d}".format(i),
                        sys.stdout.flush()
                        column_no += 1
                        if column_no % NumberOfColumns == 0:
                            column_no = 0
                            print "\n" + " " * 4,
                word = wordlist[i]
                WordAnalyzedFlag = False
                for i in range(len(word), Lexicon.MinimumStemLength - 1, -1):
                    if affix_type == "suffix":
                        stem = word[:i]
                    else:
                        stem = word[-1 * i:]
                    if stem in Lexicon.Protostems:
                        #---------------------------------------------------------------------------------------
                        # suffixing
                        if affix_type == "suffix":
                            suffix = word[i:]
                            if not suffix:
                                continue
                            Lexicon.Parses[(stem, suffix)] = 1
                            if stem in Lexicon.Word_counts_dict:
                                Lexicon.Parses[(stem, "NULL")] = 1
                            if len(suffix) <= Lexicon.MaximumAffixLength:
                                Lexicon.WordBiographies[word].append(" The split "+stem+ "=" + suffix + " is good.")
                                if verboseflag:
                                        reportline = formatstring.format(word,stem,suffix, " suffix is good.")
                                        contentlist.append(reportline)
                            if len(suffix) > Lexicon.MaximumAffixLength:
                                Lexicon.WordBiographies[word].append(" The split "+stem+ " / " + suffix + " is suspicious; suffix too long.")
                                if verboseflag:
                                    reportline = formatstring.format(word,stem,suffix, "suffix too long.")
                                    contentlist.append(reportline)
                            Lexicon.add_stem_to_raw_suffix(suffix,stem)
                        #-----------------------------------------------------------------------------------------
                        # prefixing
                        else: #affix_type = "prefix"
                            ii = len(word) - i
                            prefix = word[:ii]
                            if not prefix:
                                continue
       	                    Lexicon.Parses[(prefix,stem)] = 1
                            if stem in Lexicon.Word_counts_dict:
                                Lexicon.Parses[("NULL", stem)] = 1
                            if len(prefix) <= Lexicon.MaximumAffixLength:
                                Lexicon.WordBiographies[word].append(" The split "+prefix+ "=" + stem + " is good.")
                                if verboseflag:
                                        reportline = formatstring.format(word, prefix, stem,  "prefix is good.")
                                        contentlist.append(reportline)
                            if len(prefix) > Lexicon.MaximumAffixLength:
                                Lexicon.WordBiographies[word].append( " The split "+ prefix+ " / " + stem  + " is suspicious; affix too long.")
                                if verboseflag:
                                    reportline = formatstring.format(word,prefix, stem, "affix too long.")
                                    contentlist.append(reportline)

        if verboseflag:
                print_report(filename, headerlist, contentlist)

        #Step += 1
        if verboseflag:
            verbose_report_on_stem_affix_pairs(Lexicon, affix_type)
 # ----------------------------------------------------------------------------------------------------------------------------#
def verbose_helper_assign_affixes(Lexicon,filename,headerlist,contentlist):
    formatstring2 = "{0:15s} {1:15s}"
    stemlist = Lexicon.StemToWord.keys()
    stemlist.sort()
    for stem in stemlist:
        affixset = Lexicon.StemToAffix_dict[stem].keys()
        affixset.sort()
        reportline = formatstring2.format(stem, "=".join(affixset), len(affixset) )
        contentlist.append(reportline)
    print_report(filename, headerlist, contentlist)
 # ----------------------------------------------------------------------------------------------------------------------------#

def assign_affixes_to_each_stem_crab(Lexicon, affix_type, verboseflag, Step=-1):
        """ This assumes parse pairs in Lexicon.Parses, and  creates:
            Affixes
            StemToWord
            StemToAffix_dict
            SignatureStringsToStems
            StemToSignature
            StemCorpusCounts
            WordToSig """
        formatstring = "{0:20s}  {1:15s} {2:20s}{3:10s}"
        formatstring1 = "{0:32s}"

        Lexicon.StemCorpusCounts = dict()
        Lexicon.Affixes = dict()
        Lexicon.Signatures = dict()
        Lexicon.StemToSignature = dict()
        Lexicon.StemCorpusCounts = dict()
        Lexicon.StemToWord = dict()
        Lexicon.WordToSig = dict()
        Lexicon.StemToAffix_dict = dict()
        Lexicon.Suffixes = dict()
        formatstring2 = "{0:15s} {1:15s}"
        formatstring3 = "\n{0:15s} {1:15s} {2:10s} "
        formatstring4 = "\n{0:15s} {1:15s} {2:10s} {3:20s}"
        if verboseflag:
                filename = "4_protostems_and_their_affix_sets.txt"
                headerlist = [ "Link stems to the set of their affixes."]
                contentlist = list()
        if verboseflag:
            print "  4. Assign affix sets to each stem.\n     Find affixes for each protostem"

  # ----------------------- Collect each affix a stem has.
        ParseList = list()

        if affix_type == "suffix":
            Affixes = Lexicon.Suffixes
        else:
            Affixes = Lexicon.Prefix

        if affix_type == "suffix":
            for stem, affix in Lexicon.Parses:
                ParseList.append((stem,affix))
            ParseList.sort(key=lambda (x,y) : x+" "+y)
            for stem,affix in ParseList:
                if not affix:
                    affix = "NULL"
                if stem not in Lexicon.StemToWord:
                    Lexicon.StemToWord[stem] = dict()
                    Lexicon.StemToAffix_dict[stem] = dict()
                word = join(stem, affix, affix_type)
                Lexicon.StemToWord[stem][word] = 1
                Lexicon.StemToAffix_dict[stem][affix] = 1
                if affix not in Affixes:
                    Affixes[affix] = 0
                Affixes[affix] += 1
                Lexicon.WordBiographies[word].append(" This split:" + stem + "=" + affix)
            if verboseflag:
                verbose_helper_assign_affixes(Lexicon,filename,headerlist,contentlist)
        else:   #prefixes...
            for affix, stem  in Lexicon.Parses:
                ParseList.append((affix,stem))
            ParseList.sort(key=lambda (x,y) : x +" "+y)
            for affix, stem  in ParseList:
                if stem not in Lexicon.StemToWord:
                    Lexicon.StemToWord[stem] = dict()
                    Lexicon.StemToAffix_dict[stem] = dict()
                word = join(stem, affix, affix_type)
                Lexicon.StemToWord[stem][word] = 1
                Lexicon.StemToAffix_dict[stem][affix] = 1
                if affix not in Affixes:
                    Affixes[affix] = 0
                Affixes[affix] += 1
                Lexicon.WordBiographies[word].append( " This split:" + affix + "=" + stem )

            if verboseflag:
                verbose_helper_assign_affixes(Lexicon,filename,headerlist,contentlist)
 # ----------------------------------------------------------------------------------------------------------------------------#
def add_to_raw_signatures(Lexicon, affix_type, stem, signature_string, number_of_stems_this_sig, contentlist ):
    formatstring4 = "\n{0:15s} {1:15s} {2:10s} {3:20s}"
    if signature_string not in Lexicon.RawSignatures:
        Lexicon.RawSignatures[signature_string]= list()
    Lexicon.RawSignatures[signature_string].append(stem)
    reportline = formatstring4.format(stem, signature_string,"Too few stems",   str(number_of_stems_this_sig)  )
    contentlist.append(reportline)
    for affix in Lexicon.StemToAffix_dict[stem]:
        thisword = join(stem, affix, affix_type)
    Lexicon.WordBiographies[thisword].append("5. Too few stems in sig: " + signature_string)
    if signature_string not in Lexicon.SignatureBiographies:
        Lexicon.SignatureBiographies[signature_string] = list()
    Lexicon.SignatureBiographies[signature_string].append("5. This signature marked as raw: too few stems.")
    return contentlist
                        #print 523, stem

 # ----------------------------------------------------------------------------------------------------------------------------#

def assign_signatures_to_each_stem_crab(Lexicon, affix_type,verboseflag, MinimumStemCountInSignature, prefix=""):

        """ This assumes parse pairs in Lexicon.Parses, and  creates:
            Affixes
            StemToWord
            StemToAffix_dict
            SignatureStringsToStems
            StemToSignature
            StemCorpusCounts
            WordToSig """

        if affix_type == "suffix":
            Affixes = Lexicon.Suffixes
            AffixToStem = Lexicon.SuffixToStem
        else:
            Affixes = Lexicon.Prefixes
            AffixToStem = Lexicon.PrefixToStem

        Lexicon.StemCorpusCounts = dict()
        Lexicon.Affixes = dict()
        Lexicon.StemCorpusCounts = dict()
        formatstring2 = "{0:15s} {1:15s}"
        formatstring3 = "\n{0:15s} {1:15s} {2:10s} "
        formatstring4 = "\n{0:15s} {1:15s} {2:10s} {3:20s}"

        Lexicon.StemToSignature.clear()
        Lexicon.WordToSig.clear()
        Lexicon.StemToWord.clear()
        Lexicon.Suffixes.clear()
        Lexicon.Signatures.clear()
        Lexicon.RawSignatures.clear()

        if verboseflag:
                filename = "5_assigning_signatures.txt"
                headerlist = [ "5. Assign a single signature to each stem."]
                contentlist = list()
                formatstring  = "{0:20s}  {1:15s} {2:20s}{3:10s}"
                formatstring3 = "{0:20s}  {1:15s} {2:15s}"
                formatstring2 = "{0:20s}  {1:30s} "
                formatstring1 = "{0:20s}"

        stemlist = Lexicon.StemToAffix_dict.keys()
        stemlist.sort()
        temp_sig_dict = dict()
        if verboseflag:
                print "     Assign a signature to each stem (occasionally two)."
        for stem in stemlist:
                sig = sig_dict_to_string(Lexicon.StemToAffix_dict[stem])  #MakeSignatureStringFromAffixDict(Lexicon.StemToAffix[stem])
                if sig not in temp_sig_dict:
                        temp_sig_dict[sig] = 0
                temp_sig_dict[sig] += 1
        temp_sigs_with_too_few_stems = list()
        for sig in temp_sig_dict:
                if temp_sig_dict[sig] < MinimumStemCountInSignature:
                        temp_sigs_with_too_few_stems.append(sig)

        for stem in stemlist:
            signature_list = sig_dict_to_list(Lexicon.StemToAffix_dict[stem])
            signature_string = sig_list_to_sig_string(signature_list)
            number_of_stems_this_sig = temp_sig_dict[signature_string]
            if number_of_stems_this_sig < MinimumStemCountInSignature:
                contentlist = add_to_raw_signatures(Lexicon, affix_type, stem, signature_string, number_of_stems_this_sig, contentlist )
                continue

            reportline = formatstring4.format(stem, signature_string, "Enough stems in this signature", str(number_of_stems_this_sig) )
            contentlist.append(reportline)

            this_signature = Lexicon.accept_stem_and_signature(affix_type, stem, signature_string)

                # 2e. Update  Signature biography.
            if signature_string not in Lexicon.SignatureBiographies:
                    Lexicon.SignatureBiographies[signature_string] = list()
            Lexicon.SignatureBiographies[signature_string].append ("Created at first opportunity, in AssignSignaturesToEachStem.")

                # 2f. Establish the link between this stem and its words:

            for affix in signature_list:
                if affix not in Affixes:
                   Affixes[affix] = 0
                Affixes[affix] += 1
                if affix not in AffixToStem:
                    AffixToStem[affix] = dict()
                AffixToStem[affix][stem] = 1
                word = join(stem, affix, affix_type)
                if word not in Lexicon.WordToSig:
                    Lexicon.WordToSig[word] = list()
                Lexicon.WordToSig[word].append((stem,signature_string))
                if stem not in Lexicon.StemToWord:
                    Lexicon.StemToWord[stem] = dict()
                Lexicon.StemToWord[stem][word] = 1
                Lexicon.StemCorpusCounts[stem] += Lexicon.Word_counts_dict[word]
                Lexicon.WordBiographies[word].append(prefix + " In signature " + signature_string)

            this_signature.add_stem(stem)
            #this_signature.add_affix(deepcopy(Lexicon.StemToAffix[stem]))
            this_signature.add_affix(affix)

        temp_sig_dict.clear()
        if verboseflag:
            print "     End of assigning a signature to each stem."
            print_report(filename, headerlist, contentlist)

        if verboseflag:
                print_report(filename, headerlist, contentlist)

# ----------------------------------------------------------------------------------------------------------------------------#
def	replace_parse_pairs_from_current_signature_structure_crab(Lexicon, affix_type = "suffix"):
# ----------------------------------------------------------------------------------------------------------------------------#
# The Lexicon.Parse pairs are the basic pieces out of which the whole signature structure is built. So in order to
# redo the signature structure, we just make sure the parses are correct, then we clear the signature structure
# and rebuild it, which is easy to do.

    print "   774 Number of parses in lexicon:", len(Lexicon.Parses)
    Lexicon.Parses.clear()
    print "   775 Number of parses in lexicon:", len(Lexicon.Parses)
    for sig_string in Lexicon.Signatures:
        stems = Lexicon.Signatures[sig_string].get_stems()
        affixes = sig_string.split("=")
        for affix in affixes:
            if affix == "NULL":
                affix = ""
            if affix_type == "suffix":
                for affix in affixes:
                    for stem in stems:

                        if stem == "direct":
                            print 787, stem, affix
                        Lexicon.Parses[(stem,affix)]=1
            else:
                for affix in affixes:
                    for stem in stems:
                        Lexicon.Parses[(affix,stem)]=1
    print "   790   Number of parses in lexicon now:", len(Lexicon.Parses)



# ----------------------------------------------------------------------------------------------------------------------------#
def	compare_stems (Lexicon,affix_type):
# ----------------------------------------------------------------------------------------------------------------------------
    stems = Lexicon.get_stems()
    temp = dict()

    for stemno in range(len(stems)):
        stem1 = stems[stemno]
        sequence_count = 1
        j = stemno + 1
        while j < len(stems) and stems[j].startswith(stem1):
            stem2 = stems[j]
            sig1 = Lexicon.StemToSignature[stem1]
            sig2 = Lexicon.StemToSignature[stem2]
            buckle = Buckle(stem1, stem2, sig1, sig2, affix_type)
            j += 1
            diff = buckle.m_difference

            if diff not in temp:
                temp[diff] = list()
            temp[diff].append(buckle)

            if j == stemno + 1:
                sequence_count += 1

            else:
                sequence_count = 0



            #print 717, buckle.m_stem1, buckle.m_stem2, diff
    difflist = sorted(temp.keys(), key = lambda x:len(temp[x]))

    for diff in difflist:
        subdifflist = sorted(temp[diff], key = lambda x:x.m_sigstring2)
        subdifflist = sorted(temp[diff], key = lambda x:x.m_sigstring1)
        #print "\n", 646, diff
        # for item in subdifflist:
        # print 648,  item.m_sigstring1, item.m_sigstring2
# ----------------------------------------------------------------------------------------------------------------------------#


