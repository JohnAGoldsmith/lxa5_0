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
from initialization import *
from ClassLexicon import *
from dataviz import *
from dynamics import *
from fsa import *
from loose_fit import *
from lxa_module import *
from read_data import *
#from svg import *
from crab import *
from config import *

FSA_flag = False




# -------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------#
# 					Initialization			   	#
# -------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------#


Initialization(argparse, config_lxa,FSA_flag)


# -------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------#
# 					Main part of program		   			   	#
# -------------------------------------------------------------------------------------------------------#
# -------------------------------------------------------------------------------------------------------#


# This is just part of documentation:
# A signature is a tuple of strings (each an affix).
# Signatures is a map: its keys are signatures.  Its values are *sets* of stems.
# StemToWord is a map; its keys are stems.       Its values are *sets* of words.
# StemToSig  is a map; its keys are stems.       Its values are lists of signatures. The usual case when a stem has two signatures is when it is X+a for a signature in which X is a stem,
# and it is X + NULL in a differrent signature
# WordToSig  is a Map. its keys are words.       Its values are *lists* of signatures.
# StemCorpusCounts is a map. Its keys are words. 	 Its values are corpus counts of stems.
# SignatureToStems is a dict: its keys are tuples of strings, and its values are dicts of stems. We don't need both this and Signatures!

Lexicon = CLexicon()
Lexicon.infolder = config_lxa["complete_infilename"]
Lexicon.outfolder = config_lxa["outfolder"]
Lexicon.graphicsfolder = config_lxa["graphicsfolder"]
FindSuffixesFlag = config_lxa["FindSuffixesFlag"]


# --------------------------------------------------------------------##
#		read wordlist (dx1)
# --------------------------------------------------------------------##

g_encoding = "asci"  # "utf8"
BreakAtHyphensFlag = True

if g_encoding == "utf8":
    infile = codecs.open(infilename, g_encoding='utf-8')
else:
    infile = open(config_lxa["complete_infilename"])

filelines = infile.readlines()
read_data(config_lxa["datatype"],filelines,Lexicon,BreakAtHyphensFlag,config_lxa["word_count_limit"])
Lexicon.WordList.sort()
print "\n1. Finished reading word list.\n"

# --------------------------------------------------------------------##
#		Initialize some output files
# --------------------------------------------------------------------##

Lexicon.PrintWordCounts()
Lexicon.Words = Lexicon.WordCounts.keys()
Lexicon.Words.sort()
initialize_files(Lexicon, "console", 0,0, config_lxa["language"])

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
    "2. Make Signatures.", FindSuffixesFlag
    MakeSignatures_Crab(Lexicon, FindSuffixesFlag, Lexicon.MinimumStemLength)

if True:
    print "     Printing signatures."
    suffix = "1"
    Lexicon.printSignatures(g_encoding, FindSuffixesFlag,suffix)


if config_lxa["dynamics"] and datatype == "CORPUS":
    dynamics_file = open(outfolder +  "dynamics.txt", "w")
    Dynamics(Lexicon,dynamics_file)

if True:
    print "  3. Find good signatures inside bad."
    FindGoodSignaturesInsideBad_crab(Lexicon,  FindSuffixesFlag,verboseflag)

   #Pull single letter from edge of stems
    print "   Shifting a single letter from stem to affix."
    while True:
		number_of_changes = pull_single_letter_from_edge_of_stems_crab(Lexicon,FindSuffixesFlag)
		print "  6a. Shift a letter from stem to affix. Number of changes: ", number_of_changes, ".",
		if number_of_changes == 0:
			print " Recompute signatures with these changes."
			break
                print " Go through the signatures again."
		AssignAffixesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag)
		MinimumStemCountInSignature = 1
		AssignSignaturesToEachStem_crab(Lexicon, FindSuffixesFlag,verboseflag, MinimumStemCountInSignature, Step=-1)
		


if (False):
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
        Lexicon.AssignSignaturesToEachStem_crab(FindSuffixesFlag,Step)

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





if False:
    print
    "3. Finding sets of extending signatures."
    extending_signatures(Lexicon, FileObject["SigExtensions"])

if False:
    print "Finding pairs of signatures that share words."
    FindSignatureChains(Lexicon)

if config_lxa["radviz"]:
    print     "3.1 Creating data structure for radviz."
    (SignatureStemList, SigDataDict) = signature_by_stem_data(Lexicon)
    for sig in SignatureStemList:
        print
        "\n", sig, "\n", SignatureStemList[sig], "\n", SigDataDict[sig]

if True:
    print
    "\n4. Printing signatures."
    suffix = "2"
    #Lexicon.printSignatures(FileObject, g_encoding, FindSuffixesFlag,suffix)
    Lexicon.printSignatures(g_encoding, FindSuffixesFlag,suffix)



if False:
    print
    "5. Printing signature transforms for each word."
    #printWordsToSigTransforms(Lexicon.SignatureToStems, Lexicon.WordToSig, Lexicon.StemCorpusCounts,
    #                          FileObject["SigTransforms"], g_encoding, FindSuffixesFlag)
    printWordsToSigTransforms(Lexicon.SignatureToStems, Lexicon.WordToSig, Lexicon.StemCorpusCounts,
                              g_encoding, FindSuffixesFlag)

if False:
    print
    "6. Slicing signatures."
    SliceSignatures(Lexicon, g_encoding, FindSuffixesFlag, FileObject["Log"])



if FSA_flag:
    print
    "7. Adding signatures to the FSA."
    AddSignaturesToFSA(Lexicon, Lexicon.SignatureStringsToStems, morphology, FindSuffixesFlag)

if FSA_flag:
    print outfolder + "fsa.txt"
    "8. Printing the FSA."
    fsa_file = open(outfolder +  "fsa.txt", "w")
    print >> fsa_file,   language, complete_infilename, config_lxa["word_count_limit"]
    morphology.printFSA(fsa_file)
    filename = outfolder + "fsa_a.html"
    #morphology.print_FSA_to_HTML(filename)
    print "  All signatures placed in FSA."
if False:
    print
    "9. Printing signatures."
    printSignatures(Lexicon, FileObject["Signatures"], FileObject["WordToSig"], FileObject[StemToWords],
                    FileObject[Suffixes], g_encoding, FindSuffixesFlag, letterCostOfStems, letterCostOfSignatures)

if False:
    print "  10. Finding robust peripheral pieces on edges in FSA."
    for loopno in range(NumberOfCorrections):
        morphology.find_highest_weight_affix_in_an_edge(FileObject["Log"], FindSuffixesFlag)

if FSA_flag and config_lxa["PrintFSAgraphs"]:
    print     "  11. Printing graphs of the FSA."
    for state in morphology.States:
        # do not print the entire graph:
        # if state == morphology.startState:
        #	continue
        ###
        graph = morphology.createPySubgraph(state)
        # if the graph has 3 edges or fewer, do not print it:

        if len(graph.edges()) < 2:
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


fsa_word_parses = open(config_lxa["outfolder"] + "fsa_word_parses.txt", "w")
if FSA_flag:
    print    "12. Parsing all words through FSA."
    morphology.parse_words(Lexicon.WordToSig.keys(), fsa_word_parses)

if FSA_flag:
    print     "13. Printing all the words' parses."
    morphology.printAllParses(fsa_word_parses)


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

    #parses = morphology.parse_word(word)



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

    else:
	    del CompletedParses[:]
	    del IncompleteParses[:]
	    del initialParseChain.my_chain[:]
	    startingParseChunk = parseChunk("", word)
	    startingParseChunk.toState = morphology.startState

	    initialParseChain.my_chain.append(startingParseChunk)
	    IncompleteParses.append(initialParseChain)
	    while len(IncompleteParses) > 0:
		CompletedParses, IncompleteParses = morphology.lparse(CompletedParses, IncompleteParses)
	    if len(CompletedParses) == 0: print "no analysis found.", "367"

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



# ---------------------------------------------------------------------------------#
#	Logging information
# ---------------------------------------------------------------------------------#

localtime = time.asctime(time.localtime(time.time()))
print
"Local current time :", localtime


# --------------------------------------------------#
