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
def MakeSignatures_Crab(Lexicon, lxalogfile, outfile_Rebalancing_Signatures, outfile_unlikelysignatures,
                       outfile_subsignatures, FindSuffixesFlag,   verboseflag = False):
        # ----------------------------------------------------------------------------------------------------------------------------#
        MinimumStemLength = Lexicon.MinimumStemLength
        verboseflag = True
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
        FindProtostems(Lexicon,  Protostems,  FindSuffixesFlag, verboseflag, Step, maximumstemlength)
        if verboseflag:
            print formatstring1.format("1. Finished finding proto-stems.", len(Protostems))

        # 2 and 3 --------------------------------------------------------------------
        Step += 1
        AssignAffixesAndWordsToStems(Lexicon, Protostems, FindSuffixesFlag,Step,verboseflag )
        if verboseflag:
            print  "   Finished finding affixes for protostems." 

        # problem already exists, of having both NULL and null with emerge? not on 3 parse pair list though.???
        # --------------------------------------------------------------------
        # 4  Assign signatures to each stem This is in a sense the most important step.        -------
        Step += 1
        AssignSignaturesToEachStem(Lexicon, FindSuffixesFlag,verboseflag,Step)
        if verboseflag:
            print  formatstring1.format("5. Finished first pass of finding stems, affixes, and signatures.",
                                    len(Lexicon.SignatureStringsToStems))
        Lexicon.Compute_Lexicon_Size()
        # --------------------------------------------------------------------
        # 3  Find good signatures inside signatures that don't have enough stems to be their own signatures.
        # We make a temporary list of signatures called GoodSignatures, which have enough stems. 
        # We check all sigs in SignaturesToStems to see if they have enough stems. If they do not,
        # we look to see if we can find a Good Signature inside it. If not, we delete it; and we delete
        # the analyses that were not handled by the Good Signature. 
        if verboseflag:
            print  formatstring1.format("6. Looking for good signatures inside bad ones.", len(Lexicon.SignatureStringsToStems))

        Step += 1
        FindGoodSignaturesInsideBad(Lexicon, outfile_subsignatures, FindSuffixesFlag,verboseflag, Step);
 
        if verboseflag:
            print formatstring2.format("5. Finished; we will reassign signature structure.")
            print formatstring2.format("6. Recompute signature structure.\n     <----------------------------------------->")
        Step += 1
        AssignSignaturesToEachStem(Lexicon, FindSuffixesFlag, verboseflag,Step)

        # --------------------------------------------------------------------
        # 4 Rebalancing now, which means:                  -------
        # We look for a stem-final sequence that appears on all or almost all the stems, and shift it to affixes.
        # Make changes in Lexicon.SignatureStringsToStems, and .StemToSig, and .WordToSig, and .StemToWord, and .StemToAffix  and signature_tuples....

        if verboseflag:
            print formatstring2.format("5. Find shift stem/affix boundary when appropriate.")
        threshold = 0.80

        if False:

            count = Lexicon.RebalanceSignatureBreaks(threshold, outfile_Rebalancing_Signatures, FindSuffixesFlag,Step)
            print formatstring2.format("5. Completed.")
            print formatstring2.format("6. Recompute signature structure.")
            Lexicon.AssignSignaturesToEachStem(FindSuffixesFlag,Step)

        # --------------------------------------------------------------------
        # 5  ------- compute robustness
        Lexicon.Compute_Lexicon_Size()
        print  formatstring2.format("6. Computed robustness")

        # 6  ------- Print
        print >> lxalogfile, formatstring3.format("Number of analyzed words", Lexicon.NumberOfAnalyzedWords)
        print >> lxalogfile, formatstring3.format("Number of unanalyzed words", Lexicon.NumberOfUnanalyzedWords)
        print >> lxalogfile, formatstring3.format("Letters in stems", Lexicon.total_letters_in_stems)
        print >> lxalogfile, formatstring3.format("Letters in affixes", Lexicon.total_affix_length_in_signatures)
        print >> lxalogfile, formatstring3.format("Total robustness in signatures", Lexicon.TotalRobustnessInSignatures)

        return

 
                #---------------------------------------------------------------------------------------------------------------------#

def FindProtostems(Lexicon,  Protostems, FindSuffixesFlag,verboseflag,Step, maximum_stem_length=-1):
        # A "maximum_stem_length" is included here so that we can use this function to explore
        # for stems shorter than the minimum that was assumed on an earlier iteration.
        wordlist = Lexicon.WordCounts.keys()
        wordlist.sort()
        minimum_stem_length = Lexicon.MinimumStemLength
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
                        differencefoundflag = True
                        stem = word[:j]
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
                                    contentlist.append(reportline)
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
                            if (previousword not in Protostems):
                                if verboseflag:
                                    reportline = formatstring1.format(word,   end, previousword, "New stem.")
                                    if word == "hanging":
                                        print "183 hanging"
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
            # print "prefixes"
            ReversedList = list()
            TempList = list()
            for word in wordlist:
                key = word.Key
                key = key[::-1]
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
                            if stem not in Protostems:
                                Protostems[stem] = 1
                            else:
                                Protostems[stem] += 1
                                # print previousword, word, stem
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


                # ----------------------------------------------------------------------------------------------------------------------------#

def AssignAffixesAndWordsToStems(Lexicon, Protostems, FindSuffixesFlag,Step, verboseflag = False):
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
        if FindSuffixesFlag:
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
                if word == "hanging":
                        print "282 hanging"
                WordAnalyzedFlag = False
                for i in range(len(word), MinimumStemLength - 1, -1):  
                    if FindSuffixesFlag:
                        stem = word[:i]
                    else:
                        stem = word[-1 * i:]
                    if stem in Protostems:
                        if word == "hanging":
                                print stem
                        if FindSuffixesFlag:
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
                                
                                if stem not in Lexicon.UnexplainedContinuations:
                                        Lexicon.UnexplainedContinuations[stem] = list()
                                Lexicon.UnexplainedContinuations[stem].append(suffix)
                                 
                                Lexicon.WordBiographies[word].append(str(Step) + " The split "+stem+ " / " + suffix + " is suspicious; suffix too long.")
                                if verboseflag:
                                    reportline = formatstring.format(word,stem,suffix, "suffix too long.")
                                    contentlist.append(reportline)
                                continue
                                
                                
                                
                        else:
                            j = len(word) - i
                            prefix = word[:j]
                            if len(prefix) > MaximumAffixLength:
                                continue
                            Lexicon.Parses[(prefix, stem)] = 1
                            if stem in Lexicon.WordCounts:
                                Lexicon.Parses[("NULL", stem)] = 1
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
            for item in Lexicon.Parses:
                if FindSuffixesFlag:
                    stem = item[0]
                    affix = item[1]
                templist.append (stem +' ' + affix )
                if affix == "NULL":
                    word = stem
                else:
                    word = stem + affix
                Lexicon.WordBiographies[word].append(str(Step) + " "+ item[0] + "=" + item[1])
            templist.sort()
            for item in templist:
                    contentlist.append(item)
            print_report(filename, headerlist, contentlist)



 
 # ----------------------------------------------------------------------------------------------------------------------------#

def AssignSignaturesToEachStem(Lexicon, FindSuffixesFlag,verboseflag,Step):
        """ This assumes StemToWord and StemToAffix, and creates:
            Affixes
            SignatureStringsToStems
            StemToSignature
            StemCorpusCounts
            WordToSig """


        Lexicon.StemCorpusCounts = dict()
        # This creates StemToWord; StemToAffixes; Affixes; 
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


  # --------              Part One     ----------------- Collect each affix a stem has.
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

 
        # --------              Part Two       -----------------

 # Now we create signatures: StemToSignature; WordToSig; StemToWord, SignatureStringsToStems


        Step += 1
        if verboseflag:
                filename = "6_assigning_signatures.txt"
                headerlist = [ "6. Assign a single signature to each stem."]
                contentlist = list()

                formatstring = "{0:20s}  {1:15s} {2:20s}{3:10s}"
                formatstring2 = "{0:20s}  {1:15s} "
                formatstring1 = "{0:32s}"

        stemlist = Lexicon.StemToAffix.keys()
        stemlist.sort()

        if verboseflag:
                print "     Assign a single signature to each stem"
        for stem in stemlist:
                signature_string = MakeSignatureStringFromAffixDict(Lexicon.StemToAffix[stem])
                this_signature = Signature(signature_string)
                Lexicon.Signatures[signature_string] = this_signature 
                Lexicon.StemToSignature[stem] = signature_string   #change this to signature
                Lexicon.StemCorpusCounts[stem] = 0
                if signature_string not in Lexicon.SignatureBiographies:
                    Lexicon.SignatureBiographies[signature_string] = list()
                    Lexicon.SignatureBiographies[signature_string].append ("Created at first opportunity, in AssignSignaturesToEachStem.")
                for word in Lexicon.StemToWord[stem]:
                    if word not in Lexicon.WordToSig:
                        Lexicon.WordToSig[word] = list()
                    if signature_string not in Lexicon.WordToSig[word]:
                        Lexicon.WordToSig[word].append((stem, signature_string)) #change this to signature
                    Lexicon.StemToWord[stem][word] = 1
                    Lexicon.StemCorpusCounts[stem] += Lexicon.WordCounts[word]
                    Lexicon.WordBiographies[word].append(str(Step) + " In signature " + signature_string)
                if signature_string not in Lexicon.SignatureStringsToStems: 
                    Lexicon.SignatureStringsToStems[signature_string] = dict() # put this into signature itself
                Lexicon.SignatureStringsToStems[signature_string][stem] = 1  # put this into signature itself
                this_signature.add_stem(stem)
                this_signature.add_affix(deepcopy(Lexicon.StemToAffix[stem]))
                if verboseflag:
                        reportline=formatstring2.format(stem,signature_string)
                        contentlist.append(reportline)
 

        if verboseflag:
            print "     End of assigning a signature to each stem."
        if verboseflag:
                print_report(filename, headerlist, contentlist)

            # ----------------------------------------------------------------------------------------------------------------------------#
            # ----------------------------------------------------------------------------------------------------------------------------#
            # This is apparently not used anymore.

def RemoveSignaturesWithTooFewStems(Lexicon):
        for sig in Lexicon.SignatureStringsToStems:  #make this use Lexicon.Signatures instead
            if len(Lexicon.SignatureStringsToStems[sig]) < Lexicon.MinimumStemsInaSignature:
                del Lexicon.Signatures[sig]
                for stem in Lexicon.SignatureStringsToStems[sig]:
                    del Lexicon.StemToSignature[stem]
                    for word in Lexicon.StemToWord[stem]:
                        if len(Lexicon.WordToSig[word]) == 1:
                            del Lexicon.WordToSig[word]
                        else:
                            Lexicon.WordToSig[word].remove(sig)
                    del Lexicon.StemToWord[stem]

                # ----------------------------------------------------------------------------------------------------------------------------#




    # ----------------------------------------------------------------------------------------------------------------------------#
def RebalanceSignatureBreaks(Lexicon, threshold, outfile, FindSuffixesFlag,verboseflag = True):
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
def FindGoodSignaturesInsideBad(Lexicon, subsignaturesfile, FindSuffixesFlag, verboseflag, Step):
        # NOTE! This needs to be updated to include Lexicon.Signatures
        # ----------------------------------------------------------------------------------------------------------------------------#
        if verboseflag:

            filename = "7_good_signatures_inside_bad.txt"
            headerlist = [ "Find good signatures inside bad ones."]
            contentlist = list()
            linelist = list()

            contentlist.append("Good signature              Bad signature")
        Lexicon.Suffixes = dict()
        GoodSignatures = list()
        Transactions = list()
        SignatureList = Lexicon.SignatureStringsToStems.keys()
        SignatureList.sort()
        for sig_string in SignatureList:
            sig_list = MakeSignatureListFromSignatureString(sig_string)
            number_of_stems = len(Lexicon.SignatureStringsToStems[sig_string])
            if number_of_stems >= Lexicon.MinimumStemsInaSignature:
                GoodSignatures.append(sig_string)
                Lexicon.SignatureBiographies[sig_string].append("Validated, with stem count:" + str(number_of_stems))
                if verboseflag:
                    contentlist.append (sig_string)
            elif verboseflag:
                if len(sig_string) < 50 :
                    contentlist.append(" "*20 + sig_string)
                    
                else:
                    sig_list = splitsignature(sig_string,40)
                    contentlist.append(" "*20 + sig_list[0] )
                    del sig_list[0]
                    for item in sig_list:
                        contentlist.append(" "*25 + item )
        if verboseflag:
            contentlist.append("\n\n Working on bad signatures\n ")

        formatstring1 = "Bad: {0:20s} Corrected: {1:50s}"
        formatstring2 = "     {0:10s}={1:6s} shifted from {2:20s} to {3:15s}"
        formatstring3=  "{0:20s} {1:30s}"
        formatstring4 = "     Removing  signature: {0:30} stem: {1:20s}  affix: {2:20s}"
        for sig_string in SignatureList:
            if sig_string in GoodSignatures:
                continue
            sig_list = MakeSignatureListFromSignatureString(sig_string)
 
                
            good_sig_list = FindGoodSignatureListFromInsideAnother(sig_list, GoodSignatures)
            good_sig_string = "=".join(good_sig_list)

            transaction = dict()
            Transactions.append(transaction)
            transaction["sig"] = sig_string
            number_of_stems == len(Lexicon.SignatureStringsToStems[sig_string])
            if good_sig_string == sig_string:
                stem_count = len(Lexicon.SignatureStringsToStems[sig_string])
                Lexicon.SignatureBiographies[sig_string].append("Low count ("+ str(stem_count) +   " but OK because it is a composite sig.")
                continue;
            if (good_sig_list):
                Lexicon.SignatureBiographies[sig_string].append("Stem count: " + str(number_of_stems) + ". Removed and replaced by: "+ good_sig_string)
                if verboseflag:
                    contentlist.append(formatstring1.format(sig_string,good_sig_string ))
                transaction["subsig"] = good_sig_string
                for stem in Lexicon.SignatureStringsToStems[sig_string]:
                    for affix in good_sig_list:
                        if FindSuffixesFlag:
                            good_parse = (stem, affix)
                        else:
                            good_parse = (affix, stem)
                        if affix == 'NULL':
                            word = stem
                        else:
                            word = stem+affix
                        Lexicon.WordBiographies[word].append("6 Shifted from " + sig_string + " to " + good_sig_string )
                        if verboseflag:
                            contentlist.append(formatstring2.format(stem ,affix , sig_string,  good_sig_string))

                remaining_affixes = set(sig_list) - set(good_sig_list)

                unlikelysignature = list(remaining_affixes)
                unlikelysignature.sort()
                unlikelysignature = '='.join(unlikelysignature)
                Lexicon.RemovedSignatureList.append(unlikelysignature)
                Lexicon.UnlikelySignatureStringsToStems[unlikelysignature] = dict()
                transaction["badsig"] = unlikelysignature
                for stem in Lexicon.SignatureStringsToStems[sig_string]:
                    Lexicon.UnlikelySignatureStringsToStems[unlikelysignature][stem] = 1
                    for affix in remaining_affixes:
                        if FindSuffixesFlag:
                            if affix == "":
                                affix = "NULL"
                            bad_parse = (stem, affix)
                            if affix == "NULL":
                                word = stem
                            else:
                                word = stem + affix
                            Lexicon.WordBiographies[word].append("6 This split is eliminated: " + stem + "=" + affix +"("+ str(number_of_stems) + ")")
                            Lexicon.WordBiographies[word].append("6 Only this signature retained:" + good_sig_string)
                            
                            contentlist.append( "Class Lexicon 939")
                            if affix not in Lexicon.PossibleSuffixes:
                                Lexicon.PossibleSuffixes[affix]= dict()
                                contentlist.append(affix)
                            Lexicon.PossibleSuffixes[affix][stem]=1
                        else:
                            bad_parse = (affix, stem)
                        del Lexicon.Parses[bad_parse]


            else:
                Lexicon.SignatureBiographies[sig_string].append("Bad signature by count, entirely deleted. Count: " + str(number_of_stems)+".")
                Lexicon.RemovedSignatureList.append(sig_string)
                transaction["badsig"] = sig_string
                if verboseflag:
                    contentlist.append(formatstring3.format("Nothing found in " , sig_string, "stem count:", number_of_stems))
                for stem in Lexicon.SignatureStringsToStems[sig_string]:
                    for affix in sig_list:
                        if affix == "NULL":
                            word = stem
                        else:
                            word = stem + affix
                        if len(affix)==0:
                            bad_parse=(stem, "NULL")
                        else:
                            bad_parse = (stem, affix)

                        del Lexicon.Parses[bad_parse]
                        if affix == "NULL":
                            affix_t = ""
                        else:
                            affix_t = affix
                        Lexicon.WordBiographies[word].append(str(Step) + " 6 Bad signature eliminated: "+ sig_string + " hence *" + stem + "=" + affix_t +"  (stem count: "+ str(number_of_stems) + ")")
                        if verboseflag:
                            line = formatstring4.format(sig_string,  stem, affix)
                            contentlist.append(line)
                            line=""
        Successes = list()
        maxlength = 0
        for transaction in Transactions:
            if "subsig" in transaction and len(transaction["subsig"]) > maxlength:
                maxlength = len(transaction["subsig"])

        for transaction in Transactions:
            if "subsig" in transaction:
                sig_list = MakeSignatureListFromSignatureString(transaction["subsig"])
                if len(sig_list) < 2:
                    continue
                Successes.append(transaction)
        Successes.sort(key=lambda L: L["subsig"])

        if verboseflag:
            print_report(filename, headerlist, contentlist)

        maxlength = 0
        for transaction in Successes:
            if len(transaction["subsig"]) > maxlength:
                maxlength = len(transaction["subsig"])

        for transaction in Successes:
            print >> subsignaturesfile, transaction["subsig"] + " " * (maxlength - len(transaction["subsig"])) + transaction[
                "badsig"]

        for suffix in Lexicon.PossibleSuffixes:
                source = "Class Lexicon l. 1004 in ClassLexicon"
                format_string_6 = "{0:15s} {1:25s} {2:30s}"
                if len(Lexicon.PossibleSuffixes[suffix]) > 1:
                    print >>subsignaturesfile, format_string_6.format(suffix, Lexicon.PossibleSuffixes[suffix], "Class Lexicon l. 1004 in ClassLexicon")

        AssignSignaturesToEachStem(Lexicon,FindSuffixesFlag,verboseflag,Step)


 
# ----------------------------------------------------------------------------------------------------------------------------#
