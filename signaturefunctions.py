def MakeSignatureStringFromAffixDict(affix_dict):
    affix_list=affix_dict.keys()
    affix_list.sort()
    count_of_NULLs = 0
    for i in range(len(affix_list)):
        if len(affix_list[i]) == 0:
                affix_list[i]= "NULL"
                count_of_NULLs += 1
    return "=".join(affix_list)

def MakeSignatureListFromSignatureString(sigstring):
    temp_list = sigstring.split("=")
    siglist = list()
    for affix in temp_list:
        if affix == "NULL":
            siglist.append("")
        else:
            siglist.append(affix)
    return siglist

def SortSignatureStringByLength(sig):
        chain = sig.split('=')
        for itemno in range(len(chain)):
                if chain[itemno] == "NULL":
                        chain[itemno] = ""
        chain.sort(key = lambda item:len(item), reverse=True)
        for itemno in range(len(chain)):
                if chain[itemno] == "":
                        chain[itemno] = "NULL"        
        return chain

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

def locallymorerobust(sig1,sig2):
	list1 = sig1.split('-')
	list2 = sig2.split('-')	
	if len(list1) > len(list2):
		return -1
	if len(list2)>len(list1):
		return 1
	if len(sig1) > len(sig2):
		return -1
	if len(sig2) > len (sig1):
		return 1
	return 0



def SortSignaturesByLocalRobustness(siglist): # if sig1 has more affixes than sig2, it is more locally robust; if two sigs have the same number of affixes, the one with more letters in the affixes is more locally
	siglist.sort(cmp=locallymorerobust)
	return siglist

# ----------------------------------------------------------------------------------------------------------------------------#
def FindGoodSignatureInsideAnother(target_affixes_list, siglist):
	SortSignaturesByLocalRobustness(siglist)
        #print "68 ", target_affixes_list
	for sig_string in siglist:
		these_affixes = set(MakeSignatureListFromSignatureString(sig_string))
                #print "    71 ", these_affixes
		if these_affixes.issubset(set(target_affixes_list)):
                        #print "    73", these_affixes
			return sig_string
	return None


def Sig1ExtendsSig2(sig1, sig2, outfile):  # for suffix signatures
	MaxLengthOfDifference = 2
	list1 = SortSignatureStringByLength(sig1)
	list2 = SortSignatureStringByLength(sig2)
	if len(list1) != len(list2):
		#print >>outfile, "C Different lengths"
		return (None, None, None)
	if sig1 == sig2:
		#print >>outfile, "E same signature" 
		return (None,None,None)
 
	length = len(list1)
	Sig1_to_Sig2 = dict()
	Sig2_to_Sig1 = dict()
	Differences = list()
	print "\n38", list1, list2
	for suffixno1 in range(length):  # we make an array of what suffix might possibly extend what suffix=
		print "  40", list1, list2
		suffix1 =  list1[suffixno1]
		suffix1_length = len(list1)
		if suffix1 == "NULL":  # this must be the last suffix in sig1, and there must be only one suffix left in LongerStrings
			suffix2 = list2.pop()
			Sig1_to_Sig2[suffix1] = suffix2
			Sig2_to_Sig1[suffix2] = suffix1
			Differences.append(suffix2)
			break
		length2 = len(list2)
		if length2 == 1 and list2[0]=="NULL":
			Sig1_to_Sig2[suffix1] = "NULL"
			Sig2_to_Sig1["NULL"] = suffix1
			Differences.append(suffix1)
		for suffixno2 in range(length2):
			suffix2 = list2[suffixno2]
			if suffix2[-1*suffix1_length:] == suffix1:
				if len(suffix2) - suffix1_length > MaxLengthOfDifference:
					continue
				else:
					if len(suffix2)>len(suffix1):
						Differences.append(len(suffix2)-len(suffix1))
					else:
						Differences.append(len(suffix1)-len(suffixno2))
					Sig1_to_Sig2[suffix1] = suffix2
					Sig2_to_Sig1[suffix2] = suffix1
					print "aligning:", suffix1, suffix2
 					del list2[suffixno2]
 					break # break from loop on suffixno2
 			if suffix1[-1*len(suffix2):] == suffix2:
				if len(suffix1) - len(suffix2) > MaxLengthOfDifference:
					continue
				else:
					if len(suffix1)>len(suffix2):
						Differences.append(len(suffix1)-len(suffix2))
					elif len(suffix2) > len(suffix1):
						Differences.append(len(suffix2)-len(suffix1))
					else: 
						Differences.append("NULL")
					Sig1_to_Sig2[suffix1] = suffix2
					Sig2_to_Sig1[suffix2] = suffix1
					print "aligning:", suffix1, suffix2
 					del list2[suffixno2]
 					break # break from loop on suffixno2
 		print "No affix found to align with ", suffix1
 		print "end of loop for :", suffix1

 
 
	AlignedList1 = list()
	AlignedList2 = list()
	Differences = list()

	print "Sig1ExtendsSig2 in signaturefunctions.py", sig1, sig2, Sig1_to_Sig2, Sig2_to_Sig1
	return (list1, list2, Differences)

def EvaluateSignatures(Lexicon, outfile):
	for sig in Lexicon.Signatures:
		print >> outfile, sig.Display()


def FindSignatureDifferences():
	Differences = list()
	for sig1, stemlist1 in SortedListOfSignatures:
		for sig2, stemlist2 in SortedListOfSignatures:
			if sig1 == sig2: continue
			list1, list2, differences = Sig1ExtendsSig2(sig1, sig2, outfile)
			Differences.append((sig1, sig2, list1, list2, differences))

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
			sig1string = list_to_string(item[2])
			sig2string = list_to_string(item[3])
			print >> outfile, item[0], " " * (width - len(item[0])), \
			item[1], " " * (width - len(item[1])), \
			sig1string, " " * (width - len(sig1string)), \
			sig2string, " " * (width - len(sig2string)), \
			item[4], " " * (width - len(item[4]))


def AddSignaturesToFSA(Lexicon, SignatureToStems, fsa, FindSuffixesFlag):
	for sig in SignatureToStems:
		affixlist = list(sig)
		stemlist = Lexicon.SignatureToStems[sig]
		if len(stemlist) >= Lexicon.MinimumStemsInaSignature:
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


