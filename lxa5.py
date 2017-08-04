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
import string
import sys
import sys
import time



from collections import defaultdict
from initialization import *
from ClassLexicon import *
from dataviz import *
from dynamics import *
from lxa_module import *
from read_data import *
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
if config_lxa["affixtype"] == "prefix" or config_lxa["affixtype"] == "prefixes":
	FindSuffixesFlag = False
else:
	FindSuffixesFlag = True

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
    print "    Shifting a single letter from stem to affix."
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

  
# ------------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------------------#
#		User inquiries about morphology
# ------------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------------------#

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

 


# ---------------------------------------------------------------------------------#
#	Logging information
# ---------------------------------------------------------------------------------#

localtime = time.asctime(time.localtime(time.time()))
print
"Local current time :", localtime


# --------------------------------------------------#
