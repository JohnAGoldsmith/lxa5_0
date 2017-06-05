# -*- coding: <utf-16> -*-
unicode = True
import argparse
import codecs
import codecs  # for utf8
import copy
import datetime
import operator
import os
import os.path
import pygraphviz as pgv
import string
import sys
import sys
import time
from collections import defaultdict

from ClassLexicon import *
from dataviz import *
from dynamics import *
from fsa import *
from loose_fit import *
from lxa_module import *
from read_data import *
from svg import * 
from crab import *




# --------------------------------------------------------------------##
#		user modified variables
# --------------------------------------------------------------------##

verboseflag = True
FindSuffixesFlag = True

# --------------------------------------------------------------------##
#		parse command line arguments
# --------------------------------------------------------------------##
datatype = None

parser = argparse.ArgumentParser(description='Compute morphological analysis.')
parser.add_argument('-l', action="store", dest="language", help="name of language", default="english")
parser.add_argument('-w', action="store", dest="wordcountlimit", help="number of words to read", default=10000)
parser.add_argument('-f', action="store", dest="filename", help="name of file to read", default="browncorpus")
parser.add_argument('-c', action="store", dest="corrections", help="number of corrections to make", default=0)
parser.add_argument('-d', action="store", dest="data_folder", help="data directory", default="../../data/")

results                 = parser.parse_args()
language                = results.language
wordcountlimit          = int(results.wordcountlimit)
shortfilename           = results.filename
NumberOfCorrections     = results.corrections

# --------------------------------------------------------------------##
#	Determine folders for input, output; initialize output files
# --------------------------------------------------------------------##


datafolder      = results.data_folder + language + "/"
outfolder       = datafolder + "lxa/"
infolder        = datafolder + 'dx1/'
if shortfilename[-4:] == ".txt":
    datatype = "CORPUS"
    infilename = datafolder + shortfilename
else:
    datatype == "DX1"
    infilename  = infolder + shortfilename + ".dx1"
graphicsfolder  = outfolder + "graphics/"
if not os.path.exists(graphicsfolder):
    os.makedirs(graphicsfolder)




g_encoding = "asci"  # "utf8"
BreakAtHyphensFlag = True

FileObject = dict()
fileslist = ("Signatures", "FSA", "SigExemplars", "WordToSig", "SigTransforms",
             "StemToWords", "StemToWords2", "WordParses", "WordCounts", "SigExtensions",
             "Suffixes", "Rebalancing_Signatures", "Subsignatures",
             "UnlikelySignatures", "Log","Words", "Dynamics", "UnexplainedContinuations")
for item in fileslist:
    # print item
    FileObject[item] = open(outfolder + item + ".txt", "w")
FileObject["html"] = open(outfolder + "signatures.html", "w")

# --------------------------------------------------------------------##
#		Tell the user what we will be doing.
# --------------------------------------------------------------------##


formatstring_initial_1 = "{:40s}{:>15s}"
print "\n\n" + "-" * 100
print("Language:", language)
if FindSuffixesFlag:
    print     "Finding suffixes."
else:
    print     "Finding prefixes."
if datatype == "DX1":
    print     formatstring_initial_1.format("Reading dx file: ", infilename)
else:
    print     formatstring_initial_1.format("Reading corpus: ", infilename)
print
formatstring_initial_1.format("Logging to: ", outfolder)
print "-" * 100

 

# -------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------#
# 					Main part of program		   			   	#
# -------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------#


# This is just part of documentation:
# A signature is a tuple of strings (each an affix).
# Signatures is a map: its keys are signatures.  Its values are *sets* of stems.
# StemToWord is a map; its keys are stems.       Its values are *sets* of words.
# StemToSig  is a map; its keys are stems.       Its values are individual signatures.
# WordToSig  is a Map. its keys are words.       Its values are *lists* of signatures.
# StemCorpusCounts is a map. Its keys are words. 	 Its values are corpus counts of stems.
# SignatureToStems is a dict: its keys are tuples of strings, and its values are dicts of stems. We don't need both this and Signatures!

Lexicon = CLexicon()

# --------------------------------------------------------------------##
#		read wordlist (dx1)
# --------------------------------------------------------------------##

if g_encoding == "utf8":
    infile = codecs.open(infilename, g_encoding='utf-8')
else:
    infile = open(infilename)

filelines = infile.readlines()

read_data(datatype,filelines,Lexicon,BreakAtHyphensFlag,wordcountlimit)

Lexicon.ReverseWordList = Lexicon.WordCounts.keys()
Lexicon.ReverseWordList.sort(key=lambda word: word[::-1])
Lexicon.WordList.sort()
print "\n1. Finished reading word list.\n"


# --------------------------------------------------------------------##
#		Initialize some output files
# --------------------------------------------------------------------##

Lexicon.PrintWordCounts(FileObject["WordCounts"])
Lexicon.Words = Lexicon.WordCounts.keys()
Lexicon.Words.sort()
print >> FileObject["Signatures"], "# ", language, wordcountlimit
initialize_files(Lexicon, FileObject["Log"], 0,0, language)
initialize_files(Lexicon, "console", 0,0, language)

# --------------------------------------------------------------------##
#		For finite state automaton
# --------------------------------------------------------------------##

splitEndState = True
morphology = FSA_lxa(splitEndState)



# ---------------------------------------------------------------------------------------------------------------##
# ----------------- We can control which functions we are working on at the moment. ------------------------------#
#
#       This is the developer's way of deciding which functions s/he wishes to explore....




if True:
    print
    "2. Make Signatures."
    MakeSignatures_Crab(Lexicon, FileObject["Log"], FileObject["Rebalancing_Signatures"], FileObject["UnlikelySignatures"],
                           FileObject["Subsignatures"], FindSuffixesFlag, Lexicon.MinimumStemLength)

if True and datatype == "CORPUS":
    Dynamics(Lexicon,FileObject["Dynamics"])

if False:
    print
    "3. Find good signatures inside bad."
    Lexicon.FindGoodSignaturesInsideBad(FileObject["Subsignatures"], True)

if False:
    print
    "3. Finding sets of extending signatures."
    extending_signatures(Lexicon, FileObject["SigExtensions"])

if True:
    print "Finding pairs of signatures that share words."
    FindSignatureChains(Lexicon)

if False:
    print
    "3.1 Creating data structure for radviz."
    (SignatureStemList, SigDataDict) = signature_by_stem_data(Lexicon)
    for sig in SignatureStemList:
        print
        "\n", sig, "\n", SignatureStemList[sig], "\n", SigDataDict[sig]

if True:
    print
    "\n4. Printing signatures."
    Lexicon.printSignatures(FileObject["Log"], FileObject["Signatures"], FileObject["UnlikelySignatures"], FileObject["html"],
                            FileObject["WordToSig"], FileObject["StemToWords"], FileObject["StemToWords2"],
                            FileObject["SigExtensions"], FileObject["Suffixes"], FileObject["UnexplainedContinuations"], FileObject["Words"], g_encoding, FindSuffixesFlag)

if False:
    print
    "5. Printing signature transforms for each word."
    printWordsToSigTransforms(Lexicon.SignatureToStems, Lexicon.WordToSig, Lexicon.StemCorpusCounts,
                              FileObject["SigTransforms"], g_encoding, FindSuffixesFlag)




if False:
    print
    "6. Slicing signatures."
    SliceSignatures(Lexicon, g_encoding, FindSuffixesFlag, FileObject["Log"])

#if True:
#   print "7. Summarizing what has not been accounted for following the recognized stems."
#   Lexicon.SummarizePostStemMaterial(FindSuffixFlag, FileObject["Remains"])

if True:
    print
    "7. Adding signatures to the FSA."
    AddSignaturesToFSA(Lexicon, Lexicon.SignatureStringsToStems, morphology, FindSuffixesFlag)

if True:
    print
    "8. Printing the FSA."
    print >> FileObject["FSA"], "#", language, shortfilename, wordcountlimit
    morphology.printFSA(FileObject["FSA"])

if False:
    print
    "9. Printing signatures."
    printSignatures(Lexicon, FileObject["Signatures"], FileObject["WordToSig"], FileObject[StemToWords],
                    FileObject[Suffixes], g_encoding, FindSuffixesFlag, letterCostOfStems, letterCostOfSignatures)

if False:
    print
    "10. Finding robust peripheral pieces on edges in FSA."
    for loopno in range(NumberOfCorrections):
        morphology.find_highest_weight_affix_in_an_edge(FileObject["Log"], FindSuffixesFlag)

if True:
    print
    "11. Printing graphs of the FSA."
    for state in morphology.States:
        # do not print the entire graph:
        # if state == morphology.startState:
        #	continue
        ###
        graph = morphology.createPySubgraph(state)
        # if the graph has 3 edges or fewer, do not print it:

        if len(graph.edges()) < 4:
            continue

        graph.layout(prog='dot')
        filename = graphicsfolder + 'morphology' + str(state.index) + '.png'
        graph.draw(filename)
        if (False):
            filename = graphicsfolder + 'morphology' + str(state.index) + '.dot'
            graph.write(filename)

# ---------------------------------------------------------------------------------#
#	5d. Print FSA again, with these changes.
# ---------------------------------------------------------------------------------#

if False:
    print
    "11. Printing the FSA."
    morphology.printFSA(FileObject[FSA])

if False:
    print
    "12. Parsing all words through FSA."
    morphology.parseWords(Lexicon.WordToSig.keys(), FileObject[WordParses])

if False:
    print
    "13. Printing all the words' parses."
    morphology.printAllParses(FileObject[WordParses])

if False:
    print
    "14. Now look for common morphemes across different edges."
    morphology.findCommonMorphemes(lxalogfile)

if False:    
    # we will remove this. It will be replaced by a function that looks at all cross-edge sharing of morphemes.
    morphology.EdgeMergers(FileObject[FSA], HowManyTimesToCollapseEdges)
     

# ------------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------------------#
#		User inquiries about morphology
# ------------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------------------#

morphology_copy = morphology.MakeCopy()

initialParseChain = ParseChain()
CompletedParses = list()
IncompleteParses = list()
word = ""
while True:
    word = raw_input('Inquire about a word: ')

    if word in Lexicon.WordBiographies:
        for line in Lexicon.WordBiographies[word]:
            print line
        print "------------------------"
        print "1. Finding protostems.  "    
        print "2. Find first parsing into proto-stems plus affixes."
        print "3. Roll out the list of parse pairs."
        print "4. Assign affixes to each protostem, stem-to-word (1)."
        print "5. Delete signatures with too few stems. (2)."
        print "6. Assign a unique signature to each stem. (3)."


    if word in Lexicon.SignatureBiographies:
        for line in Lexicon.SignatureBiographies[word]:
            print "sigs: ", line


    if word == "exit":
        break
        
# ------------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------------------#

        
        
    if word == "State":
        while True:
            stateno = raw_input("State number:")
            if stateno == "" or stateno == "exit":
                break
            stateno = int(stateno)
            for state in morphology.States:
                if state.index == stateno:
                    break
            state = morphology.States[stateno]
            for edge in state.getOutgoingEdges():
                print
                "Edge number", edge.index
                i = 0
                for morph in edge.labels:
                    print
                    "%12s" % morph,
                    i += 1
                    if i % 6 == 0: print
            print
            "\n\n"
            continue
    if word == "Edge":
        while True:
            edgeno = raw_input("Edge number:")
            if edgeno == "" or edgeno == "exit":
                break
            edgeno = int(edgeno)
            for edge in morphology.Edges:
                if edge.index == edgeno:
                    break
            print
            "From state", morphology.Edges[edgeno].fromState.index, "To state", morphology.Edges[edgeno].toState.index
            for edge in morphology.Edges:
                if edge.index == int(edgeno):
                    morphlist = list(edge.labels)
            for i in range(len(morphlist)):
                print
                "%12s" % morphlist[i],
                if i % 6 == 0:
                    print
            print
            "\n\n"
            continue
    if word == "graph":
        while True:
            stateno = raw_input("Graph state number:")

#   ---------------  New section: Parsing in the FSA ------------------------ #


    del CompletedParses[:]
    del IncompleteParses[:]
    del initialParseChain.my_chain[:]
    startingParseChunk = parseChunk("", word)
    startingParseChunk.toState = morphology.startState

    initialParseChain.my_chain. append(startingParseChunk)
    IncompleteParses.append(initialParseChain)
    while len(IncompleteParses) > 0:
        CompletedParses, IncompleteParses = morphology.lparse(CompletedParses, IncompleteParses)
    if len(CompletedParses) == 0: print
    "no analysffound."

    for parseChain in CompletedParses:
        for thisParseChunk in parseChain.my_chain:
            if (thisParseChunk.edge):
                print
                "\t", thisParseChunk.morph,
        print
    print

    for parseChain in CompletedParses:
        print
        "\tStates: ",
        for thisParseChunk in parseChain.my_chain:
            if (thisParseChunk.edge):
                print
                "\t", thisParseChunk.fromState.index,
        print
        "\t", thisParseChunk.toState.index
    print

    for parseChain in CompletedParses:
        print
        "\tEdges: ",
        for thisParseChunk in parseChain.my_chain:
            if (thisParseChunk.edge):
                print
                "\t", thisParseChunk.edge.index,
        print
    print
    "\n\n"

# ---------------------------------------------------------------------------------------------------------------------------#
# ---------------------------------------------------------------------------------#
#	Close output files
# ---------------------------------------------------------------------------------#
for item in fileslist:
    FileObject[item].close()

# ---------------------------------------------------------------------------------#
#	Logging information
# ---------------------------------------------------------------------------------#

localtime = time.asctime(time.localtime(time.time()))
print
"Local current time :", localtime

FileObject["Log"].close()
# --------------------------------------------------#
