from copy import deepcopy

# -------------      Some short utility functions ---------------------------------------

def remove_parentheses (word):
    temp = list()
    for i in range(len(word)):
 	if word[i]=="(" or word[i]==")":
	    continue
	else:
	    temp.append(word[i])
    return "".join(temp)
 

def AddAffixToSigString(affix, sigstring):
    sigset = set(sigstring.split("="))
    if affix == "":
        affix = "NULL"
    sigset.add(affix)
    affixlist = list(sigset)
    affixlist.sort()
    sep = '='
    return sep.join(affixlist)


def MakeSignatureStringFromAffixDict(affix_dict):
    affix_list = affix_dict.keys()
    affix_list.sort()
    count_of_NULLs = 0
    for i in range(len(affix_list)):
        if len(affix_list[i]) == 0:
            affix_list[i] = "NULL"
            count_of_NULLs += 1
    return "=".join(affix_list)


def MakeSignatureStringFromSignatureList(siglist):
    for i in range(len(siglist)):
        if len(siglist[i]) == 0:
            siglist[i] = "NULL"
    return "=".join(siglist)


def MakeSignatureListFromSignatureString(sigstring):
    temp_list = sigstring.split("=")
    siglist = list()
    for affix in temp_list:
        #if affix == "NULL":
        #    siglist.append("")
        #else:
        siglist.append(affix)
    return siglist


def NumberOfAffixesInSigString(sig):
    return sig.count("=") + 1


def list_to_string(mylist):
    outstring = ""
    if mylist == None:
        return None
    sep = '='
    for i in range(len(mylist)):
        if mylist[i] == None:
            outstring += "@"
        else:
            outstring += mylist[i]
        if i < len(mylist) - 1:
            outstring += sep
    # print outstring
    return outstring


def SortSignatureStringByLength(sig):
    chain = sig.split('=')
    for itemno in range(len(chain)):
        if chain[itemno] == "NULL":
            chain[itemno] = ""
    chain.sort(key=lambda item: len(item), reverse=True)
    for itemno in range(len(chain)):
        if chain[itemno] == "":
            chain[itemno] = "NULL"
    return chain


def SortSignatureListByLength(sig):
    containedNULL_flag = False
    for itemno in range(len(sig)):
        if sig[itemno] == "NULL":
            sig[itemno] = ""
            containedNULL_flag = True
    sig.sort(key=lambda item: len(item), reverse=True)
    if containedNULL_flag:
        for itemno in range(len(sig)):
            if sig[itemno] == "":
                sig[itemno] = "NULL"
    return sig


def FindListWithLongerStrings(chain1, chain2):
    # assumes that chains are sorted in order of decreasing length
    # assumes the chains are of the same length
    if len(chain1) != len(chain2):
        return -1
    for no in range(len(chain1)):
        if len(chain1[no] > len(chain2[no])):
            return 1
        elif len(chain2[no]) > len(chain1[no]):
            return 2
    return 0


def locallymorerobust(sig1, sig2):
    if len(sig1) > len(sig2):
        return -1
    if len(sig2) > len(sig1):
        return 1
    sigstring1 = MakeSignatureStringFromSignatureList(sig1)
    sigstring2 = MakeSignatureStringFromSignatureList(sig2)
    if len(sigstring1) > len(sigstring2):
        return -1
    if len(sigstring2) > len(sigstring1):
        return 1
    return 0


def globallymorerobust(sig1, sig2):
    sig1_string = str(sig1[0])
    sig2_string = str(sig2[0])
    siglist1 = MakeSignatureListFromSignatureString(sig1_string)
    siglist2 = MakeSignatureListFromSignatureString(sig2_string)
    numberofaffixes1 = len(siglist1)
    numberofaffixes2 = len(siglist2)
    numberofstems1 = len(sig1[1])
    numberofstems2 = len(sig2[1])
    total_stem_length_1 = 0
    total_stem_length_2 = 0
    for stem in sig1[1]:
        total_stem_length_1 += len(stem)
    for stem in sig2[1]:
        total_stem_length_2 += len(stem)
    robustness1 = (numberofaffixes1 - 1) * total_stem_length_1
    robustness2 = (numberofaffixes2 - 1) * total_stem_length_2
    lettersinsig1 = 0
    lettersinsig2 = 0
    for affix in siglist1:
        lettersinsig1 += len(affix)
    for affix in siglist2:
        lettersinsig2 += len(affix)
    robustness1 += lettersinsig1 * (numberofstems1 - 1)
    robustness2 += lettersinsig2 * (numberofstems2 - 1)
    # print sig1[0], robustness1, sig2[0],  robustness2
    return robustness1 - robustness2


def SortSignaturesByLocalRobustness(
        siglist):  # if sig1 has more affixes than sig2, it is more locally robust; if two sigs have the same number of affixes, the one with more letters in the affixes is more locally
    siglist.sort(cmp=locallymorerobust)
    return siglist


def SortSignaturesByGlobalRobustness(signature_list, SignatureStringsToStems, outfile):
    temp_Sig_List = list()
    for sig in signature_list:
        stems = SignatureStringsToStems[sig].keys()
        sigpair = (sig, stems)
        temp_Sig_List.append(sigpair)
    temp_Sig_List.sort(cmp=globallymorerobust, reverse=True)
    signature_list = list()
    for sig, stemlist in temp_Sig_List:
        signature_list.append(sig)
        # print >>outfile," 135", sig, len(stemlist)
    return signature_list


# -----------------------------------------------------------------#

def EvaluateSignatures(Lexicon, outfile):
    for sig in Lexicon.Signatures:
        print >> outfile, sig.Display()


# -----------------------------------------------------------------#


# --------------------------------------------------------------------------------------------------------------------------
#     Important functions, called from main file

# ----------------------------------------------------------------------------------------------------------------------------#
def FindGoodSignatureListFromInsideAnother(target_affixes_list, siglist):
    good_affixes_set = set()
    


    for sig_string in siglist:
        these_affixes = set(MakeSignatureListFromSignatureString(sig_string))
        if these_affixes.issubset(set(target_affixes_list)):
            good_affixes_set.update(these_affixes)
    sig_list = list(good_affixes_set)
    sig_list.sort()
    return sig_list


# ----------------------------------------------------------------------------------------------------------------------------#
#  Call from the main function
# -----------------------------------------------------------------#
def extending_signatures(Lexicon, outfile, new_stem_length=3, ):
    signature_list = list()
    for sig in Lexicon.SignatureStringsToStems:
        if NumberOfAffixesInSigString(sig) < 2:
            continue
        signature_list.append(sig)
    signature_list = SortSignaturesByGlobalRobustness(signature_list, Lexicon.SignatureStringsToStems, outfile)
    FindSignatureDifferences(signature_list, outfile)


# ----------------------------------------------------------------------------------------------------------------------------#
# -----------------------------------------------------------------#
def FindSignatureDifferences(SortedListOfSignatureStrings, outfile):
    Differences = list()
    for signo1 in range(len(SortedListOfSignatureStrings)):
        sigS_1 = SortedListOfSignatureStrings[signo1]
        sigL_1 = MakeSignatureListFromSignatureString(sigS_1)
        # print " 186 ", sigL_1
        print >> outfile, "182 Find Sig Diffs", signo1, sigS_1, sigL_1
        if len(sigL_1) < 2:
            continue
        for signo2 in range(signo1 + 1, len(SortedListOfSignatureStrings)):
            sigS_2 = SortedListOfSignatureStrings[signo2]
            sigL_2 = MakeSignatureListFromSignatureString(sigS_2)
            # print >>outfile, "  192", sigL_2
            if sigL_1 == sigL_2:
                continue
            if len(sigL_2) == 1:
                print "     185 singleton"
                continue
            if len(sigL_1) != len(sigL_2):
                # print "     140 unequal lengths", sig_list1,len (sig_list1),  sig_list2, len(sig_list2)
                continue
            # print >>outfile, "    201", sigL_2
            # print "  200 Find sig differences", sigL_1, sigL_2

            Extends(sigL_1, sigL_2, outfile)

            # continue
            # Differences.append((sig_list1, sig_list2, list1, list2, differences))
            # print "200 sig1:", sig_list1, "     sig_list2:", sig_list2, "lists extracted: ", list1, list2
            # print "  146 {:20s} {:20s} {:40s} {:40s}) ".format(sig_list1,   sig_list2, list1, list2)
    Differences.sort(key=lambda entry: entry[4])
    width = 25
    h1 = "Sig 1"
    h2 = "Sig 2"
    h3 = "List 1"
    h4 = "List 2"
    h5 = "differences"
    print >> outfile, "Differences between similar pairs of signatures"
    print >> outfile, h1, " " * (width - len(h1)), \
        h2, " " * (width - len(h2)), \
        h3, " " * (width - len(h3)), \
        h4, " " * (width - len(h4)), \
        h5, " " * (width - len(h5))
    for item in Differences:
        if item[3] != None:
            # print "204", item
            sig1string = list_to_string(item[2])
            sig2string = list_to_string(item[3])
            print >> outfile, item[0], " " * (width - len(item[0])), \
                item[1], " " * (width - len(item[1])), \
                sig1string, " " * (width - len(sig1string)), \
                sig2string, " " * (width - len(sig2string)), \
                item[4], " " * (width - len(item[4]))


# ----------------------------------------------------------------------------------------------------------------------------#
def Extends(sigL_a, sigL_b, outfile, type="suffix"):
    # ----------------------------------------------------------------------------------------------------------------------------#
    """
    This function determines if sig2 extends sig1, meaning that there is a 1 to 1 association
    between affixes in the two signatures in which the affix in sig1 is a prefix of the corresponding affix in sig2.
    We assume at this time that both signatures are "almost suffix-free",
    meaning that if we iterate through the affixes in decreasing length, it
    is never the case that a longer affix will be matched against a string which should have been matched with a shorter affix.
    We make sure that signatures are in descending order of length of affix, with NULL given 0 length. 
    """
    # print >>outfile, "244 Extends", sigL_a, sigL_b
    if len(sigL_a) != len(sigL_b):
        return False
    sigL_1 = list(sigL_a)
    sigL_2 = list(sigL_b)
    SortSignatureListByLength(sigL_1)
    SortSignatureListByLength(sigL_2)
    AffixList1 = list()
    AffixList2 = list()
    print >> outfile, "253 Extends", sigL_1, sigL_2
    NullAffixFound = False
    UnmatchedAffix_in_Affixes_1 = list()
    siglength = len(sigL_1)

    if type == "suffix":
        # We iterate through affixes1-list:
        # We do not know which signature extends the other yet (if it does)
        for affixno in range(siglength):
            if sigL_1[affixno] == sigL_2[affixno]:
                # a match is found, so we add each affix to a list, and delete the affix from AffixList2
                affix1 = sigL_1[affixno]
                affix2 = sigL_2[affixno]
                AffixList1.append(affix1)
                AffixList2.append(affix2)
            else:
                break
        sig1affix = sigL_1[affixno]
        sig2affix = sigL_2[affixno]
        if len(sig1affix) > len(sig2affix):
            # sig1 may be an extention of sig2
            for affixno2 in range(len(sigL_2)):
                sig2affix = sigL_2[affixno2]
                if sig2affix == sig1affix[-1 * len(sig2affix):]:
                    print >> outfile, " 277 ", sig1affix, sig2affix
        else:
            len(sig1affix) > len(sig2affix)
            # sig2 may be an extention of sig1
            for affixno2 in range(len(sigL_2)):
                sig2affix = sigL_2[affixno2]
                if sig1affix == sig2affix[-1 * len(sig1affix):]:
                    print >> outfile, " 286 ", sig1affix, sig2affix

        for affix1 in sigL_1:
            MatchedSuffixFound = False
            # if affix1 is NULL, we just hold on to that fact until the very end of the matching
            if affix1 == "":
                NullAffixFound = True
                continue
            for affixno2 in range(len(sigL_2)):
                affix2 = sigL_2[affixno2]
                if len(affix1) > len(affix2):
                    # If this is so, affix2 can't *continue* affix1
                    continue
                if affix1 == affix2[-1 * len(affix1):]:
                    # a match is found, so we add each affix to a list, and delete the affix from AffixList2
                    MatchedSuffixFound = True
                    AffixList1.append(affix1)
                    AffixList2.append(affix2)
                    del sigL_2[affixno2]
                    break
            if MatchedSuffixFound == False:
                # Here we have looked at all the affixes in AffixList2, and found no alignment could be made:
                UnmatchedAffix_in_Affixes_1.append(affix1)
        if len(sigL_2) == 1 and NullAffixFound:
            AffixList1.append("")
            AffixList2.append(sigL_2[0])
        else:
            return False;
        print >> outfile, "Extends", AffixList1, AffixList2
        return (AffixList1, AffixList2);


# Call from
# DEPRECATED -- remove
def Siglist1ExtendsSiglist2(siglist_A, siglist_B, outfile):  # for suffix signatures
    MaxLengthOfDifference = 2
    # list1 = SortSignatureStringByLength(sig1)
    # list2 = SortSignatureStringByLength(sig2)
    siglist1 = SortSignatureListByLength(siglist_A)
    siglist2 = SortSignatureListByLength(siglist_B)
    # siglist2.sort(lambda x,y:cmp(len(x), len(y)))
    # print "92", siglist_A, siglist1, siglist_B, siglist2
    if len(siglist1) != len(siglist2):
        # print >>outfile, "C Different lengths"
        return (None, None, None)
    if siglist1 == siglist2:
        # print >>outfile, "E same signature"
        return (None, None, None)

    length = len(siglist1)
    Sig1_to_Sig2 = dict()
    Sig2_to_Sig1 = dict()
    Differences = list()
    # print "\n38", siglist1, siglist2
    for suffixno1 in range(length):  # we make an array of what suffix might possibly extend what suffix=
        # print "  40", siglist1, siglist2, suffixno1
        suffix1 = siglist1[suffixno1]
        suffix1_length = len(siglist1)
        if suffix1 == "NULL":  # this must be the last suffix in sig1, and there must be only one suffix left in LongerStrings
            suffix2 = siglist2.pop()
            Sig1_to_Sig2[suffix1] = suffix2
            Sig2_to_Sig1[suffix2] = suffix1
            Differences.append(suffix2)
            break
        length2 = len(siglist2)
        if length2 == 1 and siglist2[0] == "NULL":
            Sig1_to_Sig2[suffix1] = "NULL"
            Sig2_to_Sig1["NULL"] = suffix1
            Differences.append(suffix1)
        for suffixno2 in range(length2):
            suffix2 = siglist2[suffixno2]
            if suffix2[-1 * suffix1_length:] == suffix1:
                if len(suffix2) - suffix1_length > MaxLengthOfDifference:
                    continue
                else:
                    if len(suffix2) > len(suffix1):
                        Differences.append(len(suffix2) - len(suffix1))
                    else:
                        Differences.append(len(suffix1) - len(suffix2))
                    Sig1_to_Sig2[suffix1] = suffix2
                    Sig2_to_Sig1[suffix2] = suffix1
                    # print "aligning:", suffix1, suffix2
                    del siglist2[suffixno2]
                    break  # break from loop on suffixno2
            if suffix1[-1 * len(suffix2):] == suffix2:
                if len(suffix1) - len(suffix2) > MaxLengthOfDifference:
                    continue
                else:
                    if len(suffix1) > len(suffix2):
                        Differences.append(len(suffix1) - len(suffix2))
                    elif len(suffix2) > len(suffix1):
                        Differences.append(len(suffix2) - len(suffix1))
                    else:
                        Differences.append("NULL")
                    Sig1_to_Sig2[suffix1] = suffix2
                    Sig2_to_Sig1[suffix2] = suffix1
                    # print "aligning:", suffix1, suffix2
                    del siglist2[suffixno2]
                    break  # break from loop on suffixno2
                    # print "  149 No affix found to align with ", suffix1
                    # print "  150 End of loop for :", suffix1

    print "\n  247 Siglist1ExtendsSiglist2 in signaturefunctions.py", siglist1, siglist2, Sig1_to_Sig2, Sig2_to_Sig1
    return (siglist1, siglist2, Differences)


def AddSignaturesToFSA(Lexicon, SignatureStringsToStems, fsa, FindSuffixesFlag):
    for sig in SignatureStringsToStems:
        affixlist = sig.split('=')
        stemlist = Lexicon.SignatureStringsToStems[sig]
        #if len(stemlist) >= Lexicon.MinimumStemsInaSignature:
        if FindSuffixesFlag:
            fsa.addSignature(stemlist, affixlist, FindSuffixesFlag)
        else:
            fsa.addSignature(affixlist, stemlist, FindSuffixesFlag)


# ----------------------------------------------------------------------------------------------------------------------------#
def ShiftSignature(sig_target, shift, StemToWord, Signatures, outfile):
    # ----------------------------------------------------------------------------------------------------------------------------#
    print >> outfile, "-------------------------------------------------------"
    print >> outfile, "Shift wrongly cut suffixes"
    print >> outfile, "-------------------------------------------------------"
    suffixlist = []
    print >> outfile, sig_target, shift
    suffixes = sig_target.split('-')
    for n in range(len(suffixes)):
        if suffixes[n] == 'NULL':
            suffixes[n] = ''
    for suffix in suffixes:
        suffix = shift + suffix
        suffixlist.append(suffix)
    suffixlist.sort()
    newsig = '-'.join(suffixlist)
    Signatures[newsig] = set()
    shiftlength = len(shift)
    stemset = Signatures[sig_target].copy()  # a set to iterate over while removing stems from Signature[sig_target]
    for stem in stemset:
        thesewords = []
        if not stem.endswith(shift):
            continue
        newstem = stem[:-1 * shiftlength]
        for suffix in suffixes:
            thesewords.append(stem + suffix)
        Signatures[sig_target].remove(stem)
        Signatures[newsig].add(newstem)
        for word in thesewords:
            StemToWord[stem].remove(word)
        if len(StemToWord[stem]) == 0:
            del StemToWord[stem]
        if not newstem in StemToWord:
            StemToWord[newstem] = set()
        for word in thesewords:
            StemToWord[newstem].add(word)
    if len(Signatures[sig_target]) == 0:
        del Signatures[sig_target]
    # ----------------------------------------------------------------------------------------------------------------------------#
    return (StemToWord, Signatures)


# ----------------------------------------------------------------------------------------------------------------------------#




# ----------------------------------------------------------------------------------------------------------------------------#
def PullOffSuffix(sig_target, shift, StemToWord, Signatures, outfile):
    # ----------------------------------------------------------------------------------------------------------------------------#
    print >> outfile, "-------------------------------------------------------"
    print >> outfile, "Pull off a suffix from a stem set"
    print >> outfile, "-------------------------------------------------------"
    print >> outfile, sig_target, shift

    shiftlength = len(shift)
    newsig = shift
    suffixes = sig_target.split('-')
    stemset = Signatures[sig_target].copy()  # a set to iterate over while removing stems from Signature[sig_target]
    while newsig in Signatures:
        newsig = "*" + newsig  # add *s to beginning to make sure the string is unique, i.e. not used earlier elsewhere

    Signatures[newsig] = set()
    StemToWord["*" + shift] = sig_target

    for stem in stemset:
        thesewords = []
        if not stem.endswith(shift):
            continue
        newstem = stem[:-1 * shiftlength]
        for suffix in suffixes:
            if suffix == "NULL":
                word = stem
            else:
                word = stem + suffix
            StemToWord[stem].remove(word)

        if len(StemToWord[stem]) == 0:
            del StemToWord[stem]
        if newstem in StemToWord:
            newstem = "*" + newstem
            StemToWord[newstem] = set()
        for word in thesewords: StemToWord[newstem].add(word)
    if len(Signatures[sig_target]) == 0:
        del Signatures[sig_target]
    # ----------------------------------------------------------------------------------------------------------------------------#
    return (StemToWord, Signatures)




# ----------------------------------------------------------------------------------------------------------------------------#
def find_signature_chains(lexicon):
    # ----------------------------------------------------------------------------------------------------------------------------#
# "Chain" here simply refers to inclusion of words under 2 or more signatures. e.g. Null=s contains some words that are also in ed-ing-ings .
    signature_containments = dict()
    wordtosig=lexicon.WordToSig
    for word in wordtosig:
        if wordtosig[word]  and len(wordtosig[word]) >1:
            sigs = wordtosig[word]
            for i in range(len(sigs)-1):
		(stem1,sig1) = sigs[i]
                for j in range(i+1,len(sigs)):
		    (stem2,sig2) = sigs[j]
		    if len(stem1) > len(stem2):
			stem2length = len(stem2)
			difference = stem1[stem2length:]
			sigpair= (sigs[j][1],sigs[i][1])
		    else:
			stem1length = len(stem1)
			difference = stem2[stem1length:]
                        sigpair=(sigs[i][1],sigs[j][1])
                    if difference not in signature_containments:
                        signature_containments[difference] = dict()
                    if sigpair not in signature_containments[difference]:
			signature_containments[difference][sigpair] = dict()
		    if (stem1,stem2) not in signature_containments[difference][sigpair]:
			signature_containments[difference][sigpair][(stem1,stem2)] = 1
		    else: 
			signature_containments[difference][sigpair][(stem1,stem2)]+= 1
		    #print "567", difference, sigpair

	
    difference_list = signature_containments.keys()
    difference_list.sort(key=lambda x: len(signature_containments[x]), reverse=True)

    formatstring = "{{0:10s} {1:5d {2:15s} {3:5d}}"
    if (True):
	    for difference in difference_list:
		print difference, "573 signature functions"
		for sigpair in signature_containments[difference]:
		    print difference, sigpair, signature_containments[difference][sigpair]
    return (signature_containments,difference_list)			

#June 2017
# ----------------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------------
