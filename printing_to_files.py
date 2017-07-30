import math
from class_alternation import *
from signaturefunctions import *
#from svg import *
from html_lxa import *
from IPython.display import display 


def print_html_report(outfile, this_lexicon, singleton_signatures, doubleton_signatures, DisplayList):
    leader=["Number of distinct words (types):" , "Total letter count in words " , "Number of signatures: ",
        "Number of singleton signatures (one stem): ", "Number of doubleton signatures (two stems): ",
        "Total number of letters in stems: ",  "Total number of affix letters: "]
    values=[ str(this_lexicon.total_word_count),  str(this_lexicon.word_letter_count), str(len(this_lexicon.SignatureStringsToStems)),
         str(singleton_signatures),   str(doubleton_signatures), str(this_lexicon.total_letters_in_stems), str(this_lexicon.total_affix_length_in_signatures) ]


    start_an_html_file( outfile)
    start_an_html_table(outfile)
    for lineno in range(7):
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



def initialize_filesdeprecated(this_lexicon, this_file, language):
    formatstring_initfiles1 = "{:40s}{:>15d}"
    formatstring_initfiles2 = "{:40s}{:>15s}"
    formatstring_initfiles3 = "{:40s}{:15.2f}"
    leader=list["Language:", "Total words:", "Minimum Stem Length", "Maximum Affix Length",
        "Minimum number of stems in signature:", "Total letter count in words:",
        "Average letters per word:"]
    if this_file == "console":
        print "Initialization."
        print formatstring_initfiles2.format(list[0], language)
        print formatstring_initfiles1.format(list[1],         this_lexicon.total_word_count)
        print formatstring_initfiles1.format(list[2],  this_lexicon.MinimumStemLength)
        print formatstring_initfiles1.format(list[3], this_lexicon.MaximumAffixLength)
        print formatstring_initfiles1.format(list[4], this_lexicon.MinimumStemsInaSignature)
        print formatstring_initfiles1.format(list[5], this_lexicon.word_letter_count)
        if this_lexicon.total_word_count > 0:
            print formatstring_initfiles3.format(list[6], this_lexicon.word_letter_count/ float(this_lexicon.total_word_count) )
    else:
        print >>this_file, "\nInitialization."
        print >> this_file, formatstring_initfiles2.format("Language: ", language)
        print >> this_file, formatstring_initfiles1.format("Total words:",         this_lexicon.total_word_count)
        print >> this_file, formatstring_initfiles1.format("Minimum Stem Length",  this_lexicon.MinimumStemLength)
        print >> this_file, formatstring_initfiles1.format("Maximum Affix Length", this_lexicon.MaximumAffixLength)
        print >> this_file, formatstring_initfiles1.format("Minimum Number of stems in signature: ",
                                                                                   this_lexicon.MinimumStemsInaSignature)
        print >> this_file, formatstring_initfiles1.format("Total letter count in words: ",
                                                                                    this_lexicon.word_letter_count)
        if this_lexicon.total_word_count > 0:
            print >> this_file, "{:40s}{:10.2f}".format("Average letters per word: ", this_lexicon.word_letter_count/ float(this_lexicon.total_word_count))


# ----------------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------------#
def initialize_files(this_lexicon, this_file, singleton_signatures, doubleton_signatures, DisplayList):
    formatstring_console = "   {:45s}{:10,d}"
    if this_file == "console":
        print
        print  formatstring_console.format("Number of words (types): ", this_lexicon.total_word_count)
        print  formatstring_console.format("Total letter count in words ", this_lexicon.word_letter_count)
        print  formatstring_console.format("Number of signatures: ", len(this_lexicon.SignatureStringsToStems))
        print  formatstring_console.format("Number of singleton signatures (one stem): ", singleton_signatures)
        print  formatstring_console.format("Number of doubleton signatures (two stems): ", doubleton_signatures)
        print  formatstring_console.format("Total number of letters in stems: ", this_lexicon.total_letters_in_stems)
        print  formatstring_console.format("Total number of affix letters in signatures: ", this_lexicon.total_affix_length_in_signatures)
        print  formatstring_console.format("Total letters in signatures: ",
                                           this_lexicon.total_letters_in_stems + this_lexicon.total_affix_length_in_signatures)
        print  formatstring_console.format("Number of analyzed words ", this_lexicon.number_of_analyzed_words)

        print  formatstring_console.format("Total number of letters in analyzed words ",
                                           this_lexicon.total_letters_in_analyzed_words)
    else:
        print >> this_file, "\nInitialization"
        print  >> this_file, "{:45s}{:10,d}".format("Number of words (corpus count): ", len(this_lexicon.WordList.mylist))
        print   >> this_file, "{:45s}{:10,d}".format("Total letter count in words ",
                                                     this_lexicon.word_letter_count)
        print   >> this_file, "{:45s}{:10,d}".format("Number of signatures: ", len(DisplayList))
        print   >> this_file, "{:45s}{:10,d}".format("Number of singleton signatures (one stem): ", singleton_signatures)
        print   >> this_file, "{:45s}{:10,d}".format("Number of doubleton signatures (two stems): ", doubleton_signatures)
        print   >> this_file, "{:45s}{:10,d}".format("Total number of letters in stems: ", this_lexicon.total_letters_in_stems)
        print   >> this_file, "{:45s}{:10,d}".format("Total number of affix letters: ",
                                                     this_lexicon.total_affix_length_in_signatures)
        print   >> this_file, "{:45s}{:10,d}".format("Total letters in signatures: ",
                                                     this_lexicon.total_letters_in_stems + this_lexicon.total_affix_length_in_signatures)
        print   >> this_file, "{:45s}{:10,d}".format("Number of analyzed words ", this_lexicon.number_of_analyzed_words)
        print   >> this_file, "{:45s}{:10,d}".format("Total number of letters in analyzed words ",
                                                     this_lexicon.total_letters_in_analyzed_words)


# ----------------------------------------------------------------------------------------------------------------------------#
def print_signature_list_1(this_file, DisplayList, stemcountcutoff, totalrobustness,SignatureToStems,StemCorpusCounts,lxalogfile,FindSuffixesFlag):
    print "   Printing signature file."
    runningsum = 0.0
    formatstring1 = '{0:25}{1:>10s} {2:>15s} {3:>25s} {4:>20s}{5:>20s} '
    formatstring2 = '{0:<30}{1:5d} {2:15d} {3:25.3%} {4:20.3%}{5:>20s}'
    print >> this_file, "\n" + "-" * 150
    print >> this_file, formatstring1.format("Signature", "Stem count", "Robustness", "Proportion of robustness",
                                             "Running sum", "Example")
    print >> this_file, "-" * 150



    DisplayList = sorted(DisplayList, lambda x, y: cmp(x[2], y[2]), reverse=True)

    for sig, stemcount, robustness, stem in DisplayList:
        runningsum += robustness
        if stemcount < stemcountcutoff:
            break;
        else:
            robustnessproportion = float(robustness) / totalrobustness
            runningsumproportion = runningsum / totalrobustness
            print >> this_file, formatstring2.format(sig, stemcount, robustness, robustnessproportion,
                                                     runningsumproportion, stem)
    print >> this_file, "-" * 60



    numberofstemsperline = 6
    stemlist = []
    reversedstemlist = []
    count = 0
    print >> this_file, "*** Stems in each signature"
    for sig, stemcount, robustness, stem in DisplayList:
        print >> this_file, "\n" + "=" * 45, '{0:30s} \n'.format(sig)
        n = 0

        stemlist = SignatureToStems[sig].keys()
        stemlist.sort()
        numberofstems = len(stemlist)
        for stem in stemlist:
            n += 1
            print >> this_file, '{0:12s}'.format(stem),
            if n == numberofstemsperline:
                n = 0
                print >> this_file
        print >> this_file, "\n" + "-" * 25

        stemlist.sort(key=lambda stem: StemCorpusCounts[stem])
        longeststemlength = 0
        for stem in stemlist:
            if len(stem) > longeststemlength:
                longeststemlength = len(stem)
        columnwidth = longeststemlength
        numberofcolumns = 4
        colno = 0
        for stem in stemlist:
            stemcount = str(StemCorpusCounts[stem])
            print >> this_file, stem, " " * (columnwidth - len(stem)), stemcount, " " * (5 - len(stemcount)),
            colno += 1
            if colno == numberofcolumns:
                colno = 0
                print >> this_file

        print >> this_file, "\n" + "-" * 25

        # ------------------- New -----------------------------------------------------------------------------------
        howmany = 5
        print >> this_file, "Average count of top", howmany, " stems:", AverageCountOfTopStems(howmany, sig,
                                                                                               SignatureToStems,
                                                                                               StemCorpusCounts,
                                                                                               lxalogfile)

        # ------------------------------------------------------------------------------------------------------
        bitsPerLetter = 5
        wordlist = makeWordListFromSignature(sig, SignatureToStems[sig])
        (a, b, c) = findWordListInformationContent(wordlist, bitsPerLetter)
        (d, e, f) = findSignatureInformationContent(SignatureToStems, sig, bitsPerLetter)
        formatstring = '%35s %10d  '
        formatstringheader = '%35s %10s    %10s  %10s'
        print >> this_file, formatstringheader % ("", "Phono", "Ordering", "Total")
        print >> this_file, formatstring % ("Letters in words if unanalyzed:", a)
        print >> this_file, formatstring % ("Letters as analyzed:", d)
        # ------------------------------------------------------------------------------------------------------
        howmanytopstems = 5

        print >> this_file, "\n-------------------------"
        print >> this_file, "Entropy-based stability: ", StableSignature(stemlist, FindSuffixesFlag)
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



    this_file.close()

def print_signature_list_1_html(this_file, DisplayList, stemcountcutoff, totalrobustness):
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

    for sig, stemcount, robustness, stem in DisplayList:

        runningsum += robustness
        if stemcount < stemcountcutoff:
            break;
        else:
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

def print_signatures_to_svg (outfile_html, DisplayList,SignatureToStems,FindSuffixesFlag):
    this_page = Page()

    DisplayList = sorted(DisplayList, lambda x, y: cmp(x[2], y[2]), reverse=True)
    this_page.start_an_html_file(outfile_html)
    column_counts = dict();
    for signo in range(len(DisplayList)):
            (sig,stemcount,robustness,stem) = DisplayList[signo]
            stemlist = SignatureToStems[sig].keys()
	    row_no= sig.count("=")+1
            if row_no not in column_counts:
		column_counts[row_no] = 1
	    else:
 		column_counts[row_no] += 1
	    col_no = column_counts[row_no]
	    radius_guide = len(stemlist) * row_no
	    this_page.print_signature (outfile_html, sig, radius_guide, row_no, col_no)

            #if FindSuffixesFlag:
            #    signature_box = SignatureBox(stemlist, affixlist,FindSuffixesFlag)
            #else:
            #    signature_box=SignatureBox(affixlist,stemlist, FindSuffixesFlag)
            #signature_box.print_signature_box(outfile_html, this_page, 300,300)
    this_page.end_an_html_file(outfile_html)
    outfile_html.close()

# ----------------------------------------------------------------------------------------------------------------------------#
def print_complex_signature_to_svg (outfile_html, sig, lexicon):
# a complex signature is one where the "stem" column is a stack, of several groups, including a stem list,
# and also a list of analyzed stems with their signatures.
    this_page = Page()

    this_page.start_an_html_file(outfile_html)
    stemlist = lexicon.SignatureToStems[sig].keys()
    affixlist = sig.split("=")
    complex_signature_box = ComplexSignatureBox(stemlist, affixlist)
    signature_box.print_signature_box(outfile_html, this_page, 300,300)
    this_page.end_an_html_file(outfile_html)
    outfile_html.close()



# ----------------------------------------------------------------------------------------------------------------------------#
def print_signature_list_3(this_file, signature_feeding_outfile, lxalogfile, Lexicon,  DisplayList, stemcountcutoff, totalrobustness, SignatureToStems, StemCorpusCounts, suffix_flag):

# this function not used, should be DELETED.


    numberofstemsperline = 6
    stemlist = []
    reversedstemlist = []
    count = 0
    print >> this_file, "*** Stems in each signature"
    for sig, stemcount, robustness, stem in DisplayList:
        print >> this_file, "\n" + "=" * 45, '{0:30s} \n'.format(sig)
        n = 0

        stemlist = SignatureToStems[sig].keys()
        stemlist.sort()
        numberofstems = len(stemlist)
        for stem in stemlist:
            n += 1
            print >> this_file, '{0:12s}'.format(stem),
            if n == numberofstemsperline:
                n = 0
                print >> this_file
        print >> this_file, "\n" + "-" * 25

        stemlist.sort(key=lambda stem: StemCorpusCounts[stem])
        longeststemlength = 0
        for stem in stemlist:
            if len(stem) > longeststemlength:
                longeststemlength = len(stem)
        columnwidth = longeststemlength
        numberofcolumns = 4
        colno = 0
        for stem in stemlist:
            stemcount = str(StemCorpusCounts[stem])
            print >> this_file, stem, " " * (columnwidth - len(stem)), stemcount, " " * (5 - len(stemcount)),
            colno += 1
            if colno == numberofcolumns:
                colno = 0
                print >> this_file

        print >> this_file, "\n" + "-" * 25

        # ------------------- New -----------------------------------------------------------------------------------
        howmany = 5
        print >> this_file, "Average count of top", howmany, " stems:", AverageCountOfTopStems(howmany, sig,
                                                                                               SignatureToStems,
                                                                                               StemCorpusCounts,
                                                                                               lxalogfile)

        # ------------------------------------------------------------------------------------------------------
        bitsPerLetter = 5
        wordlist = makeWordListFromSignature(sig, SignatureToStems[sig])
        (a, b, c) = findWordListInformationContent(wordlist, bitsPerLetter)
        (d, e, f) = findSignatureInformationContent(SignatureToStems, sig, bitsPerLetter)
        formatstring = '%35s %10d  '
        formatstringheader = '%35s %10s    %10s  %10s'
        print >> this_file, formatstringheader % ("", "Phono", "Ordering", "Total")
        print >> this_file, formatstring % ("Letters in words if unanalyzed:", a)
        print >> this_file, formatstring % ("Letters as analyzed:", d)
        # ------------------------------------------------------------------------------------------------------
        howmanytopstems = 5

        print >> this_file, "\n-------------------------"
        print >> this_file, "Entropy-based stability: ", StableSignature(stemlist, suffix_flag)
        print >> this_file, "\n", "High frequency possible affixes \nNumber of stems: ", len(stemlist)
        formatstring = '%10s    weight: %5d count: %5d %2s'
        peripheralchunklist = find_N_highest_weight_affix(stemlist, suffix_flag)

        for item in peripheralchunklist:
            if item[2] >= numberofstems * 0.9:
                flag = "**"
            else:
                flag = ""
            print >> this_file, formatstring % (item[0], item[1], item[2], flag)


    this_file.close()


# ----------------------------------------------------------------------------------------------------------------------------#
# We find signatures which are more finely divided by a later signature (the later signature is shorter, with a longer stem).
# Signature feeding 
def print_signature_list_2(signature_feeding_outfile, lxalogfile, Lexicon,  DisplayList, stemcountcutoff, totalrobustness, SignatureToStems, StemCorpusCounts, suffix_flag):

    start_an_html_file (signature_feeding_outfile)
    stemlist = []

    for sig, stemcount, robustness, stem in DisplayList:
        stemlist = SignatureToStems[sig]
        numberofstems = len(stemlist)
        temp_signatures_with_stems = dict()

        # test whether there will be any entries here:
        PrintThisSignatureFlag=False
        for stem in stemlist:
	    for affix in sig.split("="):
		if suffix_flag==True:	
		    if affix == "NULL":
			word = stem
		    else:
			word = stem + affix
		word = remove_parentheses(word)
                for pair in Lexicon.WordToSig[word]:
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

	# for all the words associated with each stem, find if there is another signature they all belong to.
	# If there is, we say that other signature FEEDS this one (sig)
	temp_signatures_with_stems = dict()
        for stem in stemlist:
	    list_of_sets_of_signatures = list()
            feeding_signatures = set()
            for affix in sig.split("="):
		if suffix_flag == True:
		    if affix == "NULL":
			word = stem
		    else:
			word = stem + affix	
		word = remove_parentheses(word)
		list_of_sets_of_signatures.append(set(Lexicon.get_all_signatures(word)))
	    feeding_signatures = set.intersection(*list_of_sets_of_signatures)
	    feeding_signatures.remove(sig)
	    if len(feeding_signatures) > 0:
		for sig1 in feeding_signatures:
		    if sig1 not in temp_signatures_with_stems:
			temp_signatures_with_stems[sig1] = list()
		    other_stem = Lexicon.get_stem_from_word_and_signature(word, sig1)
		    diff = len(stem) - len(other_stem)
                    display = other_stem + "/" + stem[-1*diff:]
		    temp_signatures_with_stems[sig1].append(display) 
		    		


        number_of_columns = 7
        colno=0
        start_an_html_div(signature_feeding_outfile, class_type="largegroup2")
        start_an_html_table(signature_feeding_outfile)
        signature_list= sorted(temp_signatures_with_stems , key = lambda x:len(temp_signatures_with_stems[x]), reverse=True  )
        for sig1  in signature_list:
	    start_an_html_table(signature_feeding_outfile)
            start_an_html_table_row(signature_feeding_outfile)
            add_an_html_table_entry(signature_feeding_outfile, sig1)
            end_an_html_table_row(signature_feeding_outfile)
            colno=0
            for chunk in temp_signatures_with_stems[sig1]:
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

        end_an_html_table(signature_feeding_outfile)
        end_an_html_div(signature_feeding_outfile)

        end_an_html_div(signature_feeding_outfile)

    signature_feeding_outfile.close()

# ----------------------------------------------------------------------------------------------------------------------------#
def print_unlikelysignatures(this_file, signatures, ColumnWidth):
    print "   Printing unlikely signatures file."
    runningsum = 0.0
    formatstring1 = '{0:<70}{1:>10s}'
    # formatstring2 = '{:<70}{:10d}  '
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
def print_suffixes(outfile, Suffixes):
    print >> outfile, "--------------------------------------------------------------"
    print >> outfile, "        Suffixes "
    print >> outfile, "--------------------------------------------------------------"
    print "   Printing suffixes."
    suffixlist = list(Suffixes.keys())
    suffixlist.sort(key=lambda suffix: Suffixes[suffix], reverse=True)
    for suffix in suffixlist:
        if suffix == "":
                suffix = "NULL"
        print >> outfile, "{:12s}{:9,d}".format(suffix, Suffixes[suffix])

    suffixlist.sort()
    for suffix in suffixlist:
        if suffix == "":
                suffix = "NULL"
        print >> outfile, "{:12s}{:9,d}".format(suffix, Suffixes[suffix])

    outfile.close()
    return suffixlist


# ----------------------------------------------------------------------------------------------------------------------------#
def print_stems(outfile1, outfile_stems_and_unanalyzed_words, Lexicon, suffixlist):
    StemToWord = Lexicon.StemToWord
    StemToSignature = Lexicon.StemToSignature
    WordCounts = Lexicon.WordCounts
    stems = StemToWord.keys()
    stems.sort()
    print >> outfile1, "--------------------------------------------------------------"
    print >> outfile1, "---  Stems and their words"
    print >> outfile1, "--------------------------------------------------------------"
    print "   Printing stems and their words."
    StemCounts = dict()
    for stem in stems:
        print >> outfile1, '{:15}'.format(stem),
        wordlist = StemToWord[stem].keys()
        wordlist.sort()
        stemcount = 0
        for word in wordlist:
            stemcount += WordCounts[word]
        StemCounts[stem] = stemcount
        print    >> outfile1, '{:5d}'.format(stemcount), '; ',
        stemcount = float(stemcount)
        for word in wordlist:
            wordcount = WordCounts[word]
            print >> outfile1, '{:10}{:4n} '.format(word, wordcount),

        print >> outfile1

    # Add to wordlist all the words that have no analysis

    stems_and_unanalyzed_words = deepcopy(stems)
    for word in WordCounts:
	if word not in Lexicon.WordToSig:
	    stems_and_unanalyzed_words.append(word + "*")
            #print "printing to files 387", word
    stems_and_unanalyzed_words.sort()
    print >> outfile_stems_and_unanalyzed_words, "--------------------------------------------------------------"
    print >> outfile_stems_and_unanalyzed_words, "---  Stems and unanalyzed words"
    print >> outfile_stems_and_unanalyzed_words, "--------------------------------------------------------------"
    print "   Printing stems and their words along with unanalyzed words."
    StemCounts = dict()
    for item in stems_and_unanalyzed_words:
        # print >> outfile_stems_and_unanalyzed_words, '{:15}'.format(item),
	if item in stems:
                stem = item
		print >> outfile_stems_and_unanalyzed_words, "{:15s}".format(stem),
		wordlist = StemToWord[stem].keys()
		wordlist.sort()
		stemcount = 0
		for word in wordlist:
		    stemcount += WordCounts[word]
		StemCounts[stem] = stemcount
		print    >> outfile_stems_and_unanalyzed_words, '{:5d}'.format(stemcount), '; ',
		stemcount = float(stemcount)
		for word in wordlist:
		    wordcount = WordCounts[word]
		    print >> outfile_stems_and_unanalyzed_words, '{:15}{:4n} {:7.1%} '.format(word, wordcount, wordcount / stemcount),
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
def findSignatureInformationContent(signatures, signature, bitsPerLetter):
    # ----------------------------------------------------------------------------------------------------------------------------#
    stemSetPhonoInformation = 0
    stemSetOrderingInformation = 0
    affixPhonoInformation = 0
    affixOrderingInformation = 0
    letters = 0
    stemset = signatures[signature]
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
def StableSignature(stemlist, MakeSuffixesFlag):
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
def print_all_words(outfile, WordCounts, WordToSig):
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

# ----------------------------------------------------------------------------------------------------------------------------#
def print_words(outfile, outfile_html, logfile,words, WordToSig, ColumnWidth):
    # ----------------------------------------------------------------------------------------------------------------------------#

    words.sort()
    print >> outfile, "***"
    print >> outfile, "\n--------------------------------------------------------------"
    print >> outfile, "Words and their signatures"
    print >> outfile, "--------------------------------------------------------------"
    maxnumberofsigs = 0
    ambiguity_counts = dict()
    for word in WordToSig:
        ambiguity = len(WordToSig[word])
        if ambiguity not in ambiguity_counts:
            ambiguity_counts[ambiguity] = 0
        ambiguity_counts[ambiguity] += 1
        if len(WordToSig[word]) > maxnumberofsigs:
            maxnumberofsigs = len(WordToSig[word])
    print >> logfile, "How many words have multiple analyses?"
    print "   How many words have multiple analyses?"
    for i in range(maxnumberofsigs):
        if i in ambiguity_counts:
            print >> logfile, "{:4d}{:10,d}".format(i, ambiguity_counts[i])
            print             "{:4d}{:10,d}".format(i, ambiguity_counts[i])

    wordlist = WordToSig.keys()
    wordlist.sort()


    formatstring = "{0:15s} {1:30s} "

    for word in wordlist:
        print >> outfile, '{0:15}'.format(word), ":",
        for n in range(len(WordToSig[word])):
            # sig = MakeStringFromSignature(WordToSig[word][n], ColumnWidth)
            stem, sig = WordToSig[word][n]
            print >> outfile, formatstring.format(stem, sig),
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
        for n in range(len(WordToSig[word])):
            # sig = MakeStringFromSignature(WordToSig[word][n], ColumnWidth)
            stem, sig = WordToSig[word][n]
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
