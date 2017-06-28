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
        FindProtostems_crab(Lexicon,  FindSuffixesFlag, verboseflag, Step, maximumstemlength, minimum_stem_length)
        if verboseflag:
            print formatstring1.format("1. Finished finding proto-stems.", len(Protostems))



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



        if verboseflag:
            print  formatstring1.format("5. Finished first pass of finding stems, affixes, and signatures.",
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

            print "  1. Finding protostems.", "Maximum stem length: ", maximum_stem_length
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
                                #print "1",  previousword, word, stem
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
			    #print "2", previousword
                        else:
                            Protostems[previousword] += 1
		            #print "3", previousword
                previousword = word



        if verboseflag:
            print_report(filename, headerlist, contentlist)


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

			#---------------------------------------------------------------------------------------
			# suffixing

                        if FindSuffixesFlag:
			    #print "SUFFIXING"
                            suffix = word[i:]
                            if len(suffix) == 0:
                                continue
 	                    Lexicon.Parses[(stem, suffix)] = 1
                            if stem in Lexicon.WordCounts:
                                Lexicon.Parses[(stem, "NULL")] = 1

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
			    Lexicon.Parses[(prefix,stem)] = 1
			    #print prefix, stem
                            if stem in Lexicon.WordCounts:
                                Lexicon.Parses[("NULL", stem)] = 1

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
            for item in Lexicon.Parses:
		#print item
                if FindSuffixesFlag:
                    stem = item[0]
                    affix = item[1]
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

def AssignAffixesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag, Step=-1):
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
            print "  4. Assign affix sets to each stem.\n     Find affixes for each protostem"
        ParseList = list()


        if FindSuffixesFlag:
            for stem,affix in Lexicon.Parses:
                ParseList.append((stem,affix))
            ParseList.sort(key=lambda (x,y) : x+" "+y)
            for stem,affix in ParseList:
                if stem not in Lexicon.StemToWord:
                    Lexicon.StemToWord[stem] = dict()
                    Lexicon.StemToAffix[stem] = dict()
                if affix == "NULL":
                    word = stem
                else:
                    word = stem + affix
                Lexicon.StemToWord[stem][word] = 1
                Lexicon.StemToAffix[stem][affix] = 1
                if affix not in Lexicon.Suffixes:
                    Lexicon.Suffixes[affix] = 0
                Lexicon.Suffixes[affix] += 1
                Lexicon.WordBiographies[word].append(str(Step) + " This split:" + stem + "=" + affix)
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
	else:   #prefixes...
            for affix, stem  in Lexicon.Parses:
                ParseList.append((affix,stem))
            ParseList.sort(key=lambda (x,y) : x +" "+y)
            for affix, stem  in ParseList:
                if stem not in Lexicon.StemToWord:
                    Lexicon.StemToWord[stem] = dict()
                    Lexicon.StemToAffix[stem] = dict()
                if affix == "NULL":
                    word = stem
                else:
                    word = affix + stem
                Lexicon.StemToWord[stem][word] = 1
                Lexicon.StemToAffix[stem][affix] = 1
                if affix not in Lexicon.Prefixes:
                    Lexicon.Prefixes[affix] = 0
                Lexicon.Prefixes[affix] += 1
                Lexicon.WordBiographies[word].append(str(Step) + " This split:" + affix + "=" + stem )
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

 # ----------------------------------------------------------------------------------------------------------------------------#

def AssignSignaturesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag, MinimumStemCountInSignature, Step=-1):



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
                #print signature_string
                number_of_stems_this_sig = temporary_signature_dict[signature_string]
                #   2a. We ignore signatures with two few stems (typically only one):
                if number_of_stems_this_sig < MinimumStemCountInSignature:
                        if signature_string not in Lexicon.RawSignatures:
                                Lexicon.RawSignatures[signature_string]= list()
                        Lexicon.RawSignatures[signature_string].append(stem)
                        reportline = formatstring4.format(stem, signature_string,"Too few stems", str(temporary_signature_dict[signature_string]),  str(number_of_stems_this_sig)  )
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
                                        Lexicon.WordBiographies[thisword].append("5. Too few stems in sig: " + signature_string)
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

        temporary_signature_dict.clear()
        if verboseflag:
            print "     End of assigning a signature to each stem."
            print_report(filename, headerlist, contentlist)

        if verboseflag:
                print_report(filename, headerlist, contentlist)





    # ----------------------------------------------------------------------------------------------------------------------------#
def RebalanceSignatureBreaks_crab(Lexicon, threshold, outfile, FindSuffixesFlag,verboseflag = True):
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
        SortedListOfSignatures = sorted(Lexicon.SignatureStringsToStems.items(), lambda x, y: cmp(len(x[1]), len(y[1])),
                                        reverse=True)
        maximumlengthofsignature = 0
        for (sig_string, wordlist) in SortedListOfSignatures:
            if len(sig_string) > maximumlengthofsignature:
                maximumlengthofsignature = len(sig_string)
        for (sig_string, wordlist) in SortedListOfSignatures:
            sig_list = MakeSignatureListFromSignatureString(sig_string)
            numberofstems = len(Lexicon.SignatureStringsToStems[sig_string])

            if numberofstems < MinimumNumberOfStemsInSignaturesCheckedForRebalancing:
                print >> outfile, "       Too few stems to shift material from suffixes", sig_string, numberofstems
                continue
            # print >>outfile, "{:20s} count: {:4d} ".format(sig_string,   numberofstems),
            shiftingchunk, shiftingchunkcount = TestForCommonEdge(Lexicon.SignatureStringsToStems[sig_string], outfile,
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
                    stems_to_change = list(Lexicon.SignatureStringsToStems[sig_string])
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
                                #print "612", stem, affix_t
                                del Lexicon.Parses[(stem, affix_t)]
                                newaffix = shiftingchunk + affix_t
                                Lexicon.Parses[(newstem, newaffix)] = 1
                                #print "615 {0:20s} {1:20s} {2:20s} {3:20s}".format(stem, affix, newstem,  newaffix )
                        else:
                            newstem = stem[chunklength:]
                            for affix in sig_list:
                                del Lexicon.Parses[(affix, stem)]
                                newaffix = affix + shiftingchunk
                                Lexicon.Parses[(newaffix, newstem)] = 1

        outfile.flush()
        print_report(filename, headerlist, contentlist)

        return count

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

        formatstring1 = "Bad: {0:20s} Corrected: {1:50s}"
        formatstring2 = "     {0:10s}={1:6s}     to {2:15s}"
        for sig_string in Lexicon.RawSignatures:
            sig_list = MakeSignatureListFromSignatureString(sig_string)
            good_sig_list = FindGoodSignatureListFromInsideAnother(sig_list, Lexicon.Signatures)
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
                    for affix in good_sig_list:
                        if FindSuffixesFlag:
                            good_parse = (stem, affix)
                        else:
                            good_parse = (affix, stem)
                        if good_parse not in Lexicon.Parses:
                            Lexicon.Parses[good_parse] = 1
                        if affix == 'NULL':
                            word = stem
                        elif FindSuffixesFlag:
                            word = stem+affix
			else:
			    word = affix + stem
                        Lexicon.WordBiographies[word].append("6. good_sig_string" )
                        if verboseflag:
                            contentlist.append(formatstring2.format(stem, affix, good_sig_string))


        if verboseflag:
            print_report(filename, headerlist, contentlist)

        MinimumStemCountinSignature = 1
        AssignAffixesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag, Step=-1)
        AssignSignaturesToEachStem_crab(Lexicon,FindSuffixesFlag,verboseflag,MinimumStemCountinSignature,Step)



# ----------------------------------------------------------------------------------------------------------------------------#
def	ReplaceParsePairsFromCurrentSignatureStructure_crab(Lexicon,FindSuffixesFlag=True):
# ----------------------------------------------------------------------------------------------------------------------------#
# The Lexicon.Parse pairs are the basic pieces out of which the whole signature structure is built. So in order to
# redo the signature structure, we just make sure the parses are correct, then we clear the signature structure
# and rebuild it, which is easy to do.

	Lexicon.Parses.clear()
        signatures= Lexicon.SignatureStringsToStems.keys()
	for sig in signatures:
                stems = Lexicon.SignatureStringsToStems[sig]
                affixes = sig.split("=")
                if FindSuffixesFlag:
                        for affix in affixes:
                                if affix == "NULL":
                                        affix = ""
                                for stem in stems:
                                        Lexicon.Parses[(stem,affix)]=1
                else:
                        for affix in affixes:
                                if affix == "NULL":
                                        affix = ""
                                for stem in stems:
                                        Lexicon.Parses[(affix,stem)]=1











# ----------------------------------------------------------------------------------------------------------------------------#
