def SortSignatureStringByLength(sig):
        chain = sig.split('-')
        for itemno in range(len(chain)):
                if chain[itemno] == "NULL":
                        chain[itemno] = ""
        chain.sort(key = lambda item:len(item), reverse=True)
        for itemno in range(len(chain)):
                if chain[itemno] == "":
                        chain[itemno] = "NULL"        
        return chain

# ----------------------------------------------------------------------------------------------------------------------------#
def Sig1ExtendsSig2(sig1, sig2, outfile):  # for suffix signatures
	MaxLengthOfDifference = 2
	list1 = list(sig1 )
	list2 = list(sig2 )
	#print >>outfile, "B -------------------", sig1, sig2
	if len(list1) != len(list2):
		#print >>outfile, "C Different lengths"
		return (None, None, None)
	if sig1 == sig2:
		#print >>outfile, "E same signature" 
		return (None,None,None)
	length = len(list1)
	ThisExtendsThat = dict()
	for suffixno1 in range(length):  # we make an array of what suffix might possibly extend what suffix
		suffix1 = list1[suffixno1]
		ThisExtendsThat[suffixno1] = dict()
		if suffix1 == "NULL":
			suffix1_length = 0
		else:
			suffix1_length = len(suffix1)

		for suffixno2 in range(length):
			suffix2 = list2[suffixno2]
			if suffix2 == "NULL":
				suffix2_length = 0
			else:
				suffix2_length = len(suffix2) 
			if suffix1 == suffix2:
				ThisExtendsThat[suffixno1][suffixno2] = 1
			elif suffix2_length == 0 and suffix1_length <= MaxLengthOfDifference:
				ThisExtendsThat[suffixno1][suffixno2] = 1
			elif suffix1[-1 * suffix2_length:] == suffix2 and abs(suffix1_length - suffix2_length) <= MaxLengthOfDifference:  
				ThisExtendsThat[suffixno1][suffixno2] = 1
				#print suffix1,suffix2, suffix1_length, suffix2_length, suffix1_length - suffix2_length
			else:
				ThisExtendsThat[suffixno1][suffixno2] = 0
	for pos in range(length):  # now we try to find a good alignment
		thisrowcount = sum(ThisExtendsThat[pos].values())
		if thisrowcount == 1:  # this means only one alignment is permitted, so this is helpful to know.
			for pos2 in range(length):
				if ThisExtendsThat[pos][pos2] == 1:
					that_pos = pos2
					break
			for pos3 in range(length):
				if pos3 != pos:
					ThisExtendsThat[pos3][that_pos] = 0

	# at this point, if any row is empty, then alignment is impossible. If any row has two 1's, then alignment is still ambiguous, but this is very unlikely.
	#for pos1 in range(length):
	#	for pos2 in range(length):
	#		print >>outfile, ThisExtendsThat[pos1][pos2],
	#	print >>outfile

	AlignPossibleFlag = True
	AlignedList1 = list()
	AlignedList2 = list()
	Differences = list()
	for pos in range(length):
		rowcount = sum(ThisExtendsThat[pos].values())
		if rowcount == 0:
			AlignmentPossibleFlag = False
			#print >>outfile, "G Alignment impossible"
			break
		if rowcount == 1:
			AlignedList1.append(list1[pos])
			for pos2 in range(length):
				if ThisExtendsThat[pos][pos2] == 1:
					AlignedList2.append(list2[pos2])
					if list2[pos2] == "NULL":
						sig2_item_length = 0
					else:
						sig2_item_length = len(list2[pos2])
					lengthofdifference = len(list1[pos]) - sig2_item_length
					if list1[pos] == "NULL" and list2[pos2] == "NULL":
						Differences.append("")
					else:
						Differences.append(list1[pos][:lengthofdifference])

	if AlignPossibleFlag == True:
		if len(Differences) == len(list1):
			return (AlignedList1, AlignedList2, Differences)
		else:
			return (None, None, None)
	else:
		return (None, None, None)




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


