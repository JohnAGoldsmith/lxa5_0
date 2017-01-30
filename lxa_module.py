import math
import os
import sys
from ClassLexicon import *
 

# from fsm import State, Transducer, get_graph



""""	 Signatures is a map: its keys are signatures. Its values are *sets* of stems. 
	 StemToWord is a map; its keys are stems.      Its values are *sets* of words.
	 StemToSig is a map; its keys are stems.       Its values are individual signatures.
	 WordToSig is a Map. its keys are words.       Its values are *lists* of signatures.
	 StemCounts is a map. Its keys are words. 	Its values are corpus counts of stems.
"""  # ---------------------------------------------------------------------------------------------------------------------------------------------#


def list_to_string(mylist):
	outstring = ""
	if mylist == None:
		return None
	sep = '-'
	for i in range(len(mylist)):
		if mylist[i] == None:
			outstring += "@"
		else:
			outstring += mylist[i]
		if i < len(mylist) - 1:
			outstring += sep
	# print outstring
	return outstring


# ------------------- New -----------------------------------------------------------------------------------
def makeFSM(morphology, Signatures, start, end):
	stateDict = dict()
	signumber = 0
	howmanywords = 3
	numberOfSignaturesToDisplay = 8
	SortedListOfSignatures = sorted(Signatures.items(), lambda x, y: cmp(len(x[1]), len(y[1])), reverse=True)
	for sig, stemset in SortedListOfSignatures:
		stemlist = list(stemset)
		stateDict[signumber] = State(sig)
		for i in range(howmanywords):
			if i == len(stemlist):
				break
			start[stemlist[i]] = stateDict[signumber]
		for affix in sig.split('-'):
			stateDict[signumber][affix] = end
		signumber += 1
		if signumber > numberOfSignaturesToDisplay:
			break
	get_graph(morphology).draw('morphology.png', prog='dot')


# ---------------------------------------------------------#
def decorateFilenameWithIteration(filename, outfolder, extension):
	# Check that logfilename does NOT contain a (.
	filenameLength = len(filename)
	filenames = os.listdir(outfolder)
	suffixes = list()
	maxvalue = 0
	for thisfilename in filenames:
		pieces = thisfilename.partition("(")
		if thisfilename[0:filenameLength] == filename:
			remainder = thisfilename[
						len(filename):]  # chop off the left-side of the thisfile's name, the part that is filename
			if thisfilename[-1 * len(extension):] == extension:
				remainder = remainder[:-1 * len(extension)]  # chop off the extension
				if len(remainder) > 0 and remainder[0] == "(" and remainder[-1] == ")":
					stringFileNumber = remainder[1:-1]
					if stringFileNumber > maxvalue:
						maxvalue = int(stringFileNumber)
	if maxvalue > 0:
		filename = outfolder + filename + "(" + str(maxvalue + 1) + ")" + extension
	else:
		filename = outfolder + filename + "(0).txt"
	return filename



# ------------------- end of New -----------------------------------------------------------------------------------
# ---------------------------------------------------------#
def makesortedstring(string):
	letters = list(string)
	letters.sort()
	return letters


# ---------------------------------------------------------#
def formatPRule(pair):
	piece1 = pair[0]
	piece2 = pair[1]
	if len(piece1) == 0 and len(piece2) == 0:
		outstring = "[ @ ]"
		return outstring
	if len(piece1) == 0:
		piece1 = "@"
	if len(piece2) == 0:
		piece2 = "@"
	outstring = "[" + piece1 + " = " + piece2 + "]"
	return outstring


# ---------------------------------------------------------#
def maximalcommonprefix(a, b):
	howfar = len(a)
	if len(b) < howfar:
		howfar = len(b)
	for i in range(howfar):
		if not a[i] == b[i]:
			return a[:i]
	return a[:howfar]


# ---------------------------------------------------------#
def listToSignature(thislist):
	for i in range(len(thislist)):
		if i == 0:
			signature = thislist[0]
		else:
			signature += "-" + thislist[i]
	return signature


# ---------------------------------------------------------#
def maximalcommonsuffix(a, b):
	alen = len(a)
	blen = len(b)
	howfar = alen
	if len(b) < howfar:
		howfar = len(b)
	for i in range(0, howfar, 1):
		if not a[alen - i - 1] == b[blen - i - 1]:
			startingpoint = alen - i
			return a[startingpoint:]
	return a[(alen - howfar):]


# ---------------------------------------------------------#
def DeltaLeft(a,
			  b):  # Returns a pair of strings, consisting of prefixes of a and b, up to the maximal common suffix that a and b share.
	howfar = len(a)
	if len(b) < howfar:
		howfar = len(b)
	# if a == "s" and b == "rs":
	# print "\n 1 DeltaLeft" ,a,"/", b, "howfar: ",  howfar
	i = 1
	while i < howfar + 1:
		# print "2 i = ", i, a[len(a) - i], b[len(b) - i]
		if not a[len(a) - i] == b[len(b) - i]:
			# print "disagreement at ", i
			a_piece = len(a) - i + 1
			b_piece = len(b) - i + 1
			# print "3. Will return ",a[:a_piece], ",", b[:b_piece]
			return (a[:a_piece], b[:b_piece])
		i += 1
	# print "4 no difference during string checkover shorter string, i is ",i
	a_piece = len(a) - i + 1
	b_piece = len(b) - i + 1
	# if a == "s" and b == "rs":
	# print "5. Will return ", a[:a_piece],"/",  b[:b_piece]
	return (a[:a_piece], b[:b_piece])


# ---------------------------------------------------------#
def DeltaRight(a,
			   b):  # Returns a pair of strings, consisting of the suffixes of each string following any maximal common prefix that may exist.
	howfar = len(a)
	if len(b) < howfar:
		howfar = len(b)
	for i in range(howfar):
		if not a[i] == b[i]:
			return (a[i:], b[i:])
	return (a[howfar:], b[howfar:])


# ---------------------------------------------------------#
def DifferenceOfDifference((X1, X2), (Y1, Y2), DiffType):
	if DiffType == "suffixal":
		# print
		lowerdifference = DeltaLeft(X2, Y2)
		# print "*2.1", X2,":",Y2, ":",lowerdifference
		upperdifference = DeltaLeft(X1, Y1)
		# print "*2.2", X1,":",Y1,":", upperdifference
		# print
		r1 = upperdifference
		r2 = lowerdifference
		return (r1, r2)

	if DiffType == "prefixal":
		# print
		lowerdifference = DeltaRight(X2, Y2)
		# print "*2.1", X2,":",Y2, ":",lowerdifference
		upperdifference = DeltaRight(X1, Y1)
		# print "*2.2", X1,":",Y1,":", upperdifference
		# print
		r1 = upperdifference
		r2 = lowerdifference
		return (r1, r2)

	if DiffType == "unordered":
		x1 = list(X1)
		x2 = list(X2)
		y1 = list(Y1)
		y2 = list(Y2)
		r1 = []
		r2 = []
		x1.extend(y2)  # add y2 to x1
		del y2[:]
		x1.sort()

		x2.extend(y1)
		del y1[:]
		x2.sort()

		while len(x1) > 0:  # remove anything in y1 from x1
			if len(x2) == 0:
				r1.extend(x1)
				del x1[:]
				break
			else:
				if x1[0] < x2[0]:
					r1.append(x1.pop(0))
				elif x1[0] == x2[0]:
					x1.pop(0)
					x2.pop(0)
				else:
					r2.append(x2.pop(0))
		if len(x2) > 0:
			r2.extend(x2)
			del x2[:]

		r1 = ''.join(r1)
		r2 = ''.join(r2)
	return (r1, r2)


# ---------------------------------------------------------#

def makesignature(a):
	delimiter = '.'
	sig = ""
	for i in range(len(a) - 1):
		if len(a[i]) == 0:
			sig += "NULL"
		else:
			sig += a[i]
		sig += delimiter
	sig += a[len(a) - 1]
	# print "sig", sig
	return sig


# ---------------------------------------------------------#
def makesignaturefrom2words(a, b):
	stemlength = 0
	howfar = len(a)
	if len(b) < howfar:
		howfar = len(b)
	for i in range(0, howfar, -1):
		if a[i] == b[i]:
			stemlength = i + 1
		else:
			break;
	affix1 = a[:stemlength]
	affix2 = b[:stemlength]
	if len(affix1) == 0:
		affix1 = "NULL"
	if len(affix2) == 0:
		affix2 = "NULL"
	return (affix1, affix2)


# ---------------------------------------------------------#
def stringdiff(instring1, instring2):
	if instring1 == 'NULL':
		instring1 = ''
	if instring2 == 'NULL':
		instring2 = ''
	# ---------------------------#
	"""
	# this function can look for suffixal differences, prefixal differences, or unordered string differences
	"""
	# ---------------------------#
	DiffType = "suffixal"

	if DiffType == "suffixal":
		# this returns a pair of lists, which give the differences of the ends of instring1 and instring2
		positive, negative = DeltaRight(instring1, instring2)
		# print "stringdiff: ", instring1,':', instring2,':', positive,':', negative
		return (positive, negative)
	elif DiffType == "unordered":
		string1 = makesortedstring(instring1)
		# print string1
		string2 = makesortedstring(instring2)
		i = 0
		j = 0
		del positive[:]
		del negative[:]
		while (True):
			if (i < len(string1) and j < len(string2)):
				if (string1[i] == string2[j]):
					i = i + 1
					j = j + 1
				elif (string1[i] < string2[j]):
					positive.append(string1[i])
					i = i + 1
				else:
					negative.append(string2[j])
					j = j + 1
			elif i == len(string1) and j == len(string2):
				for k2 in range(j, len(string2)):
					negative.append(string2[k2])
				for k1 in range(i, len(string1)):
					positive.append(string1[k1])
				break
			elif (i >= len(string1)):
				for k2 in range(j, len(string2)):
					negative.append(string2[k2])
				break
			elif (j >= len(string2)):
				for k1 in range(i, len(string1)):
					positive.append(string1[k1])
				break
	positive = ''.join(positive)
	negative = ''.join(negative)
	return (positive, negative)


# ---------------------------------------------------------------------------------------------------------------------------------------------#
class intrasignaturetable:
	def setsignature(self, sig):
		self.affixes = sig.split('-')
		self.affixlabels = {}  # use this if we care deeply about the spelling of the morphemes
		for affix in self.affixes:
			self.affixlabels[affix] = affix
		# if affix=='NULL':
		#	affix = ''
		self.indexed_affixlabels = []  # use this if we have entered the elements of the signature in a particular and significant order, an order which we wish to use to compare against another signature e.g.
		for m in range(len(self.affixes)):
			self.indexed_affixlabels.append(affix)
		self.differences = {}  #
		self.indexed_differences = {}
		positive = []
		negative = []

		for m in range(len(self.affixes)):
			affix1 = self.affixes[m]
			for n in range(len(self.affixes)):
				affix2 = self.affixes[n]
				(positive, negative) = stringdiff(affix1, affix2)
				self.differences[(affix1, affix2)] = (positive, negative)
				self.indexed_differences[(m, n)] = (positive, negative)

	def compress(self):
		# print "sig", self.affixes, self.differences
		pairInventory = {}
		costPerLetter = 5
		costForNull = 1
		TotalCost = 0
		# print
		for pair in self.differences:
			(positive, negative) = self.differences[pair]
			pairString = ''.join(positive) + ':' + ''.join(negative)
			# print "pairString", pairString
			if not pairString in pairInventory:
				pairInventory[pairString] = 1
			# print "new pair: ", pairString, len(positive), len(negative)
			else:
				pairInventory[pairString] += 1
		for pair in pairInventory:
			# print pair
			pieces = pair.split(':')
			affix1 = pieces[0]
			affix2 = pieces[1]
			if len(affix1) == 0 and len(affix2) == 0:
				costA = 0
				costB = 0
			# print "both null"
			else:
				if len(affix1) == 0:
					costA = costForNull
				else:
					costA = len(affix1) * costPerLetter
				if len(affix2) == 0:
					costB = costForNull
				else:
					costB = len(affix2) * costPerLetter
				TotalCost += (costA + costB) + (pairInventory[pair] - 1)  # we pay the "full price" for the first pair,
				# and each additional occurrence costs just one bit.
				# print costA, costB

				# print TotalCost
		# print TotalCost
		return (TotalCost, pairInventory)

	def display(self):
		positive = []
		negative = []

	# print 'making table'
	# print '\t',
	# for affix in self.affixes:
	#	print affix, '\t',
	# print

	# for affix1 in self.affixes:
	#	print affix1, ':','\t',
	#	for affix2 in self.affixes:
	#		print self.differences[(affix1, affix2)][0],':',self.differences[(affix1, affix2)][1],
	#	print
	def changeAffixLabel(self, before, after):
		for n in range(len(self.affixes)):
			if self.affixes[n] == before:
				self.affixlabels[before] = after
				return
		return

	def changeIndexedAffixLabel(self, index, after):
		self.indexed_affixlabels[index] = after

	def displaytofile(self, outfile):
		positive = []
		negative = []

		for affix in self.affixes:
			print >> outfile, '%18s' % self.affixlabels[affix],
		print >> outfile

		for affix1 in self.affixes:
			print >> outfile, '%10s' % self.affixlabels[affix1],
			for affix2 in self.affixes:
				# print "display to file, suffixes", affix1, affix2
				item = self.differences[(affix1, affix2)]
				print >> outfile, '[%4s]:[%-4s]    ' % (item[0], item[1]),
			print >> outfile
		TotalCost, pairInventory = self.compress()
		print >> outfile, "Compressed form: ", TotalCost
		return TotalCost

	def displaytolist(self, outlist):
		positive = []
		negative = []
		outlist = []
		line = "@"  # makes empty box in table
		for affix in self.affixes:
			line = line + "\t" + self.affixlabels[affix]
		outlist.append(line)
		for affix1 in self.affixes:
			line = self.affixlabels[affix1]
			for affix2 in self.affixes:
				# print "display to file, suffixes", affix1, affix2
				item = self.differences[(affix1, affix2)]
				part1 = item[0]
				part2 = item[1]
				if len(part1) == 0 and len(part2) == 0:
					line = line + " $NULL$"
				else:
					if len(part1) == 0:
						part1 = "NULL"
					if len(part2) == 0:
						part2 = "NULL"
					line = line + " $\\frac{" + part1 + "}{" + part2 + "}$"
			outlist.append(line)
		return outlist

	def displaytolist_aligned_latex(self, outlist):
		positive = []
		negative = []
		outlist = []
		affix1 = ""
		line = "@"  # makes empty box in table
		for n in range(len(self.affixes)):
			line = line + "\t" + self.indexed_affixlabels[n]
		outlist.append(line)
		for n in range(len(self.affixes)):
			affix1 = self.affixes[n]
			line = self.indexed_affixlabels[n]
			for m in range(len(self.affixes)):
				affix2 = self.affixes[m]
				item = self.indexed_differences[(n, m)]
				part1 = item[0]
				part2 = item[1]
				if len(part1) == 0 and len(part2) == 0:
					line = line + " $NULL$"
				else:
					if len(part1) == 0:
						part1 = "NULL"
					if len(part2) == 0:
						part2 = "NULL"
					line = line + " $\\frac{" + part1 + "}{" + part2 + "}$"
			outlist.append(line)
		return outlist

	def displaytolist_aligned(self, outfile):
		positive = []
		negative = []
		outlist = []
		colwidth = 30
		# outputtemplate = "%25s"
		# outputtemplate2 = "    [%5s %5s]    "
		# outputtemplate3 = "%5s]"

		print >> outfile, "".center(15),
		for n in range(len(self.affixes)):
			affix1 = self.affixes[n]
			# print >>outfile,  '%25s' %self.indexed_affixlabels[n],
			print >> outfile, self.indexed_affixlabels[n].ljust(30),
		print >> outfile
		for n in range(len(self.affixes)):
			affix1 = self.affixes[n]
			# print >>outfile, '%15s' %self.indexed_affixlabels[n],
			print >> outfile, self.indexed_affixlabels[n].ljust(15),
			for m in range(len(self.affixes)):
				affix2 = self.affixes[m]
				item = self.indexed_differences[(n, m)]
				part1 = item[0]
				part2 = item[1]
				if len(part1[0]) == 0 and len(part1[0]) == 0 and len(part2[0]) == 0 and len(part2[1]) == 0:
					#	#print >>outfile, "[    NULL   ]    ",
					print >> outfile, "[ @ ]".ljust(colwidth),
				else:
					outstring1 = formatPRule(part1)
					outstring2 = formatPRule(part2)
					# print >>outfile, outputtemplate2 %(outstring1, outstring2,)
					print >> outfile, outstring1, ":", outstring2.ljust(15), "".ljust(colwidth - 19 - len(outstring1)),
					# print >>outfile, outputtemplate3 %outstring, # '[%4s]:[%-4s]    '%(firstpiece,secondpiece) ,
			print >> outfile

		return

	def minus(self, other, DiffType):
		counterpart = {}
		(alignedAffixList1, alignedAffixList2) = FindBestAlignment(self.affixes, other.affixes)
		for i in range(len(alignedAffixList1)):
			counterpart[alignedAffixList1[i]] = alignedAffixList2[i]
		for index1 in range(len(alignedAffixList1)):
			for index2 in range(len(alignedAffixList2)):
				thispiece1 = alignedAffixList1[index1]
				thispiece2 = alignedAffixList1[index2]
				otherpiece1 = alignedAffixList2[index1]
				otherpiece2 = alignedAffixList2[index2]
				(thispositive, thisnegative) = self.differences[(thispiece1, thispiece2)]
				(otherpositive, othernegative) = other.differences[(otherpiece1, otherpiece2)]
				self.differences[(thispiece1, thispiece2)] = DifferenceOfDifference((thispositive, thisnegative), (otherpositive, othernegative), DiffType)

		# get rid of rows corresponding to unmatched affixes
		affixlistcopy = list(self.affixes)
		for affix1 in affixlistcopy:
			if not affix1 in alignedAffixList1:
				for affix2 in other.affixes:
					if (affix1, affix2) in self.differences:
						del self.differences[(affix1, affix2)]
				self.affixes.remove(affix1)
		for affix in self.affixes:
			self.changeAffixLabel(affix, str(affix + ":" + counterpart[affix]))
		return

	def minus_aligned(self, other, DiffType):
		for index1 in range(len(self.affixes)):
			for index2 in range(len(other.affixes)):
				thispiece1 = self.affixes[index1]
				thispiece2 = self.affixes[index2]
				otherpiece1 = other.affixes[index1]
				otherpiece2 = other.affixes[index2]
				(thispositive, thisnegative) = self.indexed_differences[(index1, index2)]
				(otherpositive, othernegative) = other.indexed_differences[(index1, index2)]
				self.indexed_differences[(index1, index2)] = DifferenceOfDifference((thispositive, thisnegative),
																					(otherpositive, othernegative),
																					DiffType)
				# put this back in: taken out for unicode, i don't know why
		for n in range(len(self.affixes)):
			self.changeIndexedAffixLabel(n, str(self.affixes[n] + ":" + other.affixes[n]))

		return


# --------------------------------------------------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------#
# def Expansion(sig,stem):
#	wordset = set()
#	affixlist = sig.split('-')
#	for affix in affixlist:
#		if affix == 'NULL':
#			affix = ''
#		wordset.add(stem + affix)
#	return wordset
# ---------------------------------------------------------#
def makesignaturefrom2words_suffixes(a, b):
	stemlength = 0
	howfar = len(a)
	if len(b) < howfar:
		howfar = len(b)
	for i in range(howfar):
		if a[i] == b[i]:
			stemlength = i + 1
		else:
			break;
	affix1 = a[stemlength:]
	affix2 = b[stemlength:]
	if len(affix1) == 0:
		affix1 = "NULL"
	if len(affix2) == 0:
		affix2 = "NULL"
	return (affix1, affix2)


# ---------------------------------------------------------#
def sortfunc(x, y):
	return cmp(x[1], y[1])


# ---------------------------------------------------------#
def sortfunc1(x, y):
	return cmp(x[1], len(y[1]))


# ---------------------------------------------------------#
def subsignature(sig1, sig2):
	sigset1 = set(sig1.split('-'))
	sigset2 = set(sig2.split('-'))
	if sigset1 <= sigset2:  # subset
		return True
	return False


# ---------------------------------------------------------#
def RemoveNULL(list1):
	for item in list1:
		if item == "NULL":
			item = ""
	return list1


# ---------------------------------------------------------#
def StringDifference(str1, str2):
	if str1 == "NULL":
		str1 = ""
	if str2 == "NULL":
		str2 = ""
	list1 = list(str1)
	list2 = list(str2)
	list1.sort()
	list2.sort()
	m = 0
	n = 0
	overlap = 0
	difference = 0
	while (True):
		if m == len(str1) and n == len(str2):
			return (overlap, difference)
		if m == len(str1):
			difference += len(str2) - n
			return (overlap, difference)
		if n == len(str2):
			difference += len(str1) - m
			return (overlap, difference)

		if list1[m] == list2[n]:
			overlap += 1
			m += 1
			n += 1
		elif list1[m] < list2[n]:
			m += 1
			difference += 1
		elif list2[n] < list1[m]:
			n += 1
			difference += 1


# ----------------------------------------------------------------------------------------------------------------------------#
def SignatureDifference(sig1, sig2,outfile):  # this finds the best alignments between affixes of a signature, and also gives a measure of the similarity.
	list1 = list(sig1.split('-'))
	list1.sort()
	list2 = list(sig2.split('-'))
	list2.sort()
	reversedFlag = False
	if (len(list1) > len(list2)):
		temp = list1
		list1 = list2
		list2 = temp  # now list2 is the longer one, if they differ in lengthpart1[0], part1[1
		reversedFlag = True
	differences = {}
	list3 = []
	Alignments = []
	AlignedList1 = []
	AlignedList2 = []

	print >> outfile, "---------------------------------------\n", sig1, sig2
	print >> outfile, "---------------------------------------\n"
	for m in list1:
		differences[m] = {}
		# print >>outfile, '%8s ' % m, ":",
		for n in list2:
			o, d = StringDifference(m, n)
			differences[m][n] = o - d
			# print >>outfile, '%2s %2d;' % (n, o-d),
			# print >>outfile

	GoodAlignmentCount = 0
	TotalScore = 0
	for loopno in range(len(list1)):
		# print >>outfile, "-----------------------------\n"
		# print >>outfile, "loop no: ", loopno
		# for m in differences.keys():
		# print >>outfile, '%8s : ' % (m),
		# for n in differences[m].keys():
		# print >>outfile, '%2s %2d;' % (n, differences[m][n]),
		# print >>outfile
		# print >>outfile

		list3 = []
		for m in differences.keys():
			for n in differences[m].keys():
				list3.append(differences[m][n])
		list3.sort(reverse=True)

		bestvalue = list3[0]
		if bestvalue >= 0:
			GoodAlignmentCount += 1
		breakflag = False
		for m in differences.keys():
			for n in differences[m].keys():
				if differences[m][n] == bestvalue:
					winner = (m, n)
					# print >>outfile, "winner:", m, n, "closeness: ", bestvalue
					breakflag = True
					break
			if breakflag:
				break;
		AlignedList1.append(m)
		AlignedList2.append(n)

		Alignments.append((m, n, bestvalue))
		TotalScore += bestvalue
		del differences[winner[0]]
		for p in differences.keys():
			del differences[p][winner[1]]
	# print >>outfile, "Final affix alignments: ", sig1, sig2
	# for item in Alignments:
	#	print >>outfile, "\t%7s %7s %7d" % ( item[0], item[1], item[2] )
	# For scoring: we count a pairing as OK if its alignment is non-negative, and we give extra credit if there are more than 2 pairings
	if GoodAlignmentCount > 2:
		TotalScore += GoodAlignmentCount - 2
	if reversedFlag:
		return (AlignedList2, AlignedList1)
	return (TotalScore, AlignedList1, AlignedList2)


# ----------------------------------------------------------------------------------------------------------------------------#
def FindBestAlignment(list1, list2):  # this is very similar to SignatureDifference...
	AlignedList1 = []
	AlignedList2 = []
	reversedFlag = False
	if (len(list1) > len(list2)):
		temp = list1
		list1 = list2
		list2 = temp  # now list2 is the longer one, if they differ in length
		reversedFlag = True
	differences = {}
	list3 = []
	Alignments = []
	# print >>outfile,  "---------------------------------------\n"
	# print >>outfile, "---------------------------------------\n",list1, list2, "** Find Best Alignment **\n"
	for m in list1:
		differences[m] = {}
		for n in list2:
			o, d = StringDifference(m, n)
			differences[m][n] = o - d

	GoodAlignmentCount = 0
	TotalScore = 0
	for loopno in range(len(list1)):
		list3 = []
		for m in differences.keys():
			for n in differences[m].keys():
				list3.append(differences[m][n])
		list3.sort(reverse=True)

		bestvalue = list3[0]
		if bestvalue >= 0:
			GoodAlignmentCount += 1
		breakflag = False
		for m in differences.keys():
			for n in differences[m].keys():
				if differences[m][n] == bestvalue:
					winner = (m, n)
					# print >>outfile, "winner: %8s %8s closeness: %2d" %( m, n, bestvalue)
					breakflag = True
					break
			if breakflag:
				break;
		AlignedList1.append(m)
		AlignedList2.append(n)
		del differences[winner[0]]
		for p in differences.keys():
			del differences[p][winner[1]]

	if reversedFlag:
		return (AlignedList2, AlignedList1)
	return (AlignedList1, AlignedList2)



# ----------------------------------------------------------------------------------------------------------------------------#
def RemoveRareSignatures(Lexicon, encoding, FindSuffixesFlag, outfile):
	# ----------------------------------------------------------------------------------------------------------------------------#
	#  we check to see which words currently are associated with more than one signature.
	# For those words that are, we choose the signature with the largest number of stems.

	MinStemCount = Lexicon.MinimumStemsInaSignature

	RobustnessCutoff = 1000  # signatures with this robustness are considered secure, and factorable.
	for sig in Lexicon.SignatureToStems:
		if Robustness(sig) < RobustnessCutoff:
			continue


# ----------------------------------------------------------------------------------------------------------------------------#
def SliceSignatures(Lexicon, encoding, FindSuffixesFlag, outfile):
	# ----------------------------------------------------------------------------------------------------------------------------#
	# we look to see if highly robust signatures like NULL.ly can be used to simplify
	# other longer signatures, like NULL.al.ally, making it NULL.al(ly), feeding NULL.ly
	# This is easiest to detect with the signatures, but easiest to implement the changes in the FSA.


	RobustnessCutoff = 1000  # signatures with this robustness are considered secure, and factorable.
	NumberOfStemsThreshold = 30
	for sig in Lexicon.SignatureToStems:
		if len(Lexicon.SignatureToStems[sig]) < NumberOfStemsThreshold:
			continue
		print >> outfile, "sig: ", sig
		for stem in Lexicon.SignatureToStems[sig]:
			# construct its words from its stems
			# those words should all share the same signatures
			# other than sig, how many are there?
			wordlist = list()
			# print "stem: ", stem,
			for affix in sig:
				if affix == "NULL":
					affix = ""
				word = stem + affix
				wordlist.append(word)
			# print wordlist,
			firstword = wordlist.pop()
			signatureset = Lexicon.WordToSig[firstword]
			# print firstword, signatureset
			for word in wordlist:
				this_signatureset = Lexicon.WordToSig[word]
				# if this_signatureset != signatureset:
				print >> outfile, '{:20}{:70}{:20}{:35}'.format(firstword, signatureset, word, this_signatureset)





				# ----------------------------------------------------------------------------------------------------------------------------#
	return


# ----------------------------------------------------------------------------------------------------------------------------#
def printWordsToSigTransforms(SignatureToStems, WordToSig, StemCounts, outfile_SigTransforms, g_encoding,
							  FindSuffixesFlag):
	sigtransforms = dict()
	for sig in SignatureToStems:
		affixes = list(sig)
		affixes.sort()
		sig_string = "-".join(affixes)
		stems = SignatureToStems[sig]
		for stem in stems:
			for affix in sig:
				if affix == "NULL":
					word = stem
				else:
					word = stem + affix
				transform = sig_string + "_" + affix
				if not word in sigtransforms:
					sigtransforms[word] = list()
				sigtransforms[word].append(transform)
	wordlist = sigtransforms.keys()
	wordlist.sort()
	for word in wordlist:
		print >> outfile_SigTransforms, '{:15}'.format(word),
		for sig in sigtransforms[word]:
			print >> outfile_SigTransforms, '{:35}'.format(sig),
		print >> outfile_SigTransforms

	# print >>outfile, '%18s' %self.affixlabels[affix],
	# ----------------------------------------------------------------------------------------------------------------------------#
	return


# ----------------------------------------------------------------------------------------------------------------------------#


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------



 





# ----------------------------------------------------------------------------------------------------------------------------#
def ShiftFinalLetter(StemToWord, StemCounts, stemlist, CommonLastLetter, sig, FindSuffixesFlag, outfile):
	# ----------------------------------------------------------------------------------------------------------------------------#
	# print >>outfile, "Shift final letter: ", CommonLastLetter
	newsig = ''
	affixlist = sig.split('-')
	newaffixlist = []
	listOfAffectedWords = list()
	for affix in affixlist:
		if affix == "NULL":
			newaffixlist.append(CommonLastLetter)
		else:
			if FindSuffixesFlag:
				newaffixlist.append(CommonLastLetter + affix)
			else:
				newaffixlist.append(affix + CommonLastLetter)  # really commonfirstletter...change name of variable
	newsig = makesignature(newaffixlist)
	# print >>outfile, "old sig", sig, "new sig", newsig
	for stem in stemlist:
		# print >>outfile, "shifting this stem: ", stem
		if FindSuffixesFlag:
			if not stem[-1] == CommonLastLetter:
				# print >>outfile, "\tNo good fit: ", stem
				continue
		else:
			if not stem[0] == CommonLastLetter:
				continue
		if FindSuffixesFlag:
			newstem = stem[:-1]
		else:
			newstem = stem[1:]
		if not newstem in StemCounts.keys():
			StemCounts[newstem] = StemCounts[stem]
		else:
			StemCounts[newstem] += StemCounts[stem]
		del StemCounts[stem]

		if not newstem in StemToWord.keys():
			StemToWord[newstem] = set()

		listOfAffectedWords = StemToWord[stem].copy()
		for word in listOfAffectedWords:
			StemToWord[stem].remove(word)
			StemToWord[newstem].add(word)
			# print >>outfile, "We're adding" , newstem , "as the stem of ", word
			if not word in StemToWord[newstem]:
				StemToWord[newstem].add(word)
		if len(StemToWord[stem]) == 0:
			# print >>outfile, "we're deleting this stemtoword stem, no longer used", stem
			del StemToWord[stem]

			# ----------------------------------------------------------------------------------------------------------------------------#
	return (StemToWord, newsig)


# ----------------------------------------------------------------------------------------------------------------------------#











# ----------------------------------------------------------------------------------------------------------------------------#
def findmaximalrobustsuffix(wordlist):
	# ----------------------------------------------------------------------------------------------------------------------------#
	bestchunk = ""
	bestwidth = 0
	bestlength = 0
	bestrobustness = 0
	maximalchunksize = 4  # should be 3 or 4 ***********************************
	threshold = 50
	bestsize = 0
	# sort by end of words:
	templist = []
	for word in wordlist:
		wordrev = word[::-1]
		templist.append(wordrev)
	templist.sort()
	wordlist = []
	for wordrev in templist:
		word = wordrev[::-1]
		wordlist.append(word)
	for width in range(1, maximalchunksize + 1):  # width is the size (in letters) of the suffix being considered
		numberofoccurrences = 0
		here = 0
		while (here < len(wordlist) - 1):
			numberofoccurrences = 0
			chunk = wordlist[here][-1 * width:]
			for there in range(here + 1, len(wordlist)):
				if (not wordlist[there][-1 * width:] == chunk) or (there == len(wordlist) - 1):
					numberofoccurrences = there - here
					currentrobustness = numberofoccurrences * width
					if currentrobustness > bestrobustness:
						bestrobustness = currentrobustness
						bestchunk = chunk
						bestwidth = width
						bestnumberofoccurrences = numberofoccurrences
						count = numberofoccurrences
					break
			here = there
	permittedexceptions = 2
	if bestwidth == 1:
		if bestnumberofoccurrences > 5 and bestnumberofoccurrences >= len(
				wordlist) - permittedexceptions and bestrobustness > threshold:
			return (bestchunk, bestrobustness)
	if bestrobustness > threshold:
		return (bestchunk, bestrobustness)
	# ----------------------------------------------------------------------------------------------------------------------------#
	return ('', 0)


# ----------------------------------------------------------------------------------------------------------------------------#


# ----------------------------------------------------------------------------------------------------------------------------#
# --------------------------------------------------------------------##
#		Start, end latex doc
# --------------------------------------------------------------------##
def StartLatexDoc(outfile):
	header0 = "\documentclass[10pt]{article} \n\\usepackage{booktabs} \n\\usepackage{geometry} \n\\geometry{verbose,letterpaper,lmargin=0.5in,rmargin=0.5in,tmargin=1in,bmargin=1in} \n\\begin{document}  \n"
	print >> outfile, header0


def EndLatexDoc(outfile):
	footer = "\\end{document}"
	print >> outfile, footer
	outfile.close()


# --------------------------------------------------------------------##
#		Make latex table
# --------------------------------------------------------------------##
def MakeLatexFile(outfile, datalines):
	tablelines = []
	longestitem = 1
	numberofcolumns = 0
	for line in datalines:
		line = line.replace("NULL", "\\emptyset")
		line = line.replace(u"\u00FC", "\\\"{u}")
		line = line.replace(u"\u00F6", "\\\"{o}")
		items = line.split()
		if len(items) > numberofcolumns:
			numberofcolumns = len(items)
		tablelines.append(items)
		for piece in items:
			if len(piece) > longestitem:
				longestitem = len(piece)
		header1 = "\\begin{centering}\n"
	header2 = "\\begin{tabular}{"
	header3 = "\\toprule "
	footer1 = "\\end{tabular}"
	footer2 = "\\end{centering}\n"
	print >> outfile, header1
	print >> outfile, header2, 'l' * numberofcolumns, "}", header3

	for m in range(len(tablelines)):
		line = tablelines[m]
		for n in range(len(line)):
			field = line[n]
			if field == "@":
				print >> outfile, " " * longestitem,
			elif len(field.split(":")) == 2:
				fraction = field.split(":")
				field = "$\\frac{" + fraction[0] + "}{" + fraction[1] + "}$"
				print >> outfile, field + " " * (longestitem - len(field)),
			else:
				print >> outfile, field + " " * (longestitem - len(field)),
			if n < len(line) - 1:
				print >> outfile, "&",

		if m == 0:
			print >> outfile, "\\\\ \\midrule"
		else:
			print >> outfile, "\\\\"
	print >> outfile, "\\bottomrule", "\n"
	print >> outfile, footer1
	print >> outfile, footer2
