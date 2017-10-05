#   Richter
#
#   Author: Clayton Norris





#####  Takes a computer-generated morphological analysis from Linguistica and compares it to human-generated
#####  output from Alchemist, returning the Precision and Recall values of morphemes analyzed and of cuts created.
#####
#####
#####
#####  Useful methods:  run(alchfile,lxafile)        prints Precision and Recall by Cuts and Morphemes
#####                   runErrors(alchfile,lxafile)  same as run, also returns a dict of incorrect interpretations
#####                   *file directories default to "../EnglishGS12.xml" and "../english_words.txt"
#####

import re
import xml.etree.ElementTree as ET
import mmap
# import mmapPiequ                      PUT THIS BACK IN ! (I guess)






################################
################################
################################
####### Class Definitions
################################

class Word:
    
    def __init__(self,key,morpheme_list,id = 0):
        self.key = key
        self.length = len(key)
        self.morpheme_list = morpheme_list
        self.cuts_list = list()
        #self.getCuts()
        self.stem = morpheme_list[0]
        self.root = ""   ### Could possibly be used to differentiate between "mak" and "make" in "making"
        #print " 44 making new CWord" , key

    def getCuts(self):
        cuts_list = list()
        morphs = self.morpheme_list
        for x in range(0,(len(self.morpheme_list))):
            cuts_list.append(cuts_list[x] + len(morphs[x]))
        self.cuts = cuts_list[1:-1]
    

#    def addInterp(self,interp):
#        self.morpheme_list = list(set(self.morpheme_list).union(set(interp)))
#        self.getCuts()

    def display(self):
        result = key + "+" + morpheme_list.join("+")
	return result

################################
####### Alchemist
################################

def readAlchemist205File(filename):
    
    print " 68 reading alchemist 2 file" 
    tree = ET.parse(filename)
    root = tree.getroot()
    morphemeinfo = root[3]
    wordinfo = root[2]
    morphlist = []
    worddict = dict()
    testmorphs = dict()
    
    for morph in morphemeinfo:
        morphlist.append(morph.get("key"))

    for word in wordinfo:
        localmorphs = []
        key = word.get("key")
        for morph in word:
            if int(morph.get("morphemeindex")) != -1:
                print "\n86", word.get("key"), morph.get("key")
                m = morphlist[int(morph.get("morphemeindex"))]
                if (m != key):
                    localmorphs.append(m)
                    print "m:", m, key,
                else:
                    localmorphs.append("NULL")
            else:
                localmorphs.append("NULL")
            print 
            print "final", key, localmorphs
            print 
#        if key in worddict: #account for multiple interpretations of the word
#            worddict[key].addInterp(localmorphs)
#        else:
#            worddict[key] = Word(key,localmorphs)

	worddict[key] = Word(key, localmorphs)
	
	formatstring = "{}   {}"

    return worddict


###################################
#Input from Alchemist 3.0.0 xml
"""
    Xml is divided in partes tres: features, morphemes, words.
    
    Words contain both words and morphemes:
    
    <word score="Certain" id="5" >
    <string>abandoned</string>
    <piece length="15" id="0" start="0" />
    <affix allomorph-id="1" id="1" >
    <string>ed</string>
    <piece length="1" id="1" start="15" />
    </affix>
    </word>
"""
def readAlchemist300File(filename):
    
    print " 122  reading alchemist 3 file" 
    tree = ET.parse(filename)
    root = tree.getroot()
    morphemes = root[1]
    words = root[2]
    features = root[0]
    wordlist = dict()
    
    for word in words:
        wordtext = word[0].text
        wordmorphs = []
        if word.get("score") != "Not Scored":
            for child in word:
                if re.search ("(root)|(affix)", child.tag):
                    wordmorphs.append(child[0].text)
                elif re.search("piece",child.tag):
                    start = int(child.get("start"))
                    end = start + int(child.get("length"))
                    wordmorphs.append(wordtext[start:end])
            if len(wordmorphs) == 0:
                wordmorphs.append("NULL") #Keeping with the Lxa formatting, NULL means it has no morphemes
#            if wordtext in wordlist: #account for multiple interpretations of the word
#                    wordlist[wordtext].addInterp(wordmorphs)											 
#            else:
#                wordlist[wordtext] = Word(wordtext,wordmorphs)
            wordlist[wordtext] = Word(wordtext,wordmorphs)
    return wordlist
####################################
### read method that checks the version for you

def readAlchemistFile(filename):

    file = open(filename)
    tell = file.readline()

    isv205 = re.search("([DOC].+)+",tell) #The first line of a 2.0.5 output contains DOCTYPE goldstandard
    #can add new searches if new ouput variants are created.
    
    if isv205:
        print "Version 2.0.5"
        return readAlchemist205File(filename)
    else:
        print "Version 3.0.0"
        return readAlchemist300File(filename)


################################
####### Linguistica
################################

####################################
#Input from Linguistica xml:
"""
    Two parts:
    First half has
    word                  [morpheme class]
    Second half has:
    word                  morpheme class_morphemes
    
    where morphemes are separated by -
    
    first and second halves are divided by the last occurance of
    --------------------------------------------------------------
"""

def readLxaFile(filename):
    word_dict = dict()
    with open (filename) as word_file:
	for line in word_file:
	    if line[0]=="#":
		continue
 	    if ":" in line:
		cuts = list()
		chunks = line.split()
		word = chunks.pop(0)
		colon = chunks.pop(0)
		morpheme_list = list()
		current_pointer_loc = 0
		while chunks:
		    this_stem = chunks.pop(0)
		    stem_length = len(this_stem)
		    sig_we_do_not_care = chunks.pop(0)
		    cuts.append(stem_length- current_pointer_loc)
		    this_morpheme = this_stem[current_pointer_loc: ]
		    current_pointer_loc = stem_length
		    morpheme_list.append(this_morpheme)
		if stem_length < len(word):  # the last chunk
		    cuts.append(len(word))
		    this_morpheme = word[current_pointer_loc:]
		    morpheme_list.append(this_morpheme)
		word_dict[word] = Word(word, morpheme_list)
    return word_dict 
                                     
    word_file.close()

#    morphsect = sects[0].split("***" ) #[1] is empty, [2] is title, [3] is section 1, [4] is section 2
#    wordlist = dict()
#    print " lenth of morphsect " , len(morphsect), morphsect, morphsect[0]
#    for x in range(0, len(morphsect)/2):
     
#        word = morphsect[2*x]
#        print "richter line 143" , x, word
#        morphs = morphsect[2*x+1].split("_")[1].split("-")
#        if (morphs != ["NULL"]):
#            root = word[:-(len(reduce((lambda a: lambda b : a + b),morphs )))] 
#            wordlist[word] = Word(word, [root] + morphs)
#        else:
#            wordlist[word] = Word(word,morphs)
    #if morphsect[a] is a word, morphsect[a+1] is its morpheme data
    #word and morphs delimited by spaces, class and morphs delimited by _, morphs delimited by -
    
    return word_dict




###########################################
###########################################
####    Precision and Recall Functions
###########################################
"""
    Precision is intersection of relevant and recalled / recalled, i.e. how many of the recalled things were accurate
    Recall is  intersection of relevant and recalled/relevant, i.e. how many of the accurate things were recalled
    
    relevant = morpheme from Alchemist
    recalled = morpheme from Lxa
    
    Used here:
    numerator = sum(intersection of recalled and relevant) adds 1 for every morpheme in both sets
    pDenominator = sum(recalled) adds 1 for every morpheme from Lxa
    rDenominator = sum(relevant) adds 1 for every morpheme from Alchemist
"""

def checkPrecRecbyMorph(alchemist_dict,lxa_dict):
    # Lists are given as dictionaries word:[morphemes]

    print " Check pre rcall by morphs" 

    alchwords = alchemist_dict.keys()
    lxawords =lxa_dict.keys()
    overlap = list(set(lxawords).intersection(set(alchwords))) # list of words that are in both outputs
    
    
    errors = dict ()
    numerator = 0.0
    pDenominator = 0.0
    rDenominator = 0.0
    formatstring = "{:18} {:30} {:30} {:30}"
    for word in overlap:
	#print alchemist_dict[word].key
	#print lxa_dict[word].key, "275"
        alcmorphs = alchemist_dict[word].morpheme_list
        lxamorphs = lxa_dict[word].morpheme_list
        relrec = list(set(alcmorphs).intersection(set(lxamorphs)))
        numerator += len(relrec)
        pDenominator += len(lxamorphs)
        rDenominator += len(alcmorphs)
        if alcmorphs != lxamorphs:
            errors [word] =( alcmorphs, lxamorphs, relrec)
            print formatstring.format(word, alcmorphs, lxamorphs, relrec)
    print "Morpheme Precision : {0} , Recall : {1}".format(numerator/pDenominator,numerator/rDenominator)
    return errors


def checkPrecRecbyCut(alchlist,lxalist):
    
    alchwords = alchlist.keys()
    lxawords = lxalist.keys()
    overlap = list(set(lxawords).intersection(set(alchwords)))
    overlap.sort()
   
    print " size of lxa words" , len(lxawords)
    print " size of alchemist words" , len(alchwords)
    print " size of overlap" , len(overlap)

    errors = dict ()
    numerator = 0.0
    pDenominator = 0.0
    rDenominator = 0.0
    
    for word in overlap:
        alccuts = alchlist.get(word).cuts
        lxacuts= lxalist.get(word).cuts
        relrec = list(set(alccuts).intersection(set(lxacuts)))
        numerator += len(relrec)
        pDenominator += len(lxacuts)
        rDenominator += len(alccuts)
        if alccuts != lxacuts:
            errors [word] =( alccuts, lxacuts, relrec)
 
    print "Cut Precision : {0} , Recall : {1}".format(numerator/pDenominator,numerator/rDenominator)
    return errors

##################################
##################################
########   Usage Functions
##################################



def get_alchemist_dict(filename):
    return readAlchemist205File(filename)

def get_lxa_dict(filename):

    return readLxaFile(filename)
def runCuts():
    return checkPrecRecbyCut(get_alchemist_dict(),get_lxa_dict())


def runMorphs(alchemist_dict, lxa_dict):
    print " in runMorphs" 
    return checkPrecRecbyMorph(alchemist_dict,lxa_dict)



def runErrors(alch_file, lxa_file):
    
    print "244", alch_file, lxa_file
	
    print "Reading Alchemist files..."
    alchemist_dict = readAlchemistFile(alch_file)
    print len(alch)    

    print "Complete. Reading Linguistica files..."
    lxa_dict = readLxaFile(lxa_file)

    print "Complete. Calculating precision and recall values...\n"
    cErrors = checkPrecRecbyCut(alch,lxa)
    mErrors = checkPrecRecbyMorph(alch,lxa)
    
    cWords = cErrors.keys()
    mWords = mErrors.keys()
    
    mistakes = list(set(mWords).union(set(cWords)))
    mistakes.sort()
    output= dict()
    for x in mistakes:
        morph = "Correct"
        cut = "Correct"
        
        if x in cWords:
            cut = cErrors[x]
        if x in mWords:
            morph = mErrors[x]
        output[x] = (cut,morph)

    return output

def run():
    lxa_filename ="/home/ja-goldsmith/Dropbox/data/english/lxa/WordToSig_iter_1.txt"
#    alchemist_filename = "/home/ja-goldsmith/Dropbox/data/english/GoldStandard/EnglishGS12.xml"
    alchemist_filename = "/home/ja-goldsmith/Dropbox/lxa/alchemist/EnglishGS15-alchemist3-part1.xml"
    
    lxa_dict = get_lxa_dict(lxa_filename)
    alchemist_dict = get_alchemist_dict(alchemist_filename)
    
    runMorphs(alchemist_dict, lxa_dict)
    #runErrors(alch_file,lxa_file)

run()




