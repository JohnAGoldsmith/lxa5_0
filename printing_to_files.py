import math
from signaturefunctions import *
from html_lxa import *
#from IPython.display import display





def print_html_report(outfile, this_lexicon, singleton_signatures, doubleton_signatures, DisplayList):
    leader=["Number of distinct words (types):" , "Total letter count in words " , "Number of stems: ", "Number of signatures: ",
        "Number of singleton signatures (one stem): ", "Number of doubleton signatures (two stems): ",
        "Total number of letters in stems: ",  "Total number of affix letters: "]
    values=[ str(this_lexicon.get_total_word_count()),  str(this_lexicon.get_total_word_letter_count()), str(len(this_lexicon.StemToSignature)), str(len(this_lexicon.Signatures)), str(singleton_signatures),   str(doubleton_signatures), str(this_lexicon.get_total_letters_in_stems()), str(this_lexicon.get_total_affix_letter_count()) ]

    start_an_html_file( outfile)
    start_an_html_table(outfile)
    for lineno in range(8):
                start_an_html_table_row(outfile)
                add_an_html_table_entry(outfile, leader[lineno])
                add_an_html_table_entry(outfile, values[lineno])
                end_an_html_table_row(outfile)
    end_an_html_table(outfile)
    end_an_html_file(outfile)



def print_report(filename, headerlist, contentlist):
    file = open(filename, 'w')
    for item in headerlist:
        print >>file, item
    print >>file, len(contentlist)
    for item in contentlist:
        print >> file, item
    file.close()

# ----------------------------------------------------------------------------------------------------------------------------#
def print_parses(this_file, Lexicon):
    print >>this_file, "size:",   str(len(Lexicon.Parses))
    for parse in sorted(Lexicon.Parses):
        print >>this_file, parse
    this_file.close()
# ----------------------------------------------------------------------------------------------------------------------------#
def initialize_files(this_lexicon, this_file, singleton_signatures, doubleton_signatures, DisplayList):
    reportlist = this_lexicon.produce_lexicon_report()
    for line in reportlist:
        if this_file == "console":
            print line
        else:
            print >>this_file, line
# ----------------------------------------------------------------------------------------------------------------------------#
def print_signature_list_1(this_file,
                           Lexicon,
                           DisplayList,
                           total_robustness,
                           lxalogfile,
                           affix_type):
    if affix_type == "suffix":
        FindSuffixesFlag = True
    else:
        FindSuffixesFlag = False
    print "   Printing signature file."
    running_sum = 0.0
    formatstring1 = '{0:25}{1:>10s} {2:>15s} {3:>25s} {4:>20s}{5:>20s}{6:>20s} '
    formatstring2 = '{0:<30}{1:5d} {2:15d} {3:25.3%} {4:20.3%}{5:20.2f}{6:>20s}'
    print >> this_file, "\n" + "-" * 150
    print >> this_file, formatstring1.format("Signature", "Stem count", "Robustness", "Proportion of robustness",
                                             "Running sum", "Stability" , "Example")
    print >> this_file, "-" * 150

    DisplayList = sorted(DisplayList, key = lambda x: x[2], reverse=True)
    for sig, stemcount, robustness, stability, stem in DisplayList:
        if sig in Lexicon.ShadowSignatures:
            #print "112 printing, shadow", annotatedsig
            annotatedsig = "[" + sig  + "]"
        else:
            annotatedsig = sig

        running_sum += robustness
        robustness_proportion = float(robustness) / total_robustness
        running_sum_proportion = running_sum / total_robustness
        print >> this_file, formatstring2.format(annotatedsig, stemcount, robustness, robustness_proportion,
                                                     running_sum_proportion, stability,  stem)
    print >> this_file, "-" * 60

    number_of_stems_per_line = 6
    stemlist = []
    for sig, stemcount, robustness,stability, stem in DisplayList:
        this_signature = Lexicon.Signatures[sig]
        if sig in Lexicon.ShadowSignatures:
             annotatedsig = "spurious: " + sig
        else:
            annotatedsig = sig
        print >> this_file, "\n" + "=" * 45, '{0:30s} \n'.format(annotatedsig)
        n = 0
        stemlist = this_signature.get_stems()
        numberofstems = len(stemlist)
        max_word_length =  len(max(stemlist, key = len))
        col_width = max_word_length + 2 
        for stem in stemlist:
            n += 1
            print >> this_file,  stem, " "* (col_width - len(stem)),
            if n % number_of_stems_per_line == 0:
                print >> this_file
        print >> this_file, "\n" + "-" * 25

        numberofcolumns = 4
        colno = 0
        stemlist.sort(key = lambda x : Lexicon.StemCorpusCounts[x], reverse = True)
        for stem in stemlist:
            print >> this_file, stem, " " * (col_width - len(stem)), '{:6d}'.format(Lexicon.StemCorpusCounts[stem] ),
            colno += 1
            if colno % numberofcolumns == 0:
                print >> this_file
        print >> this_file, "\n" + "-" * 25

        bitsPerLetter = 5
        wordlist = makeWordListFromSignature(sig, stemlist)
        (a, b, c) = findWordListInformationContent(wordlist, bitsPerLetter)
        (d, e, f) = findSignatureInformationContent(  sig, stemlist, bitsPerLetter)
        formatstring = '%35s %10d  '
        formatstringheader = '%35s %10s    %10s  %10s'
        print >> this_file, formatstringheader % ("", "Phono", "Ordering", "Total")
        print >> this_file, formatstring % ("Letters in words if unanalyzed:", a)
        print >> this_file, formatstring % ("Letters as analyzed:", d)
        # ------------------------------------------------------------------------------------------------------
        howmanytopstems = 5

        print >> this_file, "\n-------------------------"
        print >> this_file, "Entropy-based stability: ", this_signature.get_stability_entropy() 
        print >> this_file, "\n", "High frequency possible affixes \nNumber of stems: ", len(stemlist)
        formatstring = '%10s    weight: %5d count: %5d %2s'
        peripheralchunklist = find_N_highest_weight_affix(stemlist, FindSuffixesFlag)

        for item in peripheralchunklist:
            if item[2] >= numberofstems * 0.9:
                flag = "**"
            else:
                flag = ""
            print >> this_file, formatstring % (item[0], item[1], item[2], flag)

    this_file.close()

def print_signature_list_1_html(this_file, DisplayList, totalrobustness):
    print "   Printing signatures in an  html file."
    runningsum = 0.0
    formatstring1 = '{0:25}{1:>10s} {2:>15s} {3:>25s} {4:>20s}{5:>20s} '
    formatstring2 = '{0:<25}{1:10d} {2:15d} {3:25.3%} {4:20.3%}{5:>20s}'
    headers = ["Signature", "Stem count", "Robustness", "Proportion of robustness",
                                             "Running sum", "Example"]
    DisplayList = sorted(DisplayList, lambda x, y: cmp(x[2], y[2]), reverse=True)
    start_an_html_file( this_file)
    start_an_html_table(this_file)
    start_an_html_table_row(this_file)
    for item in headers:
        add_an_html_table_entry(this_file, item)
    end_an_html_table_row(this_file)

    for sig, stemcount, robustness, stability, stem in DisplayList:
        runningsum += robustness
        start_an_html_table_row(this_file)
        robustnessproportion = float(robustness) / totalrobustness
        runningsumproportion = runningsum / totalrobustness
        add_an_html_table_entry(this_file, sig)
        add_an_html_table_entry(this_file, str(stemcount) )
        add_an_html_table_entry(this_file, str(robustness))
        add_an_html_table_entry(this_file, str(robustnessproportion))
        add_an_html_table_entry(this_file, str(runningsumproportion))
        add_an_html_table_entry(this_file, stem)
        end_an_html_table_row(this_file)
    end_an_html_table(this_file)
    end_an_html_file( this_file)
    this_file.close()

# ----------------------------------------------------------------------------------------------------------------------------#

def print_signatures_to_svg (outfile_html, DisplayList,Signatures,FindSuffixesFlag):
    this_page = Page()
    DisplayList = sorted(DisplayList, lambda x, y: cmp(x[2], y[2]), reverse=True)
    this_page.start_an_html_file(outfile_html)
    column_counts = dict();
    for signo in range(len(DisplayList)):
            (sig,stemcount,robustness,stability,stem) = DisplayList[signo]
            stemlist = Signatures[sig].get_stems()
            row_no= sig.count("=")+1
            if row_no not in column_counts:
                column_counts[row_no] = 1
            else:
                column_counts[row_no] += 1
            col_no = column_counts[row_no]
            radius_guide = len(stemlist) * row_no
            stem_count = len(stemlist)
            this_page.print_signature (outfile_html, sig, radius_guide, row_no, col_no, stem_count)
    this_page.end_an_html_file(outfile_html)
    outfile_html.close()

# ----------------------------------------------------------------------------------------------------------------------------#
def print_complex_signature_to_svg (outfile_html, sig, lexicon):
# a complex signature is one where the "stem" column is a stack, of several groups, including a stem list,
# and also a list of analyzed stems with their signatures.
    this_page = Page()
    this_page.start_an_html_file(outfile_html)
    stem_list = lexicon.Signatures[sig].getstems()
    affix_list = sig.split("=")
    complex_signature_box = ComplexSignatureBox(stem_list, affix_list)
    signature_box.print_signature_box(outfile_html, this_page, 300,300)
    this_page.end_an_html_file(outfile_html)
    outfile_html.close()

# ----------------------------------------------------------------------------------------------------------------------------#
def print_signature_list_2(signature_feeding_outfile, lxalogfile, Lexicon,  DisplayList, totalrobustness, suffix_flag):

    start_an_html_file (signature_feeding_outfile)
    stemlist = []
    for sig, stemcount, robustness, stability, stem in DisplayList:
        this_signature = Lexicon.Signatures[sig]
        stemlist = this_signature.stem_counts.keys()
        # ------------------------------------------------------------------------------------------------------
        # Already analyzed stems: Just a temporary experiment to see how one signature feeds another.
        #print "\n", sig    , "line 213 of printing_to_files"
        numberofstems = len(stemlist)
        temp_signatures_with_stems = dict()

        # test whether there will be any entries here:
        PrintThisSignatureFlag=False
        for stem in stemlist:
            if stem in Lexicon.WordToSig:
                for pair in Lexicon.WordToSig[stem]:
                    if pair[1] != sig:
                        PrintThisSignatureFlag = True
                        break
            if PrintThisSignatureFlag == True:
                break
        if PrintThisSignatureFlag == False:
            continue

        start_an_html_div(signature_feeding_outfile, class_type="largegroup")
        this_box = Box(sig, "signature")
        this_box.print_box(signature_feeding_outfile, "signature-left")

        for stem in stemlist:
            if stem in Lexicon.WordToSig:
                for pair in Lexicon.WordToSig[stem]:
                    sig2 = pair[1]
                    if  sig2 != sig:
                        #start_an_html_table_row(signature_feeding_outfile)
                        #add_an_html_table_entry(signature_feeding_outfile, stem)
                        #add_an_html_table_entry(signature_feeding_outfile, sig2)
                        #add_an_html_table_entry(signature_feeding_outfile, pair[0] )
                        if sig2 not in temp_signatures_with_stems:
                                temp_signatures_with_stems[sig2]=list()
                        temp_signatures_with_stems[sig2].append((stem,pair[0]))
                        #end_an_html_table_row(signature_feeding_outfile)
        #end_an_html_table(signature_feeding_outfile)

        number_of_columns = 7
        colno=0
        start_an_html_table(signature_feeding_outfile)
        signature_list= sorted(temp_signatures_with_stems , key = lambda x:len(temp_signatures_with_stems[x]), reverse=True  )
        for item  in signature_list:
            start_an_html_table_row(signature_feeding_outfile)
            add_an_html_table_entry(signature_feeding_outfile, item)
            end_an_html_table_row(signature_feeding_outfile)
            colno=0
            for chunk in temp_signatures_with_stems[item]:
                if colno == 0:
                    colno = 1
                    start_an_html_table_row(signature_feeding_outfile)
                    add_an_html_table_entry(signature_feeding_outfile, "")
                add_an_html_table_entry(signature_feeding_outfile, chunk)
                colno += 1
                if colno == number_of_columns:
                    end_an_html_table_row(signature_feeding_outfile)
                    colno = 0
        end_an_html_table(signature_feeding_outfile)
        end_an_html_div(signature_feeding_outfile)
    signature_feeding_outfile.close()

# ----------------------------------------------------------------------------------------------------------------------------#
def print_unlikelysignatures(this_file, signatures, ColumnWidth):
    print "   Printing unlikely signatures file."
    runningsum = 0.0
    formatstring1 = '{0:<70}{1:>10s}'
    formatstring2 = '{:<70} '
    print >> this_file, "\n" + "-" * 150
    print >> this_file, formatstring2.format("Unlikely Signatures")
    print >> this_file, "-" * 150
    these_signatures_list = signatures.keys()
    these_signatures_list.sort()
    for sig in these_signatures_list:
        if len(sig) == 0:
            continue
        for stem in signatures[sig]:
            print >> this_file, stem
        print >> this_file, formatstring2.format(sig)

        print >> this_file
    print >> this_file, "-" * 60

    this_file.close()
# ----------------------------------------------------------------------------------------------------------------------------#
def print_suffixes(outfile, Suffixes, RawSuffixes):
    print >> outfile, "--------------------------------------------------------------"
    print >> outfile, "        Suffixes "
    print >> outfile, "--------------------------------------------------------------"
    print "   Printing suffixes."
    formatstring = "{:12s}{:9,d}"
    suffixlist = list(Suffixes.keys())
    suffixlist.sort(key=lambda suffix: Suffixes[suffix], reverse=True)
    for suffix in suffixlist:
        if suffix == "":
                suffix = "NULL"
        print >> outfile, formatstring.format(suffix, Suffixes[suffix])
        if suffix in RawSuffixes:
            count = 0
            how_many = 5
            for stem in sorted(RawSuffixes[suffix]):
                if count == 0:
                    print >>outfile, "\t",
                print >>outfile, stem,
                if count == how_many:
                    count = 0
                    print >>outfile
                else:
                    count += 1
            print >>outfile, "\n"
    print >>outfile, "\n-------------------------------------\n"
    suffixlist.sort()
    for suffix in suffixlist:
        if suffix == "":
                suffix = "NULL"
        print >> outfile, formatstring.format(suffix, Suffixes[suffix])

    outfile.close()
    return suffixlist
# ----------------------------------------------------------------------------------------------------------------------------#
def print_stems(outfile1, outfile_stems_and_unanalyzed_words, Lexicon, suffixlist):
    StemToWord = Lexicon.StemToWord
    StemToSignature = Lexicon.StemToSignature
    WordCounts = Lexicon.Word_counts_dict
    stems = StemToWord.keys()
    stems.sort()
    length_longest_stem = len ( max (stems, key = len)) 
    print >> outfile1, "--------------------------------------------------------------"
    print >> outfile1, "---  Stems and their words"
    print >> outfile1, "--------------------------------------------------------------"
    print "   Printing stems and their words."
    StemCounts = dict()
    for stem in stems:
        print >> outfile1, stem, " "*(length_longest_stem + 2 - len(stem)),
        wordlist = StemToWord[stem].keys()
        wordlist.sort()
        stemcount = 0
        for word in wordlist:
            if word in WordCounts:
                stemcount += WordCounts[word]
        StemCounts[stem] = stemcount
        print    >> outfile1, '{:5d}'.format(stemcount), '; ',
        stemcount = float(stemcount)
        for word in wordlist:
            wordcount = 0
            if word in WordCounts:
                wordcount = WordCounts[word]
            print >> outfile1, '{:20}{:6n} '.format(word, wordcount),
        print >> outfile1

    # Add to wordlist all the words that have no analysis

    stems_and_unanalyzed_words = deepcopy(stems)
    for word in WordCounts:
	if word not in Lexicon.WordToSig:
	    stems_and_unanalyzed_words.append(word + "*")
    stems_and_unanalyzed_words.sort()
    print >> outfile_stems_and_unanalyzed_words, "--------------------------------------------------------------"
    print >> outfile_stems_and_unanalyzed_words, "---  Stems and unanalyzed words"
    print >> outfile_stems_and_unanalyzed_words, "--------------------------------------------------------------"
    print "   Printing stems and their words along with unanalyzed words."
    StemCounts = dict()
    for item in stems_and_unanalyzed_words:
	if item in stems:
                stem = item
		print >> outfile_stems_and_unanalyzed_words, "{:15s}".format(stem),
		wordlist = StemToWord[stem].keys()
		wordlist.sort()
		stemcount = 0
		for word in wordlist:
                    if word in WordCounts:
		        stemcount += WordCounts[word]
		StemCounts[stem] = stemcount
		print >> outfile_stems_and_unanalyzed_words, '{:5d}'.format(stemcount), '; ',
		stemcount = float(stemcount)
		for word in wordlist:
                    wordcount = 0
                    ratio = 0.0
                    if word in WordCounts:
          	        wordcount = WordCounts[word]
                        ratio = wordcount/ float(stemcount)
		    print >> outfile_stems_and_unanalyzed_words, '{:15}{:4n} {:7.1%} '.format(word, wordcount, ratio),
        	print >> outfile_stems_and_unanalyzed_words
	else:
		print >>outfile_stems_and_unanalyzed_words,  item
    outfile1.close()
    outfile_stems_and_unanalyzed_words.close()
# ----------------------------------------------------------------------------------------------------------------------------#
def AverageCountOfTopStems(howmany, sig, Signatures, StemCounts, logfile):
    stemlist = list(Signatures[sig])
    countlist = []
    count = 0
    average = 0
    for stem in stemlist:
        if stem not in StemCounts:
            print >> logfile, "Stem", stem, "is present in signature", sig, "but is not in the Stem list."
        else:
            countlist.append(StemCounts[stem])
    countlist = sorted(countlist, reverse=True)
    if len(countlist) < howmany:
        howmany = len(countlist)
    if howmany == 0:
        print >> logfile, "230 zero count for stem", stem
        return 0
    for n in range(howmany):
        average += countlist[n]
    average = average / howmany
    return average
# ---------------------------------------------------------#
def makeWordListFromSignature(signature, stemset):
    wordlist = list()
    word = ""
    for stem in stemset:
        for affix in signature:
            if affix == "NULL":
                word = stem
            else:
                word = stem + affix
        wordlist.append(word)
    return wordlist
# ---------------------------------------------------------#
def findWordListInformationContent(wordlist, bitsPerLetter):
# ----------------------------------------------------------------------------------------------------------------------------#
    phonoInformation = 0
    orderingInformation = 0
    letters = 0
    for word in wordlist:
        wordlength = len(word)
        letters += wordlength
        phonoInformation += bitsPerLetter * wordlength
        orderingInformation += wordlength * (wordlength - 1) / 2
    return (letters, phonoInformation, orderingInformation)
# ---------------------------------------------------------#
def findSignatureInformationContent(signature, stemset, bitsPerLetter):
# ----------------------------------------------------------------------------------------------------------------------------#
    stemSetPhonoInformation = 0
    stemSetOrderingInformation = 0
    affixPhonoInformation = 0
    affixOrderingInformation = 0
    letters = 0
    for stem in stemset:
        stemlength = len(stem)
        letters += stemlength
        stemSetPhonoInformation += bitsPerLetter * stemlength
        if stemlength > 1:
            stemSetOrderingInformation += math.log(stemlength * (stemlength - 1) / 2, 2)
    for affix in signature:
        affixlength = len(affix)
        letters += affixlength
        affixPhonoInformation += bitsPerLetter * len(affix)
        if affixlength > 1:
            affixOrderingInformation += math.log(affixlength * (affixlength - 1) / 2, 2)
        else:
            affixOrderingInformation = 0
    phonoInformation = int(stemSetPhonoInformation + affixPhonoInformation)
    orderingInformation = int(stemSetOrderingInformation + affixOrderingInformation)
    return (letters, phonoInformation, orderingInformation)
# ----------------------------------------------------------------------------------------------------------------------------#
def  StabilityAsEntropy(stemlist, MakeSuffixesFlag):
# ----------------------------------------------------------------------------------------------------------------------------#
    """Determines if this signature is prima facie plausible, based on letter entropy.
       If this value is above 1.5, then it is a stable signature: the number of different letters
       that precede it is sufficiently great to have confidence in this morpheme break."""

    entropy = 0.0
    frequency = dict()
    templist = list()
    if MakeSuffixesFlag == False:
        for chunk in stemlist:
            templist.append(chunk[::-1])
        stemlist = templist
    for stem in stemlist:
        lastletter = stem[-1]
        if lastletter not in frequency:
            frequency[lastletter] = 1.0
        else:
            frequency[lastletter] += 1.0
    for letter in frequency:
        frequency[letter] = frequency[letter] / len(stemlist)
        entropy += -1.0 * frequency[letter] * math.log(frequency[letter], 2)
    return entropy
# ----------------------------------------------------------------------------------------------------------------------------#
def find_N_highest_weight_affix(wordlist, suffix_flag):
# ----------------------------------------------------------------------------------------------------------------------------#

    maximalchunksize = 6  # should be 3 or 4 ***********************************
    totalweight = 0
    # threshold         = 50
    weightthreshold = 0.02
    # permittedexceptions   = 2
    MinimalCount = 10
    chunkcounts = {}
    chunkweights = {}
    chunkweightlist = []
    tempdict = {}
    templist = []
    for word in wordlist:
        totalweight += len(word)

    if suffix_flag:
        for word in wordlist:
            for width in range(1,
                               maximalchunksize + 1):  # width is the size (in letters) of the suffix being considered
                chunk = word[-1 * width:]
                if not chunk in chunkcounts.keys():
                    chunkcounts[chunk] = 1
                else:
                    chunkcounts[chunk] += 1
    else:
        for word in wordlist:
            for width in range(1,
                               maximalchunksize + 1):  # width is the size (in letters) of the prefix being considered
                chunk = word[:width]
                if not chunk in chunkcounts.keys():
                    chunkcounts[chunk] = 1
                else:
                    chunkcounts[chunk] += 1
    for chunk in chunkcounts.keys():
        chunkweights[chunk] = chunkcounts[chunk] * len(chunk)
        if chunkweights[chunk] < weightthreshold * totalweight:
            continue
        if chunkcounts[chunk] < MinimalCount:
            continue
        tempdict[chunk] = chunkweights[chunk]

    templist = sorted(tempdict.items(), key=lambda chunk: chunk[1], reverse=True)
    for stem, weight in templist:
        chunkweightlist.append((stem, weight, chunkcounts[stem]))

    # ----------------------------------------------------------------------------------------------------------------------------#
    return chunkweightlist


# ----------------------------------------------------------------------------------------------------------------------------#
def print_all_words(outfile, lexicon, WordCounts, WordToSig):
    # ----------------------------------------------------------------------------------------------------------------------------#
    words = WordCounts.keys()
    words.sort()
    print >> outfile, "***"
    print >> outfile, "\n--------------------------------------------------------------"
    print >> outfile, "Words"
    print >> outfile, "--------------------------------------------------------------"

    wordlist = WordToSig.keys()
    wordlist.sort()

    for word in words:
        if word in WordToSig:
            print >> outfile, '{0:<30}'.format(word), ":", WordCounts[word]
        else:
            print >> outfile, '  {0:<28}'.format(word), ":", WordCounts[word]
        for line in lexicon.WordBiographies[word]:
            print >>outfile, line
# ----------------------------------------------------------------------------------------------------------------------------#
def print_words(Lexicon, outfile_words, outfile, outfile_html, logfile,   ColumnWidth):
# ----------------------------------------------------------------------------------------------------------------------------#
    formatstring = "{0:15s} {1:30s} "
    Lexicon.sort_words()
    wordlist = Lexicon.Word_list_forward_sort
    print >> outfile_words, "***"
    print >> outfile_words, "\n" + "-" * 70
    print >> outfile_words, "Words"
    print >> outfile_words, "-" * 70
    MINLENGTH = 1
    for word in wordlist:
        print >>outfile_words, word
        #j = 0
        #for i in range(MINLENGTH,len(word)):
        #    if word[:i] in Lexicon.StemToSignature:
        #        print >>outfile_words,  word[j:i] + " ",
        #        j = i
        #print >>outfile_words, word[j:]
        if word in Lexicon.WordToSig:
            for n in range(len(Lexicon.WordToSig[word])):
                stem, sig = Lexicon.WordToSig[word][n]
                print >> outfile_words, "\t",formatstring.format(stem, sig)
        for line in Lexicon.WordBiographies[word]:
            print >>outfile_words, "  bio:",  line
    outfile_words.close()

    Lexicon.sort_words()
    print >> outfile, "***"
    print >> outfile, "\n" + "-" * 70
    print >> outfile, "Words and their signatures"
    print >> outfile, "-" * 70
    maxnumberofsigs = 0
    ambiguity_counts = dict()
    for word in wordlist:
        if word in Lexicon.WordToSig:
            ambiguity = len(Lexicon.WordToSig[word])
            if ambiguity not in ambiguity_counts:
                ambiguity_counts[ambiguity] = 0
            ambiguity_counts[ambiguity] += 1
            if len(Lexicon.WordToSig[word]) > maxnumberofsigs:
                maxnumberofsigs = len(Lexicon.WordToSig[word])
    print >> logfile, "How many words have multiple analyses?"
    print "   How many words have multiple analyses?"
    for i in range(maxnumberofsigs):
        if i in ambiguity_counts:
            print >> logfile, "{:4d}{:10,d}".format(i, ambiguity_counts[i])
            print             "{:4d}{:10,d}".format(i, ambiguity_counts[i])

    for word in wordlist:
        #current_left_edge = 0
        #broken_word = ""
        #Lexicon.break_word_by_suffixes(word)
        #for i in range(len(word)):
        #    if word[:i] in Lexicon.StemToWord:
        #        piece = word[current_left_edge:i]
        #        broken_word =  broken_word + " " +  piece
        #        current_left_edge = i
        #broken_word += " " + word[current_left_edge:]
        #print >>outfile, formatstring.format(word, broken_word)
        print >>outfile, word
        if word in Lexicon.WordToSig:
            for n in range(len(Lexicon.WordToSig[word])):
		    stem, sig = Lexicon.WordToSig[word][n]
		    print >> outfile, "\t",formatstring.format(stem, sig)
            print >> outfile

    start_an_html_file(outfile_html)
    start_an_html_div(outfile_html, class_type="wordlist")
    start_an_html_table(outfile_html)
    start_an_html_table_row(outfile_html)
    add_an_html_header_entry(outfile_html,"word")
    add_an_html_header_entry(outfile_html,"stem")
    add_an_html_header_entry(outfile_html,"signature")
    end_an_html_table_row(outfile_html)
    for word in wordlist:
        start_an_html_table_row(outfile_html)
        add_an_html_table_entry(outfile_html,word)
        if word in Lexicon.WordToSig:
            for n in range(len(Lexicon.WordToSig[word])):
                # sig = MakeStringFromSignature(WordToSig[word][n], ColumnWidth)
                stem, sig = Lexicon.WordToSig[word][n]
                add_an_html_table_entry(outfile_html,stem)
                add_an_html_table_entry(outfile_html,sig)
        end_an_html_table_row(outfile_html)

        print >> outfile_html
    end_an_html_table(outfile_html)
    end_an_html_div(outfile_html)
    end_an_html_file(outfile_html)


# ----------------------------------------------------------------------------------------------------------------------------#
def MakeStringFromSignature(sigset, maxlength):
    sig = "-".join(list(sigset))
    if len(sig) > maxlength - 2:
        sig = sig[:maxlength - 5] + "..."
    return sig


# ----------------------------------------------------------------------------------------------------------------------------#
def print_signature_extensions(outfile, logfile, DisplayList, SignatureToStems):
    print >> outfile, "--------------------------------------------------------------"
    print >> outfile, "        Signature extensions  "
    print >> outfile, "--------------------------------------------------------------"
    print "   Printing signature extensions."
    ListOfAlternations = list()
    ListOfAlternations2 = list()
    DictOfAlternations = dict()
    AlternationDict = dict()
    count = 0
    for (sig1, stemcount, robustness) in DisplayList:
        if count > 100:
            break
        count += 1
        for sig2, count2, robustness2 in DisplayList:
            if len(sig1) != len(sig2):
                continue
            (AlignedList1, AlignedList2, Differences) = Sig1ExtendsSig2(sig2, sig1, logfile)
            stemcount = len(SignatureToStems[sig2])
            if AlignedList1 != None:
                print >> outfile, "Signature extension:"
                print >> outfile, "{:35s}{:35s}{:35s}".format(AlignedList1, AlignedList2, Differences),


                if (False):
                    print >> outfile_SigExtensions, "A", FindSuffixesFlag, "{:35s}{:35s}{:35s}".format(AlignedList1,
                                                                                                       AlignedList2,
                                                                                                       Differences)
                    if len(AlignedList1) == 2:
                        alternation = (Differences[0], Differences[1])
                        ListOfAlternations.append((Differences[0], AlignedList2[0], Differences[1], AlignedList2[1]))
                        if alternation not in DictOfAlternations:
                            DictOfAlternations[alternation] = list()
                        DictOfAlternations[alternation].append(
                            (Differences[0], AlignedList2[0], Differences[1], AlignedList2[1]))

    ListOfAlternations.sort(key=lambda item: item.Count, reverse=True)
    for item in ListOfAlternations:
        if item.Count > 1:
            print >> outfile, item.display()

    print >> outfile, "*" * 50
    print >> outfile, "*" * 50

    ListOfAlternations.sort(key=lambda item: item.Alloforms[0].Form)
    for item in ListOfAlternations:
        if item.Count > 1:
            print >> outfile, item.Alloforms[0].Form, item.display()

    outfile.flush()

    return


# ----------------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------------#
class CProseReportLine:
    def __init__(self):
        self.MyList = list()
        self.MyLastItem = None

    def MakeReport(self):
        returnstring = "hello!"
        for item in self.MyList:
            returnstring += item.MyHead
            for item2 in self.MyTail:
                returnstring += " " + item2
        if self.MyLastItem:
            returnstring += item.MyHead
            for item2 in self.MyTail:
                returnstring += " " + item2
        return returnstring

    # ----------------------------------------------------------------------------------------------------------------------------#


class CReportLineItem:
    def __init__(self):
        self.MyHead = NULL
        self.MyTail = NULL


# ----------------------------------------------------------------------------------------------------------------------------#
class CDataGroup:
    def __init__(self, type, count):
        self.Type = type
        self.MyKeyDict = dict()
        self.Count = count

    def display(self):
        colwidth1 = 20
        colwidth2 = 40
        countstring = str(self.Count)
        returnstring = countstring + " " * (4 - len(countstring))
        string1 = ""
        string2 = ""

        ItemList = list(self.MyKeyDict.keys())
        # if there is a word-finally, put it in last place


        for i in range(len(ItemList)):
            phone = ItemList[i]
            if "\#" in self.MyKeyDict[phone]:
                # word final phoneme
                word_final_phone = ItemList[i]
                del ItemList[i]
                ItemList.append(word_final_phone)
        # if there is a "NIL", then put it in first place.
        for i in range(len(ItemList)):
            phone = ItemList[i]
            if phone == "nil":
                del ItemList[i]
                ItemList.insert(0, "nil")

        if self.Type == "KeyAndList":
            for key in ItemList:
                NULL_flag = False
                string1 = "[" + key + "]"
                string2 = ""
                returnstring += string1 + " " * (colwidth1 - len(string1))

                FirstItemFlag = True
                for item in self.MyKeyDict[key]:
                    if item == "NULL":
                        NULL_flag = True
                        continue
                    if FirstItemFlag:
                        string2 += "before "
                        FirstItemFlag = False
                    string2 += "/" + item + "/ "
                if NULL_flag:
                    if FirstItemFlag == False:
                        string2 += "and word-finally."
                    else:
                        string2 += "word-finally."
                returnstring += string2 + " " * (colwidth2 - len(string2))

        return returnstring

# ----------------------------------------------------------------------------------------------------------------------------#


 
# ----------------------------------------------------------------------------------------------------------------------------#
def print_signature_list_latex(this_file,
                           Lexicon,
                           DisplayList,
                           total_robustness,
                           lxalogfile,
                           affix_type):
    header1 = "\\documentclass[10pt]{article}" 
    header2 = "\\usepackage{booktabs}" 
    header3 = "\\usepackage{geometry}" 
    header4 = "\\usepackage{longtable}" 
    header5 = "\\geometry{verbose,letterpaper,lmargin=0.5in,rmargin=0.5in,tmargin=1in,bmargin=1in}"
    header6 = "\\begin{document} "
    starttab = "\\begin{longtable}{lllllllllll}"
    endtab = "\\end{longtable}"
    if affix_type == "suffix":
        FindSuffixesFlag = True
    else:
        FindSuffixesFlag = False
    print "   Printing signature file in latex."
    running_sum = 0.0
    print >>this_file, header1
    print >>this_file, header2
    print >>this_file, header3
    print >>this_file, header4
    print >>this_file, header5
    print >>this_file
    print >>this_file, header6
    print >>this_file
    print >>this_file, starttab
    print >> this_file,  " & Signature & Stem count & Robustness & Proportion of robustness\\\\ \\toprule"
 
    colwidth = 20
    DisplayList = sorted(DisplayList, key = lambda x: x[2], reverse=True)
    count = 1
    for sig, stemcount, robustness, stability, stem in DisplayList:
        running_sum += robustness
        robustness_proportion = float(robustness) / total_robustness
        running_sum_proportion = running_sum / total_robustness
        print >>this_file, count,  sig, " "*(colwidth-len(sig)), "&",  stemcount, "&",  robustness, "&", "{0:2.3f}".format(robustness_proportion), "\\\\"
        count += 1
    print >>this_file, endtab

    number_of_stems_per_line = 6
    stemlist = []
    print >>this_file
    print >>this_file
    for sig, stemcount, robustness, stability, stem in DisplayList:
        this_signature = Lexicon.Signatures[sig]
        print >>this_file, starttab
        print >>this_file, sig, "\\\\"
        n = 0
        stemlist = this_signature.get_stems()
        numberofstems = len(stemlist)
        for stem in stemlist:
            n += 1
            print >> this_file,  stem, " & ",
            if n % number_of_stems_per_line == 0:
                print >>this_file, "\\\\"
        print >>this_file, endtab
        print >>this_file

        print >>this_file
        print >>this_file
        print >>this_file, starttab
        numberofcolumns = 4
        colno = 0
        stemlist.sort(key = lambda x : Lexicon.StemCorpusCounts[x], reverse = True)
        for stem in stemlist:
            print >> this_file, stem, "&",  Lexicon.StemCorpusCounts[stem], "&",
            colno += 1
            if colno % numberofcolumns == 0:
                print >> this_file, "\\\\"
        print >> this_file, endtab	
        print >> this_file
        print >> this_file
    
    print >>this_file, "\\end{document}"	
    this_file.close()



