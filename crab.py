#import math
import sys

from printing_to_files import *
from signaturefunctions import *
from class_lexicon import *
from class_morphemetosignature import *
from crab3_splitmorphemes import Words_with_multiple_analyses_high_entropy
from crab3_splitmorphemes import Words_with_multiple_analyses_low_entropy
from crab3_splitmorphemes import Words_with_multiple_analyses
#from ClassLexicon import Signature
from SigLattice import *
import stringfunctions as Strfn
from collections import defaultdict

formatstring1 = "  {:50s}{:>10,}"
formatstring2 = "  {:50s}"
formatstring3 = "{0:20s} {1:20s} {2:20s} {3:32s}"
formatstring4 = "{0:20s} {1:20s}"
formatstring5 = "{0:20s} {1:20s} {2:32s}"
formatstring6 = "{0:20s} {1:20s} {2:10s}"
formatstring7 = "{0:15s} {1:15s}"
formatstring8 = "\n{0:15s} {1:15s} {2:10s} {3:20s}"
 



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
        create_stem_affix_pairs(Lexicon, affix_type, verboseflag)

        # 3 --------------------------------------------------------------------
        assign_affixes_to_each_stem_crab(Lexicon, affix_type, verboseflag, "crab1")
        # 3 --------------------------------------------------------------------
        if verboseflag:
            print formatstring2.format("   Finished finding affixes for protostems.")

        # 4 --------------------------------------------------------------------
        # Assign signatures to each stem.
        # 4 --------------------------------------------------------------------

        MinimumStemCountInSignature = 2
        assign_signatures_to_each_stem_crab (Lexicon, affix_type, verboseflag,MinimumStemCountInSignature, "crab1")
        Lexicon.Families.create_families(Lexicon)

	generate_shadow_signatures(Lexicon)

        report = Lexicon.produce_lexicon_report()
        
 
    	 
 
# ------------------------------------------------------------------------#
def MakeSignatures_Crab_2(Lexicon, affix_type, verboseflag = False):
# ------------------------------------------------------------------------#
    replace_parse_pairs_from_current_signature_structure_crab(Lexicon,  affix_type )
    widen_scope_of_signatures(Lexicon, affix_type, Lexicon.MinimumStemLength)
    assign_affixes_to_each_stem_crab(Lexicon, affix_type, verboseflag)
    MinimumStemCountInSignature = 1  # important! 
    assign_signatures_to_each_stem_crab (Lexicon, affix_type, verboseflag,MinimumStemCountInSignature, "crab2")
    Lexicon.Families.create_families(Lexicon)

# ------------------------------------------------------------------------#
def MakeSignatures_Crab_3(Lexicon, affix_type, verboseflag = False):
# ------------------------------------------------------------------------#

    Words_with_multiple_analyses (Lexicon, affix_type)
    Words_with_multiple_analyses_high_entropy (Lexicon, affix_type)
    assign_affixes_to_each_stem_crab(Lexicon, affix_type, verboseflag)
    MinimumStemCountInSignature = 1  #  May 6, 2021 JG I had it at 2, that might have caused a bug by which many analyses from WidenSigs were being ignored.  
    assign_signatures_to_each_stem_crab (Lexicon, affix_type, verboseflag,MinimumStemCountInSignature, "crab3a")
    Lexicon.Families.create_families(Lexicon)
        
    if False: 

		replace_parse_pairs_from_current_signature_structure_crab(Lexicon,  affix_type )
		Words_with_multiple_analyses_low_entropy (Lexicon, affix_type)
		MinimumStemCountInSignature = 2  #   
		assign_signatures_to_each_stem_crab (Lexicon, affix_type, verboseflag,MinimumStemCountInSignature, "crab3b")


# ------------------------------------------------------------------------#
def MakeSignatures_Crab_4(Lexicon, affix_type, verboseflag = False):
# ------------------------------------------------------------------------#
    """
    Complex signatures are composed of pairs of signatures whose
    stems differ in length by only one letter. Typically because
    two or more affixes begin with the same letter.
    """
    Find_complex_signatures(Lexicon, affix_type)
#-----------------------------------------------------------------------------#
#          Widen stems in signatures: Crab2
#-----------------------------------------------------------------------------#

#sig1
#stem continues all suffixes in sig1
#family sig1 and satellite affixes a1 a2
#family contains sig1 + a1  AND sig + a2 BUT not sig1 + a1 + as2
#sig1 + a1  OR sig + a2 but not BOTH

#sig1  + a1 + a2



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
    thisfile = open("widensigs.txt", "w ")
    if affix_type == "suffix":
	affixes_to_stem = Lexicon.SuffixToStem
    else:
	affixes_to_stem = Lexicon.PrefixToStem
    
    for sig in signatures:
        print >>thisfile, "\n", sig[0]
        if sig[1].get_internal_robustness() < Lexicon.MinimumRobustness:
            print >>thisfile, "\n Robustness too low: ", sig[1].get_internal_robustness()
        sig_list = sort_signature_string_by_length(sig[0])
        affix_1 = sig_list[0]

	    # May 12 2021: changed the following line, so that several different signatures can leave their imprint on a given stem: the new signature may be a combination of previous signatures
        stem_collection = [stem  for stem in affixes_to_stem[affix_1] if stem not in stems_assigned_to_signatures]
        #stem_collection = [stem  for stem in affixes_to_stem[affix_1]]

        for i in range(1,len(sig)):
            for affix  in sig_list:
                if affix == "NULL":
                    stem_collection = [stem for stem in stem_collection if stem in Lexicon.Word_counts_dict]
                else:
                    stem_collection = [stem for stem in stem_collection if stem in affixes_to_stem[affix]]
        stem_collection.sort()
        for stem in stem_collection:
                if stem in Lexicon.StemToSignature:
                    pass
                else:
                    print >>thisfile, sig[0], "New stem:", stem
                    for affix in sig_list:
                        if affix_type == "suffix":
                            Lexicon.Parses[(stem, affix)] = 1
                            print >>thisfile, stem, affix
                        else:
                            Lexicon.Parses[(affix, stem)] = 1
                            print >>thisfile,  affix, stem
                    print >>thisfile
                    #this following line is not necessary, if we allow (as we do) stems to hook up with 2 or more signatures in this widening.
                    stems_assigned_to_signatures[stem] = 1
                    
   
    print >>thisfile,  "Number of parses:", len(Lexicon.Parses)
    thisfile.close()

#-----------------------------------------------------------------------------#
def add_prefixal_stem_to_protostems1(Lexicon, contentlist,   verboseflag, previous_word, word, stem):
        Lexicon.WordBiographies[word].append(" Found stem " + stem)
        if stem not in Lexicon.Protostems:
            Lexicon.Protostems[stem] = 1
            if verboseflag:
                reportline = formatstring3.format(previous_word, word, stem, "" )
                contentlist.append(reportline)
        else:
            if verboseflag:
                reportline = formatstring3.format(previous_word, word,   stem, "Known stem.")
                contentlist.append(reportline)
        Lexicon.Protostems[stem] += 1
#---------------------------------------------------------------------------------------------------------------------#
def add_suffixal_stem_to_protostems2(Lexicon,contentlist,  verboseflag, stem):
        if verboseflag:
            reportline = formatstring4.format(word, "New stem.")
            contentlist.append(reportline)
        Lexicon.Protostems[stem] = 1
#---------------------------------------------------------------------------------------------------------------------#
def add_suffixal_stem_to_protostems1(Lexicon, contentlist, verboseflag,  word, stem):
    Lexicon.WordBiographies[word].append("Found stem " + stem)
    if stem not in Lexicon.Protostems:
             Lexicon.Protostems[stem] = 1
             if verboseflag:
                 reportline = formatstring5.format(word,  stem, "New stem.")
                 contentlist.append(reportline)
    else:
        if verboseflag:
            reportline = formatstring5.format(word, stem, "Known stem.")
            contentlist.append(reportline)
    Lexicon.Protostems[stem] += 1
#---------------------------------------------------------------------------------------------------------------------#

def find_protostems_crab(Lexicon, affix_type,verboseflag, maximum_stem_length=-1):

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
                                reportline = formatstring5.format(word,  "", "Too short.")
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
            templist=list()
            print_report(filename, headerlist, contentlist)
            affix =  ""
            for item in Lexicon.Parses:
                if affix_type == "suffix":
                    stem = item[0]
                    affix = item[1]
                    templist.append (stem +' ' + affix )
                    word = Strfn.clean_join(stem, affix, affix_type)
                    Lexicon.WordBiographies[word].append(" "+ stem + "=" + affix)
                else: # affix_type = "prefix"
                    affix = item[0]
                    stem= item[1]
                    templist.append (affix + ' ' + stem)
                    word = Strfn.clean_join(stem, affix, affix_type)
                    Lexicon.WordBiographies[word].append(" "+ affix +   "=" + stem)
            templist.sort()
            for item in templist:
                    contentlist.append(item)
            print_report(filename, headerlist, contentlist)
# ---------------------------------------------------------------------------#
def create_stem_affix_pairs(Lexicon,  affix_type, verboseflag):
        # This function creates the pairs in Parses. Most words have multiple appearances.
        # Step = 2.
        if verboseflag:
            print "  2. Assign affixes and words to stems."
            filename = "2_All_initial_word_splits.txt"
            headerlist = [ "Assign affixes and words to stems"]
            contentlist = list()
            linelist = list()
        wordlist = deepcopy(Lexicon.Word_counts_dict.keys())
        wordlist.sort()
        column_no = 0
        NumberOfColumns = 8
        for i in range(len(wordlist)):
                word = wordlist[i]
                WordAnalyzedFlag = False
                for i in range(len(word), Lexicon.MinimumStemLength - 1, -1):
                    if affix_type == "suffix":
                        stem = word[:i]
                    else:
                        stem = word[-1 * i:]
                    if stem in Lexicon.Protostems:
                        #---------------------------------------------------------------------------------------
                        if affix_type == "suffix":
                            affix = word[i:]
                            if not affix:
                                continue
                            #added May 2021; why wasn't this there before?
                            if len(affix) > Lexicon.MaximumAffixLength:
                                continue
                            Lexicon.Parses[(stem, affix)] = 1
                            if stem in Lexicon.Word_counts_dict:
                                Lexicon.Parses[(stem, "NULL")] = 1
                            result = stem + "=" + affix 
                            Lexicon.add_stem_to_raw_suffix(affix,stem)
                        else:
                            ii = len(word) - i
                            affix = word[:ii]
                            if not affix:
                                continue
                            #added May 2021
                            if len(affix) > Lexicon.MaximumAffixLength:
                                continue
       	                    Lexicon.Parses[(affix,stem)] = 1
                            if stem in Lexicon.Word_counts_dict:
                                Lexicon.Parses[("NULL", stem)] = 1
			    result = affix + "=" + stem
                        #---------------------------------------------------------------------------------------
                        if len(affix) <= Lexicon.MaximumAffixLength:
                            Lexicon.WordBiographies[word].append(" The split " + result + " is good.")
                            if verboseflag:
                                reportline = formatstring6.format(word, result , "is good.")
                                contentlist.append(reportline)
                        #if len(affix) > Lexicon.MaximumAffixLength:
                        #    Lexicon.WordBiographies[word].append(" The split " + result + " is suspicious; affix too long.")
                        #    if verboseflag:
                        #        reportline = formatstring6.format(word, result,  "affix is too long.")
                        #        contentlist.append(reportline)
                         #-----------------------------------------------------------------------------------------
        if verboseflag:
                print_report(filename, headerlist, contentlist)
        if verboseflag:
            verbose_report_on_stem_affix_pairs(Lexicon, affix_type)
 # ----------------------------------------------------------------------------------------------------------------------------#
def verbose_helper_assign_affixes(Lexicon,filename,headerlist,contentlist):

    stemlist = Lexicon.StemToWord.keys()
    stemlist.sort()
    for stem in stemlist:
        affixset = Lexicon.StemToAffix_dict[stem].keys()
        affixset.sort()
        reportline = formatstring7.format(stem, "=".join(affixset), len(affixset) )
        contentlist.append(reportline)
    print_report(filename, headerlist, contentlist)
 # ----------------------------------------------------------------------------------------------------------------------------#

def assign_affixes_to_each_stem_crab(Lexicon, affix_type, verboseflag, label=""):
        """ This assumes parse pairs in Lexicon.Parses, and  creates:
            Affixes
            StemToWord
            StemToAffix_dict
            SignatureStringsToStems
            StemToSignature
            StemCorpusCounts
            WordToSig """

        MINIMUM_AFFIXES_IN_SIGNATURE = 2

        Lexicon.StemCorpusCounts = dict()
        
        Lexicon.Signatures = dict()
        Lexicon.StemToSignature = dict()
        Lexicon.StemCorpusCounts = dict()
        Lexicon.StemToWord = dict()
        Lexicon.WordToSig = dict()
        Lexicon.StemToAffix_dict = dict()
        Lexicon.Suffixes = dict()
        if verboseflag:
                filename = "4_protostems_and_their_affix_sets.txt"
                headerlist = [ "Link stems to the set of their affixes."]
                contentlist = list()
        if verboseflag:
            print "  4. Assign affix sets to each stem.\n     Find affixes for each protostem"
        ParseList = list()

        if affix_type == "suffix":
            Affixes = Lexicon.Suffixes
        else:
            Affixes = Lexicon.Prefix
        ParseList = list(Lexicon.Parses.keys())
        ParseList.sort(key=lambda (x,y) : x +" "+y)

        for x,y in ParseList:
            if affix_type == "suffix":
                stem = x
                affix = y
            else:
                affix = x
                stem = y
            if stem not in Lexicon.StemToWord:
                    Lexicon.StemToWord[stem] = dict()
                    Lexicon.StemToAffix_dict[stem] = dict()
                    Lexicon.StemCorpusCounts[stem] = 0
            word = Strfn.clean_join(stem, affix, affix_type)
            word2 = Strfn.join_with_separator (stem, affix, affix_type)
            Lexicon.StemToWord[stem][word] = 1
            Lexicon.StemToAffix_dict[stem][affix] = 1
            if word in Lexicon.Word_counts_dict:  
                Lexicon.StemCorpusCounts[stem] += Lexicon.Word_counts_dict[word] 
            if affix not in Affixes:
                    Affixes[affix] = 0
            Affixes[affix] += 1
            if word not in Lexicon.WordBiographies:
                Lexicon.WordBiographies[word] = list()
            Lexicon.WordBiographies[word].append(label + "   affix to stem:" + word2 + " (tentative)")  
        # Remove a stem if it has only one affix
        badstems = list()
        for stem in Lexicon.StemToAffix_dict:
            if len(Lexicon.StemToAffix_dict[stem]) < MINIMUM_AFFIXES_IN_SIGNATURE:
                badstems.append(stem)
                for word in Lexicon.StemToWord[stem]:
                    Lexicon.WordBiographies[word].append("Analysis dropped because only one affix found for stem.")
                del Lexicon.StemCorpusCounts[stem]
                del Lexicon.StemToWord[stem]
        for stem in badstems:
            del Lexicon.StemToAffix_dict[stem]
        if verboseflag:
            verbose_helper_assign_affixes(Lexicon,filename,headerlist,contentlist)
 # ----------------------------------------------------------------------------------------------------------------------------#
def add_to_raw_signatures(Lexicon, affix_type, stem, signature_string, number_of_stems_this_sig, contentlist ):
    if signature_string not in Lexicon.RawSignatures:
        Lexicon.RawSignatures[signature_string]= list()
    Lexicon.RawSignatures[signature_string].append(stem)
    reportline = formatstring8.format(stem, signature_string,"Too few stems",   str(number_of_stems_this_sig)  )
    contentlist.append(reportline)
    for affix in Lexicon.StemToAffix_dict[stem]:
        thisword = Strfn.clean_join(stem, affix, affix_type)
        Lexicon.WordBiographies[thisword].append("5. Too few stems in sig: " + " (" + stem + ") " + signature_string)
    if signature_string not in Lexicon.SignatureBiographies:
        Lexicon.SignatureBiographies[signature_string] = list()
    Lexicon.SignatureBiographies[signature_string].append("5. This signature marked as raw: too few stems.")
    return contentlist
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
            Lexicon.Suffixes = defaultdict(int)
            Affixes = Lexicon.Suffixes
            AffixToStem = Lexicon.SuffixToStem
        else:
            Lexicon.Prefixes = defaultdict(int)
            Affixes = Lexicon.Prefixes
            AffixToStem = Lexicon.PrefixToStem

        Lexicon.StemCorpusCounts = dict()
        Lexicon.StemCorpusCounts = dict()

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
 
        stemlist = Lexicon.StemToAffix_dict.keys()
        stemlist.sort()
        temp_sig_dict = defaultdict(int)
        # New May 2021
        temp_sig_robustness_dict = defaultdict(int)
        if verboseflag:
                print "     Assign a signature to each stem (occasionally two)."
        for stem in stemlist:
                sig = sig_dict_to_string(Lexicon.StemToAffix_dict[stem]) 
                temp_sig_dict[sig] += 1
                # New May 2021
                temp_sig_robustness_dict[sig] += len(stem) * (NumberOfAffixesInSigString(sig) - 1) 
        temp_sigs_with_too_few_stems = [sig for sig in temp_sig_dict.keys() if temp_sig_dict[sig] < MinimumStemCountInSignature]

        for stem in stemlist:
            signature_list = sig_dict_to_list(Lexicon.StemToAffix_dict[stem])
            signature_string = sig_list_to_sig_string(signature_list)
            number_of_stems_this_sig = temp_sig_dict[signature_string]
            if signature_string in temp_sigs_with_too_few_stems:
                contentlist = add_to_raw_signatures(Lexicon, affix_type, stem, signature_string, number_of_stems_this_sig, contentlist )
                continue
            reportline = formatstring8.format(stem, signature_string, "Enough stems in this signature", str(number_of_stems_this_sig) )
            contentlist.append(reportline)
            this_signature = Lexicon.accept_stem_and_signature(affix_type, stem, signature_string)
            # 2e. Update  Signature biography.
            if signature_string not in Lexicon.SignatureBiographies:
                    Lexicon.SignatureBiographies[signature_string] = list()
            Lexicon.SignatureBiographies[signature_string].append ("Created at first opportunity, in AssignSignaturesToEachStem.")

            # 2f. Establish the link between this stem and its words:

            Lexicon.StemCorpusCounts[stem] = 0
            for affix in signature_list:
                if affix not in Affixes:
                   Affixes[affix] = 0
                Affixes[affix] += 1
                if affix not in AffixToStem:
                    AffixToStem[affix] = dict()
                AffixToStem[affix][stem] = 1
                word = Strfn.clean_join(stem, affix, affix_type)
                if word not in Lexicon.WordToSig:
                    Lexicon.WordToSig[word] = list()
                Lexicon.WordToSig[word].append((stem,signature_string))
                if stem not in Lexicon.StemToWord:
                    Lexicon.StemToWord[stem] = dict()
                Lexicon.StemToWord[stem][word] = 1
                if word in Lexicon.Word_counts_dict:
                    Lexicon.StemCorpusCounts[stem] += Lexicon.Word_counts_dict[word]
                Lexicon.WordBiographies[word].append(prefix + " core signature-formation: " + signature_string)

            this_signature.add_stem(stem)
            this_signature.add_affix(affix)

        temp_sig_dict.clear()  # why?
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

    Lexicon.Parses.clear()
    for sig_string in Lexicon.Signatures:
        stems = Lexicon.Signatures[sig_string].get_stems()
        affixes = sig_string.split("=")
        for affix in affixes:
            if affix == "NULL":
                affix = ""
            if affix_type == "suffix":
                for affix in affixes:
                    for stem in stems:
                        Lexicon.Parses[(stem,affix)]=1
            else:
                for affix in affixes:
                    for stem in stems:
                        Lexicon.Parses[(affix,stem)]=1
    #print "   790   Number of parses in lexicon now:", len(Lexicon.Parses)
 # ----------------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------------#
def	Find_complex_signatures (Lexicon, affix_type):
# ----------------------------------------------------------------------------------------------------------------------------
	pass




def agree_on_first_letter_only(str1, str2):
    if len(str1) == 0 or len(str2) == 0:
        return False
    if str1[0] != str2[0]:
        return False
    if len(str1) == 1 or len(str2) == 1:
        return True
    if str1[1] == str2[1]:
        return False
    return True
# ----------------------------------------------------------------------------------------------------------------------------#
def	generate_shadow_signatures(lexicon):
# ----------------------------------------------------------------------------------------------------------------------------
    """ Each high-entropy signature generates a hypothesis about shadow signatures it probably generates"""
    shadowsigfile = open("shadow_signatures.txt", "w")
    shadow_signatures = dict()	
    ENTROPY_THRESHOLD = 1.6
    print "5. Finding spurious shadow signatures."
    for signature in lexicon.Signatures.values():
        if signature.get_stability_entropy() > ENTROPY_THRESHOLD:
            affixes = [affix for affix in signature.get_affix_list() if affix != "NULL"]
            affixes.sort()
            initials = [affix[0] for affix in affixes] 
            flag = False
            from_place = 0
            while from_place  < len(affixes) - 1 :
                for to_place in range(from_place+1, len(affixes)):
                    if  agree_on_first_letter_only(affixes[from_place], affixes[to_place]):
                        if to_place == len(affixes)-1 or affixes[to_place + 1][0] != affixes[from_place][0]:
                            package = (initials[from_place], affixes[from_place:to_place+1])
                            new_sig = list()
                            for affix in affixes[from_place:to_place+1]:
                                if len(affix) == 1:
                                    new_sig.append("NULL")
                                else: 
                                    new_sig.append(affix[1:])
                            new_sig.sort()
                            new_sig_string = "=".join(new_sig)
                            print >>shadowsigfile,  "\n{0:25s} shadow signature: {1:20s}".format(signature.display(), new_sig_string),
                            if new_sig_string in lexicon.Signatures:
                                entropy = lexicon.Signatures[new_sig_string].get_stability_entropy()
                                print >>shadowsigfile, "which was present. Entropy is: {0:1.5f} ".format( entropy),
                                if entropy < ENTROPY_THRESHOLD:
                                    print >>shadowsigfile, "We will eliminate ", new_sig_string, "."
                                    lexicon.ShadowSignatures[new_sig_string] = lexicon.Signatures[new_sig_string]
                            else:
                                print >>shadowsigfile, " but this shadow signature was not found as a signature" , new_sig_string
		            from_place = to_place + 1
                            break
                    else:  
                        from_place = to_place
                        break     
    print >>shadowsigfile, "\nComplete list of spurious shadow signatures:"
    siglist = lexicon.ShadowSignatures.keys()
    siglist.sort()
    for sig in siglist: 
        print >>shadowsigfile, sig  










