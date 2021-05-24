from copy import deepcopy
from stringfunctions import remove_label 

# -------------      Some short utility functions ---------------------------------------

def list_contains(list1, list2):
    for item in list2:
        if item not in list1:
            return False
    return True

def contains(sigstring1, sigstring2):
    list1 = signature_string_to_signature_list(sigstring1)
    list2 = signature_string_to_signature_list(sigstring2)
    for item in list2:
        if item not in list1:
            return False
    return True

def AddAffixToSigString(affix, sigstring):
    sigset = set(sigstring.split("="))
    if affix == "":
        affix = "NULL"
    sigset.add(affix)
    affixlist = list(sigset)
    affixlist.sort()
    sep = '='
    return sep.join(affixlist)

def sig_dict_to_string(affix_dict):
    affix_list = list()
    for affix in affix_dict.keys():
        affix_list.append(remove_label(affix))
    affix_list.sort()
    for i in range(len(affix_list)):
        if len(affix_list[i]) == 0:
            affix_list[i] = "NULL"
    return "=".join(affix_list)

def sig_dict_to_list(affix_dict):
    affix_list = affix_dict.keys()
    affix_list.sort()
    return affix_list

#deprecated:
def make_signature_string_from_affix_dict(affix_dict):
    affix_list = affix_dict.keys()
    affix_list.sort()
    count_of_NULLs = 0
    for i in range(len(affix_list)):
        if len(affix_list[i]) == 0:
            affix_list[i] = "NULL"
            count_of_NULLs += 1
    return "=".join(affix_list)

def sig_list_to_sig_string(siglist):
    if len(siglist) == 0:
        print "signature functions 54 problem"
        return ""
    affix_list = [remove_label(affix) for affix in siglist]
    for i in range(len(affix_list)):
        if len(affix_list[i]) == 0:
            affix_list[i] = "NULL"
    affix_list.sort()
    return "=".join(affix_list)

def make_signature_string_from_signature_list(siglist):
    if len(siglist) == 0:
        print "signature functions 54 problem"
        return ""
    for i in range(len(siglist)):
        if len(siglist[i]) == 0:
            siglist[i] = "NULL"
    return "=".join(siglist)

def signature_string_to_signature_list(sigstring):
    temp_list = sigstring.split("=")
    siglist = list()
    for affix in temp_list:
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
            print
            print 77, outstring,
            print 78, mylist[i]
            outstring += mylist[i]
        if i < len(mylist) - 1:
            outstring += sep
    # print outstring
    return outstring

def sort_signature_string_by_length(sig):
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
    sigstring1 = make_signature_string_from_signature_list(sig1)
    sigstring2 = make_signature_string_from_signature_list(sig2)
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


def SortSignaturesByLocalRobustness(siglist):  # if sig1 has more affixes than sig2, it is more locally robust; if two sigs have the same number of affixes, the one with more letters in the affixes is more locally
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

  
