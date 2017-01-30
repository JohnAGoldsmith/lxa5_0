import math 
from signaturefunctions import *
from class_alternation import *


def initialize_files1(this_lexicon, this_file,language ):
    formatstring_initfiles1 = "{:40s}{:>15d}"
    formatstring_initfiles2 = "{:40s}{:>15s}"
    formatstring_initfiles3 = "{:40s}{:15.2f}"
    if this_file == "console":
        print formatstring_initfiles2.format("Language: ", language)
        print formatstring_initfiles1.format("Total words:", len(this_lexicon.WordList.mylist))
        print formatstring_initfiles1.format("Minimum Stem Length", this_lexicon.MinimumStemLength)
        print formatstring_initfiles1.format("Maximum Affix Length", this_lexicon.MaximumAffixLength )
        print formatstring_initfiles1.format("Minimum Number of stems in signature: ", this_lexicon.MinimumStemsInaSignature)
        print formatstring_initfiles1.format("Total letter count in words: ", this_lexicon.TotalLetterCountInWords)
        print formatstring_initfiles3.format("Average letters per word: ",3.0) #(float(this_lexicon.TotalLetterCountInWords))/len(this_lexicon.WordList.mylist))
    else:
        print >>this_file, "{:40s}{:>15s}".format("Language: ", language)
        print >>this_file, "{:40s}{:10,d}".format("Total words:", len(this_lexicon.WordList.mylist))
        print >>this_file, "{:40s}{:>10,}".format("Minimum Stem Length", this_lexicon.MinimumStemLength)
        print >>this_file, "{:40s}{:>10,}".format("Maximum Affix Length", this_lexicon.MaximumAffixLength )
        print >>this_file, "{:40s}{:>10,}".format("Minimum Number of stems in signature: ", this_lexicon.MinimumStemsInaSignature)
        print >>this_file, "{:40s}{:10,d}".format("Total letter count in words: ", this_lexicon.TotalLetterCountInWords)
        print >>this_file, "{:40s}{:10.2f}".format("Average letters per word: ",  float(this_lexicon.TotalLetterCountInWords)/len(this_lexicon.WordList.mylist))

# ----------------------------------------------------------------------------------------------------------------------------# 
# ----------------------------------------------------------------------------------------------------------------------------#
def initialize_files(this_lexicon, this_file,singleton_signatures,doubleton_signatures, DisplayList ):
    formatstring_console = "   {:45s}{:10,d}"
    if this_file == "console":
        print  formatstring_console.format("Number of words: ", len(this_lexicon.WordList.mylist))
        print  formatstring_console.format("Total letter count in words ", this_lexicon.TotalLetterCountInWords)
        print  formatstring_console.format("Number of signatures: ", len(DisplayList))
        print  formatstring_console.format("Number of singleton signatures: ", singleton_signatures)
        print  formatstring_console.format("Number of doubleton signatures: ", doubleton_signatures)
        print  formatstring_console.format("Total number of letters in stems: ", this_lexicon.LettersInStems)
        print  formatstring_console.format("Total number of affix letters: ", this_lexicon.AffixLettersInSignatures)
        print  formatstring_console.format("Total letters in signatures: ", this_lexicon.LettersInStems + this_lexicon.AffixLettersInSignatures)
        print  formatstring_console.format("Number of analyzed words ", this_lexicon.NumberOfAnalyzedWords)
        print  formatstring_console.format("Total number of letters in analyzed words ", this_lexicon.LettersInAnalyzedWords)
    else:
        print  >> this_file,  "{:45s}{:10,d}".format("Number of words: ", len(this_lexicon.WordList.mylist))
        print   >> this_file, "{:45s}{:10,d}".format("Total letter count in words ", this_lexicon.TotalLetterCountInWords)
        print   >> this_file, "{:45s}{:10,d}".format("Number of signatures: ", len(DisplayList))
        print   >> this_file, "{:45s}{:10,d}".format("Number of singleton signatures: ", singleton_signatures)
        print   >> this_file, "{:45s}{:10,d}".format("Number of doubleton signatures: ", doubleton_signatures)
        print   >> this_file, "{:45s}{:10,d}".format("Total number of letters in stems: ", this_lexicon.LettersInStems)
        print   >> this_file, "{:45s}{:10,d}".format("Total number of affix letters: ", this_lexicon.AffixLettersInSignatures)
        print   >> this_file, "{:45s}{:10,d}".format("Total letters in signatures: ", this_lexicon.LettersInStems + this_lexicon.AffixLettersInSignatures)
        print   >> this_file, "{:45s}{:10,d}".format("Number of analyzed words ", this_lexicon.NumberOfAnalyzedWords)
        print   >> this_file, "{:45s}{:10,d}".format("Total number of letters in analyzed words ", this_lexicon.LettersInAnalyzedWords)
# ----------------------------------------------------------------------------------------------------------------------------# 
def print_signature_list_1(this_file, DisplayList,stemcountcutoff, totalrobustness):
    print "   Printing signature file."
    runningsum = 0.0
    formatstring1 = '{0:<70}{1:>10s} {2:>15s} {3:>25s} {4:>20s} '
    formatstring2 = '{:<70}{:10d} {:15d} {:25.3%} {:20.3%}'
    print >> this_file, "\n" + "-" * 150
    print >> this_file, formatstring1.format("Signature", "Stem count", "Robustness", "Proportion of robustness", "Running sum")
    print >> this_file, "-" * 150      
    DisplayList = sorted(DisplayList, lambda x, y: cmp(x[2], y[2]), reverse=True)
     
    for sig, stemcount, robustness in DisplayList:
        runningsum+=robustness
        if stemcount < stemcountcutoff:
            break;
        else:
            robustnessproportion = float(robustness) / totalrobustness
            runningsumproportion = runningsum/totalrobustness
            print >> this_file, formatstring2.format(sig, stemcount, robustness,robustnessproportion, runningsumproportion )
    print >> this_file, "-"*60
# ----------------------------------------------------------------------------------------------------------------------------#
def print_signature_list_2(this_file, DisplayList,stemcountcutoff, totalrobustness, SignatureToStems, StemCounts, suffix_flag):
    numberofstemsperline = 6
    stemlist = []
    reversedstemlist = []
    count = 0
    print >> this_file, "*** Stems in each signature"
    for sig, stemcount, robustness in DisplayList:
        #if encoding == "utf8":
        #        print >> this_file, "\n"+"="*45 , sig, "\n"
        #else:
        print >> this_file, "\n"+"="*45, '{0:30s} \n'.format(sig)
        n = 0

        stemlist =  SignatureToStems[sig].keys()
        stemlist.sort()
        numberofstems = len(stemlist)
        for stem in stemlist:
                n += 1
                print >> this_file, '{0:12s}'.format(stem),
                if n == numberofstemsperline:
                    n = 0
                    print >> this_file
        print >> this_file, "\n" + "-"*25
        # ------------------- New -----------------------------------------------------------------------------------
        howmany = 5     
        print >>this_file, "Average count of top",howmany, " stems:" , AverageCountOfTopStems(howmany, sig, SignatureToStems, StemCounts)
            

        # ------------------------------------------------------------------------------------------------------
        bitsPerLetter = 5
        wordlist = makeWordListFromSignature(sig, SignatureToStems[sig])
        (a, b, c) = findWordListInformationContent(wordlist, bitsPerLetter)
        (d, e, f) = findSignatureInformationContent(SignatureToStems, sig, bitsPerLetter)
        formatstring = '%35s %10d  '
        formatstringheader = '%35s %10s    %10s  %10s'
        print >> this_file, formatstringheader % ("", "Phono", "Ordering", "Total")
        print >> this_file, formatstring % ("Letters in words if unanalyzed:", a   )
        print >> this_file, formatstring % ("Letters as analyzed:", d)
        # ------------------------------------------------------------------------------------------------------
        howmanytopstems = 5
            


        print >> this_file, "\n-------------------------"
        print >> this_file, "Entropy-based stability: ", StableSignature(stemlist,suffix_flag)
        print >> this_file, "\n", "High frequency possible affixes \nNumber of stems: ", len(stemlist)
        formatstring = '%10s    weight: %5d count: %5d %2s'
        peripheralchunklist = find_N_highest_weight_affix(stemlist, suffix_flag)

        for item in peripheralchunklist:
            if item[2] >= numberofstems * 0.9:
                    flag = "**"
            else:
                    flag = ""
            print >> this_file, formatstring % (item[0], item[1], item[2], flag)
# ----------------------------------------------------------------------------------------------------------------------------#
def print_suffixes(outfile, Suffixes ):
        print >>outfile,  "--------------------------------------------------------------"
        print >>outfile , "        Suffixes "
        print >>outfile,  "--------------------------------------------------------------"
        print "   Printing suffixes."
        suffixlist = list(Suffixes.keys())
        suffixlist.sort(key=lambda  suffix:Suffixes[suffix], reverse=True)
        for suffix in suffixlist:
            print >>outfile,"{:8s}{:9,d}".format(suffix, Suffixes[suffix])
        return suffixlist
# ----------------------------------------------------------------------------------------------------------------------------#
def print_stems(outfile1, outfile2, StemToWord, StemToSignature, WordCounts, suffixlist): 
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
                stemcount +=  WordCounts[word]
            StemCounts[stem]=stemcount
            print    >> outfile1, '{:5d}'.format(stemcount),'; ',
            stemcount = float(stemcount)    
            for word in wordlist:
                wordcount =  WordCounts[word]
                print >> outfile1 , '{:15}{:4n} {:7.1%} '.format(word,wordcount, wordcount/stemcount),
            print >> outfile1 

            # We print a list of stems with their words (and frequencies) in which only those suffixes which are among the K most frequent suffixes,
            # in order to use visualization methods that put soft limits on the number of dimensions they can handle well.
            
            threshold_for_top_affixes = 25 # this will give us one more than that number, since we are zero-based counting.
            top_affixes = suffixlist[0:threshold_for_top_affixes]
        print >> outfile2, "\n--------------------------------------------------------------"
        print >> outfile2, "---  Stems and their words with high frequency affixes"
        print >> outfile2, "--------------------------------------------------------------"
        print "   Printing stems and their words, but only with high frequency affixes."
        print >>outfile2, "---\n--- Only signatures with these affixes: ", top_affixes
        print >>outfile2, "---"
        StemCounts = dict()
        for stem in stems:
            signature = StemToSignature[stem]
            for affix in signature:
                if affix not in top_affixes:
                    continue 
            print >> outfile2, '{:15}'.format(stem),
            wordlist = StemToWord[stem].keys()
            wordlist.sort()
            stemcount = 0
            for word in wordlist:
                stemcount += WordCounts[word]
            StemCounts[stem]=stemcount
            print    >> outfile2, '{:5d}'.format(stemcount),'; ',
            stemcount = float(stemcount)    
            for word in wordlist:
                wordcount = WordCounts[word]
                print >> outfile2, '{:15}{:4n} {:7.1%} '.format(word,wordcount, wordcount/stemcount),
            print >> outfile2        
            #print top_affixes

# ----------------------------------------------------------------------------------------------------------------------------#
def AverageCountOfTopStems(howmany, sig, Signatures, StemCounts):
	stemlist = list(Signatures[sig])
	countlist = []
	count = 0
	average = 0
	for stem in stemlist:
		countlist.append(StemCounts[stem])
	countlist = sorted(countlist, reverse=True)
	if len(countlist) < howmany:
		howmany = len(countlist)
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
	for word  in wordlist:
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
def StableSignature(stemlist,MakeSuffixesFlag):
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
	# threshold 		= 50
	weightthreshold = 0.02
	# permittedexceptions 	= 2
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
			for width in range(1, maximalchunksize + 1):  # width is the size (in letters) of the suffix being considered
				chunk = word[-1 * width:]
				if not chunk in chunkcounts.keys():
					chunkcounts[chunk] = 1
				else:
					chunkcounts[chunk] += 1
	else:
		for word in wordlist:
			for width in range(1, maximalchunksize + 1):  # width is the size (in letters) of the prefix being considered
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
def print_allwords(outfile, WordCounts ): 
# ----------------------------------------------------------------------------------------------------------------------------#
    words = WordCounts.keys()
    words.sort()
    print >> outfile, "***"
    print >> outfile, "\n--------------------------------------------------------------"
    print >> outfile, "Words"  
    print >> outfile, "--------------------------------------------------------------"
     
    wordlist =  WordToSig.keys()
    wordlist.sort()

    for word in words:
        print >> outfile, '{0:<30}'.format(word), ":", WordCounts[word]
        
# ----------------------------------------------------------------------------------------------------------------------------#
def print_words(outfile, logfile, WordToSig,ColumnWidth ): 
# ----------------------------------------------------------------------------------------------------------------------------#
    words = WordToSig.keys()
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
            #print word, maxnumberofsigs
    print >> logfile, "How many words have multiple analyses?"
    print "   How many words have multiple analyses?"
    for i in range(maxnumberofsigs):
        if i in ambiguity_counts:
            print >> logfile, "{:4d}{:10,d}".format(i, ambiguity_counts[i])
            print             "{:4d}{:10,d}".format(i, ambiguity_counts[i])
     

    wordlist =  WordToSig.keys()
    wordlist.sort()

    for word in wordlist:
        print >> outfile, '{0:<30}'.format(word), ":",
        for n in range(len(WordToSig[word])):               
            #sig = MakeStringFromSignature(WordToSig[word][n], ColumnWidth)
            sig = WordToSig[word][n]
            print >> outfile, sig + " " * (ColumnWidth - len(sig)),
        print >> outfile

# ----------------------------------------------------------------------------------------------------------------------------#
def MakeStringFromSignature(sigset, maxlength):
	sig = "-".join(list(sigset))
	if len(sig) >  maxlength-2:
		sig = sig[:maxlength-5] + "..."
	return sig
# ----------------------------------------------------------------------------------------------------------------------------#
def print_signature_extensions(outfile, logfile, DisplayList,SignatureToStems ):
    print >>outfile,  "--------------------------------------------------------------"
    print >>outfile, "        Signature extensions  "
    print >>outfile,  "--------------------------------------------------------------"
    print "   Printing signature extensions."
    ListOfAlternations = list()
    ListOfAlternations2 = list()
    DictOfAlternations = dict()
    AlternationDict = dict()
    count = 0
    for (sig1,stemcount,robustness)  in  DisplayList:
        if count > 100:
            break
        count += 1
        for sig2, count2, robustness2 in DisplayList:
            if len(sig1) != len(sig2) :
                continue
            (AlignedList1, AlignedList2, Differences) = Sig1ExtendsSig2(sig2,sig1,logfile)
            stemcount = len(SignatureToStems[sig2])
            if  AlignedList1 != None:
                print >>outfile, "{:35s}{:35s}{:35s}".format(AlignedList1, AlignedList2, Differences), 
                #Make CAlternation:
                this_alternation = CAlternation(stemcount)
                for i  in range(len(AlignedList1)):
                    this_alloform = CAlloform(Differences[i], AlignedList2[i], stemcount)
                    this_alternation.AddAlloform (this_alloform)
                print  >>outfile, this_alternation.display()
                ListOfAlternations.append(this_alternation)

                if (False):
                    print >>outfile_SigExtensions, "A", FindSuffixesFlag, "{:35s}{:35s}{:35s}".format(AlignedList1, AlignedList2, Differences)
                    if len(AlignedList1)==2:
                        alternation = (Differences[0],  Differences[1])
                        ListOfAlternations.append((Differences[0], AlignedList2[0], Differences[1], AlignedList2[1]))
                        if alternation not in DictOfAlternations:
                            DictOfAlternations[alternation]= list()
                        DictOfAlternations[alternation].append((Differences[0], AlignedList2[0], Differences[1], AlignedList2[1]))

    ListOfAlternations.sort(key=lambda item:item.Count, reverse=True)
    for item in ListOfAlternations:
        if item.Count > 1:
            print >>outfile, item.display()

    print >>outfile, "*"*50
    print >>outfile, "*"*50


    ListOfAlternations.sort(key=lambda item:item.Alloforms[0].Form)
    for item in ListOfAlternations:
            if item.Count > 1:
                print >>outfile, item.Alloforms[0].Form, item.display()


    outfile.flush()

    return


# ----------------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------------#
class CProseReportLine:
    def __init__(self):
        self.MyList = list()
        self.MyLastItem = None

    def MakeReport(self):
        returnstring="hello!"
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
    def __init__(self, type,count):
        self.Type = type
        self.MyKeyDict = dict()
        self.Count = count


    def display(self):
        colwidth1 = 20
        colwidth2 = 40
        countstring = str(self.Count)
        returnstring = countstring + " "*(4-len(countstring))
        string1 = ""
        string2 =""

        ItemList = list(self.MyKeyDict.keys())
        #if there is a word-finally, put it in last place


        for i in range(len(ItemList)):
            phone = ItemList[i]
            if "\#" in self.MyKeyDict[phone]:
                #word final phoneme
                word_final_phone = ItemList[i]
                del ItemList[i]
                ItemList.append(word_final_phone)
        #if there is a "NIL", then put it in first place.
        for i in range(len(ItemList)):
            phone=ItemList[i]
            if phone== "nil":
                del ItemList[i]
                ItemList.insert(0,"nil")



        if self.Type == "KeyAndList":
            for key in ItemList:
                NULL_flag = False
                string1 = "[" + key + "]" 
                string2 = ""
                returnstring += string1 + " "*(colwidth1-len(string1))
               
                FirstItemFlag= True
                for item in self.MyKeyDict[key]:
                    if item == "NULL":
                        NULL_flag = True
                        continue
                    if FirstItemFlag:
                        string2 += "before " 
                        FirstItemFlag = False
                    string2 += "/"+item + "/ "
                if NULL_flag:
                    if FirstItemFlag == False:
                        string2 += "and word-finally."
                    else:
                        string2 += "word-finally."
                returnstring += string2 + " "*(colwidth2- len(string2))

                     
             
        return returnstring
# ----------------------------------------------------------------------------------------------------------------------------#

