import math
import sys

from printing_to_files import *
from signaturefunctions import *
from ClassLexicon import *
from ClassLexicon import Signature



	
    ## -------                                                      ------- #
    ##              Central signature computation                   ------- #
    ## -------                                                      ------- #

    # ----------------------------------------------------------------------------------------------------------------------------#
def MakeSignatures_Crab(Lexicon, FindSuffixesFlag,   verboseflag = False):
        # ----------------------------------------------------------------------------------------------------------------------------#
        lxalogfile                      = open(Lexicon.outfolder + "lxalog.txt", "w")
        outfile_Rebalancing_Signatures  = open(Lexicon.outfolder + "Rebalancing_Signatures.txt", "w")
        outfile_subsignatures           = open(Lexicon.outfolder + "Subsignatures.txt", "w")
        MinimumStemLength               = Lexicon.MinimumStemLength
        verboseflag                     = True
        formatstring1 = "  {:50s}{:>10,}"
        formatstring2 = "  {:50s}"
        formatstring3 = "{:40s}{:10,d}"
        if verboseflag:
            print formatstring2.format("The MakeSignatures function")

        # Protostems are candidate stems made during the algorithm, but not kept afterwards.
        Protostems = dict()
        Lexicon.NumberOfAnalyzedWords = 0
        Lexicon.LettersInAnalyzedWords = 0
        Lexicon.NumberOfUnanalyzedWords = 0
        Lexicon.LettersInUnanalyzedWords = 0

        AnalyzedWords = dict()

        Lexicon.TotalRobustnessInSignatures = 0
        Lexicon.TotalLetterCostOfAffixesInSignatures = 0
        Lexicon.TotalLetterCostOfAffixesInSignatures = 0
        if FindSuffixesFlag:
            Affixes = Lexicon.Suffixes
        else:
            Affixes = Lexicon.Prefixes

        # 1 --------------------------------------------------------------------

        Step = 1
        maximumstemlength = 100
	minimum_stem_length = 2
        if verboseflag:
            print formatstring1.format("1a. Finding protostems. Maximum stem length: ", minimum_stem_length)
        FindProtostems_crab(Lexicon,  FindSuffixesFlag, verboseflag, Step, maximumstemlength, minimum_stem_length)
        if verboseflag:
            print formatstring1.format("1b. Finished finding proto-stems.", len(Protostems))



        # 2 --------------------------------------------------------------------
        Step += 1

	CreateStemAffixPairs (Lexicon, FindSuffixesFlag,Step,verboseflag )



        # 3 --------------------------------------------------------------------

	AssignAffixesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag)

        if verboseflag:
            print  "     Finished finding affixes for protostems."

        # --------------------------------------------------------------------
        # 4  Assign signatures to each stem.
        MinimumStemCountInSignature = 2
        AssignSignaturesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag, MinimumStemCountInSignature, Step=-1)



 
	# 5 Pull single letter from edge of stems
	print "  4. Shifting a single letter from stem to affix."
	while True:
		number_of_changes = pull_single_letter_from_edge_of_stems_crab(Lexicon,FindSuffixesFlag)
		print "  5. Shift a letter from stem to affix. Number of changes: ", str(number_of_changes) + "."
		if number_of_changes == 0:
			print "     Recompute signatures with these changes."
			break
                print "     Go through the signatures again."
		AssignAffixesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag, "inside letter-shift")
		MinimumStemCountInSignature = 2
		AssignSignaturesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag, MinimumStemCountInSignature, Step=-1)
		

        if verboseflag:
            print  formatstring1.format("6. Finished first pass of finding stems, affixes, and signatures.",
                                    len(Lexicon.SignatureStringsToStems))
        Lexicon.Compute_Lexicon_Size()


                #---------------------------------------------------------------------------------------------------------------------#

def FindProtostems_crab(Lexicon, FindSuffixesFlag,verboseflag,Step, maximum_stem_length=-1, minimum_stem_length = 2):
        # A "maximum_stem_length" is included here so that we can use this function to explore
        # for stems shorter than the minimum that was assumed on an earlier iteration.
        wordlist = Lexicon.WordCounts.keys()
        wordlist.sort()
        minimum_stem_length = Lexicon.MinimumStemLength
	Protostems = Lexicon.Protostems
        if verboseflag:
            filename = "1_FindProtoStems.txt"
            headerlist = [ "Find proto-stems"]
            contentlist = list()
            formatstring = "{0:20s} Comparison span: {1:4s} {2:20s} {3:20s}."

            formatstring2 = "{0:15s} {1:15s}"
            formatstring1 = "{0:20s} {1:5n} {2:20s}{3:32s}"
        previousword = ""

        if FindSuffixesFlag:
            for i in range(len(wordlist)):
                word = wordlist[i]
                differencefoundflag = False
                if previousword == "":  # only on first iteration
                    previousword = word
                    continue
                begin=minimum_stem_length
                if maximum_stem_length > 0:
                    end = min(len(word), len(previousword), maximum_stem_length)
                else:
                    end = min(len(word), len(previousword))
                for j in range(end):
                    if word[j] != previousword[j]:  # will a stem be found in the very first word?
                        stem = word[:j]
                        differencefoundflag = True
                        if len(stem) >= minimum_stem_length:
                            Lexicon.WordBiographies[word].append(str(Step) + " Found stem " + stem)
                            if stem not in Protostems:
                                Protostems[stem] = 1
                                if verboseflag:
                                    reportline = formatstring1.format(word,  end, stem, "New stem." + str(j))
                                    contentlist.append(reportline)
                            else:
                                if verboseflag:
                                    reportline = formatstring1.format(word,   end, stem, "Known stem."+ str(j))
                                Protostems[stem] += 1
                        else:
                            if verboseflag:
                                reportline = formatstring1.format(word,  end, stem, "Too small.")
                                contentlist.append(reportline)
                        previousword = word
                        break
                if differencefoundflag:
                    continue
                else:  # there no were differences between this word and the preceding word, on the length that they both shared.

                    if (len(word)) >= len(previousword):
                        if len(previousword) >= minimum_stem_length:
                            if (previousword not in Lexicon.Protostems):
                                if verboseflag:
                                    reportline = formatstring1.format(word,   end, previousword, "New stem.")
                                    contentlist.append(reportline)
                                Protostems[previousword] = 1
                                Lexicon.WordBiographies[previousword].append(str(Step) + " This word is a stem.")
                            else:
                                Protostems[previousword] += 1
                                if verboseflag:
                                   reportline = formatstring1.format(word,   end, stem, "Known stem.")
                                   contentlist.append(reportline)
                        else:
                            if verboseflag:
                                reportline = formatstring1.format(word,   end, "", "Too short." + previousword )
                                contentlist.append(reportline)
                    previousword = word

        else:
            ReversedList = list()
            TempList = list()
            for word in wordlist:
                key = word[::-1]
                TempList.append(key)
            TempList.sort()
            for word in TempList:
                ReversedList.append(word[::-1])
            for i in range(len(ReversedList)):
                word = ReversedList[i]
                differencefoundflag = False
                if previousword == "":  # only on first iteration
                    previousword = word
                    continue
                span = min(len(word), len(previousword))
                for i in range(1, span, ):
                    if word[-1 * i] != previousword[-1 * i]:
                        differencefoundflag = True
                        stem = word[-1 * i + 1:]
                        if len(stem) >= minimum_stem_length:
			    Lexicon.WordBiographies[word].append(str(Step) + " Found stem " + stem)
                            if stem not in Protostems:
                                Protostems[stem] = 1
                                if verboseflag:
                                    reportline = formatstring1.format(word,  0, stem, "New stem." + str(i))
                                    contentlist.append(reportline)
                            else:
                                if verboseflag:
                                    reportline = formatstring1.format(word,   0, stem, "Known stem."+ str(i))
                                Protostems[stem] += 1
                        else:
                            if verboseflag:
                                reportline = formatstring1.format(word,  0, stem, "Too small.")
                                contentlist.append(reportline)
                            if stem not in Protostems:
                                Protostems[stem] = 1
                            else:
                                Protostems[stem] += 1
                        previousword = word
                        break
                if differencefoundflag:
                    continue
                if len(previousword) > i + 1:
                    previousword = word
                    continue
                if (len(word)) >= i:
                    if len(previousword) >= minimum_stem_length:
                        if (previousword not in Protostems):
                            Protostems[previousword] = 1
                        else:
                            Protostems[previousword] += 1
                previousword = word



        if verboseflag:
            print_report(filename, headerlist, contentlist)
	    Lexicon.Log.append("Minimum stem length:" + str( minimum_stem_length))
	    Lexicon.Log.append("Number of proto-stems:" + str( len(Protostems)))

                # ----------------------------------------------------------------------------------------------------------------------------#

def CreateStemAffixPairs(Lexicon,  FindSuffixesFlag,Step, verboseflag = False):
        # This function creates the pairs in Parses. Most words have multiple appearances.
        # Step = 2.


        if verboseflag:
            print "  2. Assign affixes and words to stems."
            filename = "2_All_initial_word_splits.txt"
            headerlist = [ "Assign affixes and words to stems"]
            contentlist = list()
            linelist = list()
            formatstring = "{0:20s}   {1:20s} {2:10s} {3:20s}"
        wordlist = deepcopy(Lexicon.WordCounts.keys())
        wordlist.sort()
        MinimumStemLength = Lexicon.MinimumStemLength
        MaximumAffixLength = Lexicon.MaximumAffixLength
        column_no = 0
        NumberOfColumns = 8
        formatstring4 = "{0:15s} {1:15s} {2:10} {3:12}"

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
                for i in range(len(word), MinimumStemLength - 1, -1):
                    if FindSuffixesFlag:
                        stem = word[:i]
                    else:
                        stem = word[-1 * i:]
                    if stem in Lexicon.Protostems:
                        if FindSuffixesFlag:
                            suffix = word[i:]
                            if len(suffix) == 0:
                                continue
			    broken_word = stem+" "+suffix
			    if broken_word not in Lexicon.ParseDict:
			    	Lexicon.ParseDict[broken_word]=1
				Lexicon.Parses.append((stem, suffix))
                            if stem in Lexicon.WordCounts:
				broken_word = stem + " NULL"
				if broken_word not in Lexicon.ParseDict:
	                            Lexicon.Parses.append((stem, "NULL"))
				    Lexicon.ParseDict[broken_word] = 1
                            if len(suffix) <= MaximumAffixLength:
                                Lexicon.WordBiographies[word].append(str(Step) + " The split "+stem+ "=" + suffix + " is good.")
                                if verboseflag:
                                        reportline = formatstring.format(word,stem,suffix, " suffix is good.")
                                        contentlist.append(reportline)
                            if len(suffix) > MaximumAffixLength:
                                # NB if we block the suffix "atives" from "represent" because "atives"is too long,
                                # then we don't get the right analysis for  "representing" (where the suffix is just
                                # 3 letters long). So we need to accept longer suffixes, and block them later (or re-analyze them).
                                Lexicon.WordBiographies[word].append(str(Step) + " The split "+stem+ " / " + suffix + " is suspicious; suffix too long.")
                                if verboseflag:
                                    reportline = formatstring.format(word,stem,suffix, "suffix too long.")
                                    contentlist.append(reportline)
			#-----------------------------------------------------------------------------------------
			# prefixing
			else:
			    ii = len(word) - i
			    prefix = word[:ii]
 			    if len(prefix) == 0:
				continue
			    broken_word = prefix + " " + stem
			    if broken_word not in Lexicon.ParseDict:
 				Lexicon.Parses.append((prefix,stem)) 
				Lexicon.ParseDict[broken_word] = 1
                            if stem in Lexicon.WordCounts:
				broken_word = stem + " " + "NULL"
				if broken_word not in Lexicon.ParseDict:
				    Lexicon.ParseDict[broken_word]=1
	                            Lexicon.Parses.append(("NULL", stem))
                            if len(prefix) <= MaximumAffixLength:
                                Lexicon.WordBiographies[word].append(str(Step) + " The split "+prefix+ "=" + stem + " is good.")
                                if verboseflag:
                                        reportline = formatstring.format(word, prefix, stem,  "prefix is good.")
                                        contentlist.append(reportline)
                            if len(prefix) > MaximumAffixLength:
                                # NB if we block the suffix "atives" from "represent" because "atives"is too long,
                                # then we don't get the right analysis for  "representing" (where the suffix is just
                                # 3 letters long). So we need to accept longer suffixes, and block them later (or re-analyze them).

                                Lexicon.WordBiographies[word].append(str(Step) + " The split "+ prefix+ " / " + stem  + " is suspicious; affix too long.")
                                if verboseflag:
                                    reportline = formatstring.format(word,prefix, stem, "affix too long.")
                                    contentlist.append(reportline)

	Lexicon.Log.append("Maximum affix length: " + str(MaximumAffixLength))
        Lexicon.Log.append("Minimum stem length: "  + str(MinimumStemLength))

        if verboseflag:
                print_report(filename, headerlist, contentlist)

        Step += 1
        if verboseflag:

            filename = "3_parse_pairs.txt"
            headerlist = [ "List of parse pairs"]
            contentlist = list()
            linelist = list()
            formatstring = "{0:20s}   {1:20s} {2:10s} {3:20s}"
            templist=list()
            print_report(filename, headerlist, contentlist)
	    affix =  ""
            for item in Lexicon.ParseDict: #Parses:
                if FindSuffixesFlag:
		    items = item.split()
                    stem = items[0]
                    affix = items[1]
                    templist.append (stem +' ' + affix )
                    if affix == "NULL":
                         word = stem
                    else:
                        word = stem + affix
                    Lexicon.WordBiographies[word].append(str(Step) + " "+ stem + "=" + affix)
		else:
		    affix = item[0]
		    stem= item[1]
		    templist.append (affix + ' ' + stem)
		    if affix == "NULL":
			word = stem
		    else:
			word = affix + stem
                    Lexicon.WordBiographies[word].append(str(Step) +  " "+ affix +   "=" + stem)
            templist.sort()
            for item in templist:
                    contentlist.append(item)
            print_report(filename, headerlist, contentlist)

 # ----------------------------------------------------------------------------------------------------------------------------#

def AssignAffixesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag, Key=""):
        """ This assumes parse pairs in Lexicon.Parses, and  creates:
            Affixes
            StemToWord
            StemToAffix
            SignatureStringsToStems
            StemToSignature
            StemCorpusCounts
            WordToSig """


        Lexicon.StemCorpusCounts = dict()
        Lexicon.Affixes = dict()
        Lexicon.SignatureStringsToStems = dict()
        Lexicon.Signatures = dict()
        Lexicon.StemToSignature = dict()
        Lexicon.StemCorpusCounts = dict()
        Lexicon.StemToWord = dict()
        Lexicon.WordToSig = dict()
        Lexicon.StemToAffix = dict()
        Lexicon.Suffixes = dict()
        formatstring2 = "{0:15s} {1:15s}"
        formatstring3 = "\n{0:15s} {1:15s} {2:10s} "
        formatstring4 = "\n{0:15s} {1:15s} {2:10s} {3:20s}"


  # ----------------------- Collect each affix a stem has.
        if verboseflag:
                filename = "4_stems_and_their_affix_sets.txt"
                headerlist = [ "Link stems to the set of their affixes."]
                contentlist = list()

                formatstring = "{0:20s}  {1:15s} {2:20s}{3:10s}"
                formatstring1 = "{0:32s}"


        if verboseflag:
            print "  3. Assign affix sets to each stem.\n     Find affixes for each protostem."
        ParseList = list()
	if FindSuffixesFlag:
	    LexiconAffixes = Lexicon.Suffixes
	else:
	    LexiconAffixes = Lexicon.Prefixes


        if True:
            for item  in Lexicon.ParseDict:  #Parses:
		items = item.split()
		piece1=items[0]
		piece2 = items[1]
                ParseList.append((piece1,piece2))
		if FindSuffixesFlag:
			stem = piece1
			affix = piece2
			broken_word = stem + " " + affix
		else:
			stem=piece2
			affix = piece1
			broken_word = affix + " "+ stem
		Lexicon.ParseDict[broken_word] = 1


                if stem not in Lexicon.StemToWord:
                    Lexicon.StemToWord[stem] = dict()
                    Lexicon.StemToAffix[stem] = dict()
                if affix == "NULL":
                    word = stem
                else:
		    if FindSuffixesFlag:
                        word = stem + affix
		    else:
			word = affix + stem
		#word = remove_parentheses(word)
                Lexicon.StemToWord[stem][word] = 1
                Lexicon.StemToAffix[stem][affix] = 1
                if affix not in LexiconAffixes:
                    LexiconAffixes[affix] = 0
                LexiconAffixes[affix] += 1
                Lexicon.WordBiographies[word].append(Key + " This split:" + broken_word	)
            ParseList.sort(key=lambda (x,y) : x+" "+y)
            if verboseflag:
                    stemlist = Lexicon.StemToWord.keys()
                    stemlist.sort()
                    for stem in stemlist:
                        affixset = Lexicon.StemToAffix[stem].keys()
                        affixset.sort()
                        reportline = formatstring2.format(stem, "=".join(affixset) )
                        contentlist.append(reportline)
            if verboseflag:
                print_report(filename, headerlist, contentlist)
                stemlist = Lexicon.StemToWord.keys()
                stemlist.sort()
                for stem in stemlist:
                        affixset = Lexicon.StemToAffix[stem].keys()
                        affixset.sort()
                        reportline = formatstring2.format(stem, "=".join(affixset) )
                        contentlist.append(reportline)
                print_report(filename, headerlist, contentlist)

 # ----------------------------------------------------------------------------------------------------------------------------#

def AssignSignaturesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag, MinimumStemCountInSignature, Step=-1):

        """ This assumes parse pairs in Lexicon.Parses, and  creates:
            Affixes
            StemToWord
            StemToAffix
            SignatureStringsToStems
            StemToSignature
            StemCorpusCounts
            WordToSig 
	    Robustness """

        Lexicon.StemCorpusCounts = dict()
        Lexicon.Affixes = dict()
        Lexicon.StemCorpusCounts = dict()
        formatstring2 = "{0:15s} {1:15s}"
        formatstring3 = "\n{0:15s} {1:15s} {2:10s} "
        formatstring4 = "\n{0:15s} {1:15s} {2:10s} {3:20s}"


        Lexicon.StemToSignature.clear()
        Lexicon.WordToSig.clear()
        Lexicon.SignatureStringsToStems.clear()
        Lexicon.StemToWord.clear()
        Lexicon.Suffixes.clear()
        Lexicon.Signatures.clear()
        Lexicon.RawSignatures.clear()
	Lexicon.Robustness.clear()

        Step += 1
        if verboseflag:
                filename = "5_assigning_signatures.txt"
                headerlist = [ "5. Assign a single signature to each stem."]
                contentlist = list()

                formatstring  = "{0:20s}  {1:15s} {2:20s}{3:10s}"
                formatstring3 = "{0:20s}  {1:15s} {2:15s}"
                formatstring2 = "{0:20s}  {1:30s} "
                formatstring1 = "{0:20s}"

        stemlist = Lexicon.StemToAffix.keys()
        stemlist.sort()

        #   1. We determine which signatures have too few stems, typically only one stem.
        #   However, that condition is only imposed the first time through -- later,
        #   we consciously create signatures with only one stem.


        temporary_signature_dict=dict()
        if verboseflag:
                print "     Assign a  signature to each stem (occasionally two)."
        for stem in stemlist:
                signature_string = MakeSignatureStringFromAffixDict(Lexicon.StemToAffix[stem])
                if signature_string not in temporary_signature_dict:
                        temporary_signature_dict[signature_string] = 0
                temporary_signature_dict[signature_string] += 1

        temp_signatures_with_too_few_stems = list()
        for signature_string in temporary_signature_dict:
                if temporary_signature_dict[signature_string] < MinimumStemCountInSignature:
                        temp_signatures_with_too_few_stems.append(signature_string)


        # We consider each *stem*.
        for stem in stemlist:
                signature_list = Lexicon.StemToAffix[stem]
                signature_string=MakeSignatureStringFromAffixDict(signature_list)
                number_of_stems_this_sig = temporary_signature_dict[signature_string]
                #   2a. We ignore signatures with too few stems (typically only one):
                if number_of_stems_this_sig < MinimumStemCountInSignature:
                        if signature_string not in Lexicon.RawSignatures:
                                Lexicon.RawSignatures[signature_string]= list()
                        Lexicon.RawSignatures[signature_string].append(stem)
                        reportline = formatstring4.format(stem, signature_string,"Too few stems", str(temporary_signature_dict[signature_string]),  str(number_of_stems_this_sig), "should be  at least", MinimumStemCountInSignature  )
                        contentlist.append(reportline)
                        if (True):
                                for affix in Lexicon.StemToAffix[stem]:
                                        if affix == "NULL":
                                            thisword = stem
                                        else:
					    if FindSuffixesFlag:
	                                            thisword = stem + affix
					    else:
						    thisword = affix + stem
					thisword=remove_parentheses(thisword)
                                        Lexicon.WordBiographies[thisword].append("5. Too few stems in sig: " + signature_string +  " (minimum is " + str( MinimumStemCountInSignature) + ".)")
                                if signature_string not in Lexicon.SignatureBiographies:
                                        Lexicon.SignatureBiographies[signature_string] = list()
                                Lexicon.SignatureBiographies[signature_string].append("5. This signature marked as raw: too few stems.")
                        continue
                # 2b. We procede with this stem, knowing that it is in a more robust signature:
                reportline = formatstring4.format(stem, signature_string, "Enough stems in this signature", str(number_of_stems_this_sig) )
                contentlist.append(reportline)

                # 2c. Create a signature if it is not already in Lexicon.Signatures
                if signature_string not in Lexicon.Signatures:
                        this_signature = Signature(signature_string)

                Lexicon.Signatures[signature_string] = this_signature
                if signature_string not in Lexicon.SignatureStringsToStems:
                        Lexicon.SignatureStringsToStems[signature_string] = dict()
                Lexicon.SignatureStringsToStems[signature_string][stem] = 1
                # 2d. Add stem to Lexicon


                if stem not in Lexicon.StemToSignature:
                        Lexicon.StemToSignature[stem] = list()
                Lexicon.StemToSignature[stem].append(signature_string)   #change this to signature
                Lexicon.StemCorpusCounts[stem] = 0

                # 2e. Update  Signature biography.
                if signature_string not in Lexicon.SignatureBiographies:
                    Lexicon.SignatureBiographies[signature_string] = list()
                    Lexicon.SignatureBiographies[signature_string].append ("Created at first opportunity, in AssignSignaturesToEachStem.")

                # 2f. Establish the link between this stem and its words:
                for affix in signature_list:
                        if FindSuffixesFlag:
                                if affix not in Lexicon.Suffixes:
                                        Lexicon.Suffixes[affix] = 0
                                Lexicon.Suffixes[affix] += 1
                                if affix == "NULL":
                                        affix = ""
                                word = stem + affix        
                        else:
                                if affix not in Lexicon.Prefixes:
                                        Lexicon.Prefixes[affix] = 0
                                Lexicon.Prefixes[affix] += 1
                                if affix == "NULL":
                                        affix = ""
			        word = affix + stem
			word = remove_parentheses(word)
                        if word not in Lexicon.WordToSig:
                                Lexicon.WordToSig[word] = list()
                        Lexicon.WordToSig[word].append((stem,signature_string))
                        if stem not in Lexicon.StemToWord:
                                Lexicon.StemToWord[stem] = dict()
                        Lexicon.StemToWord[stem][word] = 1
                        Lexicon.StemCorpusCounts[stem] += Lexicon.WordCounts[word]
                        Lexicon.WordBiographies[word].append(str(Step) + " In signature " + signature_string)


                this_signature.add_stem(stem)
                this_signature.add_affix(deepcopy(Lexicon.StemToAffix[stem]))
                #if verboseflag:
                #        reportline=formatstring2.format(stem,signature_string)
                #        contentlist.append(reportline)

	for sig in Lexicon.SignatureStringsToStems:
	    Lexicon.Robustness[sig] = compute_robustness(Lexicon, sig)

	signaturelist = Lexicon.SignatureStringsToStems.keys()
	Lexicon.SignatureListSorted = sorted(signaturelist, key = lambda sig: len(Lexicon.SignatureStringsToStems[sig]), reverse=True)		

        temporary_signature_dict.clear()
        if verboseflag:
            print "     End of assigning a signature to each stem."
            print_report(filename, headerlist, contentlist)

	

        if verboseflag:
                print_report(filename, headerlist, contentlist)




# ----------------------------------------------------------------------------------------------------------------------------#
def FindGoodSignaturesInsideBad_crab(Lexicon,   FindSuffixesFlag, verboseflag, Step=0):
# NOTE! This needs to be updated to include Lexicon.Signatures
# ----------------------------------------------------------------------------------------------------------------------------#
        # 3  Find good signatures inside signatures that don't have enough stems to be their own signatures.
        # Lexicon.RawSignatures are those signatures with only a single stem, and therefore they are not
        # reliable. In many cases, a subsignature within them is valid, and we must find it.

        outfile_Subsignatures = open(Lexicon.outfolder + "subsignatures.txt", "w")
        if verboseflag:
            filename = "7_good_signatures_inside_bad.txt"
            headerlist = [ "Find good signatures inside bad ones."]
            contentlist = list()
            linelist = list()
            contentlist.append("Good signature              Bad signature")
        Transactions = list()

	# We will be recreating the signature structure on the basis of a new set of parse-pairs that
	# will be found here. Therefore we must delete the old set of parse-pairs, and replace them
        # with the set of parse-pairs that exactly describe the current signature structure.
	ReplaceParsePairsFromCurrentSignatureStructure_crab(Lexicon,FindSuffixesFlag )
	Minimum_Count_In_Signature_To_Serve_As_Exemplar = 25
	Good_Signature_Exemplars = list()  # signatures that we will look for inside bad signatures
	for signature in Lexicon.Signatures:
		if len(Lexicon.SignatureStringsToStems[signature]) > Minimum_Count_In_Signature_To_Serve_As_Exemplar:
			Good_Signature_Exemplars.append(signature)

        formatstring1 = "Bad: {0:20s} Corrected: {1:50s}"
        formatstring2 = "     {0:10s}={1:6s}     to {2:15s}"
        for sig_string in Lexicon.RawSignatures:
            sig_list = MakeSignatureListFromSignatureString(sig_string)
            good_sig_list = FindGoodSignatureListFromInsideAnother(sig_list, Good_Signature_Exemplars)
            good_sig_string = "=".join(good_sig_list)


            if len(good_sig_string) == 0:
                continue
            number_of_stems = len(Lexicon.RawSignatures[sig_string])
            if good_sig_string == sig_string:
                stem_count = len(Lexicon.RawSignatures[sig_string])
                Lexicon.SignatureBiographies[sig_string].append("Low count ("+ str(stem_count) +   " but OK because it is a composite sig.")
                continue;
            if (good_sig_list):
                Lexicon.SignatureBiographies[sig_string].append("Stem count: " + str(number_of_stems) + ". Removed and replaced by: "+ good_sig_string)
                if verboseflag:	
                    contentlist.append(formatstring1.format(sig_string,good_sig_string ))
                for stem in Lexicon.RawSignatures[sig_string]:
			
		    for affix in sig_list:
                    	if affix in good_sig_list:
		                if FindSuffixesFlag:
		                    good_parse = (stem, affix)
				    word = stem + affix
				    word = remove_parentheses
				    new_broken_word = stem + " " + affix
		                else:
		                    good_parse = (affix, stem)
				    word = affix + stem
				    word = remove_parentheses(word)
				    new_broken_word = affix + " "+ stem	
		                if new_broken_word not in Lexicon.Parses:
				    Lexicon.ParseDict[new_broken_word] = 1
  		                    Lexicon.Parses.append(good_parse)

		                if affix == 'NULL':
		                    word = stem
		                elif FindSuffixesFlag:
		                    word = stem+affix
				else:
				    word = affix + stem
				word = remove_parentheses(word) 
		                Lexicon.WordBiographies[word].append("6. good_sig_string: " +  good_sig_string )
		                if verboseflag:
		                    contentlist.append(formatstring2.format(stem, affix, good_sig_string))
			#else:
			    #if FindSuffixesFlag:
				#print "find good in bad, but this is bad", affix, "not in ", good_sig_list

        if verboseflag:
            print_report(filename, headerlist, contentlist)

        MinimumStemCountinSignature = 1
        AssignAffixesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag, Key="Good_in_bad")
        AssignSignaturesToEachStem_crab(Lexicon,FindSuffixesFlag,verboseflag,MinimumStemCountinSignature,Step)



# ----------------------------------------------------------------------------------------------------------------------------#
def	ReplaceParsePairsFromCurrentSignatureStructure_crab(Lexicon,FindSuffixesFlag=True):
# ----------------------------------------------------------------------------------------------------------------------------#
# The Lexicon.Parse pairs are the basic pieces out of which the whole signature structure is built. So in order to
# redo the signature structure, we just make sure the parses are correct, then we clear the signature structure
# and rebuild it, which is easy to do.

	Lexicon.Parses=list()
	Lexicon.ParseDict= dict()
        signatures= Lexicon.SignatureStringsToStems.keys()
	for sig in signatures:
                stems = Lexicon.SignatureStringsToStems[sig]
                affixes = sig.split("=")
                if FindSuffixesFlag:
                        for affix in affixes:
                                for stem in stems:
                                        Lexicon.Parses.append((stem,affix))
					Lexicon.ParseDict[stem + " " + affix]=1
				#broken_word = stem + " " + affix
                                #if affix == "NULL":
                                #        affix = ""
				#word = stem + affix
				#word = remove_parentheses (word)
				#if broken_word not in Lexicon.ParseDict:
				#    Lexicon.ParseDict[broken_word]=1
				
                else:
                        for affix in affixes:

                                for stem in stems:
                                        Lexicon.Parses.append((affix,stem))
				broken_word = affix + " "+ stem
                                if affix == "NULL":
                                        affix = ""
				word = affix + stem
				if word not in Lexicon.ParseDict:
				    Lexicon.ParseDict[word]=1
				 








# ----------------------------------------------------------------------------------------------------------------------------#
#def find_word_in_parse_pairs(Lexicon,this_stem,this_suffix):
# 	for i in range(len(Lexicon.Parses)):#
#	    if Lexicon.Parses[i][0] == this_stem and Lexicon.Parses[i][1]==this_suffix:
#		return i
#	return None

# ----------------------------------------------------------------------------------------------------------------------------#
def	pull_single_letter_from_edge_of_stems_crab(Lexicon,FindSuffixesFlag=True):
# ----------------------------------------------------------------------------------------------------------------------------#
	# This is accomplished by changing the ParsePairs, and then recomputing signatures.
	# If a signature contains NULL, we skip it.
	# When we "create" a new parse, there is a good chance that the parse already exists.
	# In that case, we do nothing!
	MinimumNumberOfStems = 5
	count_of_changes_made = 0
	for signature_string in Lexicon.Signatures:
	    if len(Lexicon.SignatureStringsToStems[signature_string]) < MinimumNumberOfStems:
		continue
	    if "NULL" in signature_string:
		continue
	    edge_letter=None
	    if FindSuffixesFlag:
	    	for this_stem in Lexicon.SignatureStringsToStems[signature_string].keys():
		    if FindSuffixesFlag:
			    if edge_letter == None:
				edge_letter = this_stem[-1]
			    else:
				if this_stem[-1] != edge_letter:
				   edge_letter = None
				   break
		    else:
			    if edge_letter == None:
				edge_letter = this_stem[0]
			    else:
				if this_stem[0] != edge_letter:
				    edge_letter = None
				    break
	        if edge_letter:
		    count_of_changes_made += 1
		    signature_list = signature_string.split("=")
	    	    for affix in signature_list:
			for stem in Lexicon.SignatureStringsToStems[signature_string]:
			    if FindSuffixesFlag:
				    broken_word_1 = stem + " " + affix
				    if affix == "NULL":
					word = stem
				    else:
					word = stem + affix
				    new_stem = stem[:-1]
				    if affix == "NULL":
					new_suffix = edge_letter
				    else:
				        new_suffix = edge_letter + affix
			    	    broken_word_2 = new_stem + " " + new_suffix
			    else: 
				    if affix == "NULL":
					word = stem
				    else:
					word = affix + stem
				    broken_word_1 = affix + " " + stem
				    new_stem = stem[1:]
				    if affix == "NULL":
					new_affix = edge_letter
				    else:
				        new_prefix = affix + edge_letter
			    	    broken_word_2 = new_prefix +   " " + new_stem
			    Lexicon.ParseDict[broken_word_2] = 1
			    del Lexicon.ParseDict[broken_word_1]
			    Lexicon.WordBiographies[word].append("Shift from " + broken_word_1 + " to " + broken_word_2)
					
	return count_of_changes_made

		 				
					
			    	    



