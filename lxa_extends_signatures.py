
#----------------------------------------------------------------------------------------------------------------------------#
def Extends(sig1, sig2, type = "suffix"):
#----------------------------------------------------------------------------------------------------------------------------#
	"""
	This function determines if sig2 extends sig1, meaning that there is a 1 to 1 association 
	between affixes in the two signatures in which the affix in sig1 is a prefix of the corresponding affix in sig2.
	We assume at this time that both signatures are "almost suffix-free", meaning that no affix is a suffix of another affix
	(when the affixes are suffixes), with the possible exception that NULL is a possible suffix (and it is a suffix of all
	other affixes, of course). 
	"""


 	AffixList1 = list()
	AffixList2 = list()
	affixes1= sig1.split("-")
	affixes2 = sig2.split("-")
	if len(affixes1) != len(affixes2):
		return False
 	NullAffixFound = False
	UnmatchedAffix_in_Affixes_1 = list()
	if type == "suffix":
	# We iterate through affixes1-list:
		for affix1 in affixes1:
			MatchedSuffixFound = False
			#if affix1 is NULL, we just hold on to that fact until the very end of the matching
			if affix1 == "NULL":
				NullAffixFound = True
				continue
			for affixno2 in range(len(affixes2)):
				affix2 = affixes2[affixno2]
				if len(affix1) > len(affix2):
					#If this is so, affix2 can't *continue* affix1
					continue
				if affix1 == affix2[-1*len(affix1):]:
					# a match is found, so we add each affix to a list, and delete the affix from AffixList2
					MatchedSuffixFound = True
					AffixList1.append(affix1)
					AffixList2.append(affix2)
					del affixes2[affixno2]	
					break
 			if MatchedSuffixFound == False:
				# Here we have looked at all the affixes in AffixList2, and found no alignment could be made:
				UnmatchedAffix_in_Affixes_1.append(affix1)			 
		if len(affixes2) == 1 and NullAffixFound:
			AffixList1.append("NULL") 
			AffixList2.append(affixes2[0])
		else:
			return False;
		print >>outfile, "Extends", AffixList1, AffixList2
		return (AffixList1, AffixList2);			
				
		


