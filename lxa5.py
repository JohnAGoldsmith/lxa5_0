# -*- coding: <utf-16> -*-
#unicode = True
import argparse
import codecs
import copy
import datetime
import operator
import os
import os.path
#import pygraphviz as pgv
import string
import sys
import time
#from dataviz import *




from collections import defaultdict
from class_lexicon import *
from dynamics import *
from fsa import *
from lxa_module import *
from read_data import *
#from svg import *
from crab import *
from config import *
from initialization import *
from class_family import *
from crab3_dropjoints import *
# --------------------------------------------------------------------##
def create_and_change_path (newpath):
# --------------------------------------------------------------------##
    current_path = path = os.getcwd()
    print ("   The current working directory is %s" % path)
    new_folder = current_path + "/" + newpath + "/"
    if not os.path.isdir(new_folder):
        try:
            os.mkdir(new_folder)
        except OSError:
            print ("Creation of the directory %s failed." % new_folder)
        else:
            print ("Successfully created the directory %s ." % new_folder)
    try:
        os.chdir(new_folder)
        print("   Output folder was changed.")
    except OSError:
        print("   Can't change the output folder.")       
    return current_path
# --------------------------------------------------------------------##
# --------------------------------------------------------------------##
# --------------------------------------------------------------------##
def change_path (newpath):
# --------------------------------------------------------------------##
    try:
        os.chdir(newpath)
        print("   Folder changed.")
    except OSError:
        print("   Can't change folder.")       
# --------------------------------------------------------------------##


Initialization(argparse, config_lxa)
# ----------------------------------------------------------------------------#
# ----------------------------------------------------------------------------#
#                     Main part of program                              #
# ----------------------------------------------------------------------------#
# ----------------------------------------------------------------------------#


# This is just part of documentation:
# A signature is a tuple of strings (each an affix).
# Signatures is a map: its keys are signatures.  Its values are *sets* of stems.
# StemToWord is a map; its keys are stems.       Its values are *sets* of words.
# StemToSig  is a map; its keys are stems.  Its values are lists of signatures.
# The usual case when a stem has two signatures is when it is X+a for
# a signature in which X is a stem,
# and it is X + NULL in a differrent signature
# WordToSig  is a Map. its keys are words.Its values are *lists* of signatures.
# StemCorpusCounts is a map. Its keys are words.      Its values are corpus counts of stems.
# SignatureToStems is a dict: its keys ar.e tuples of strings,
# and its values are dicts of stems. We don't need both this and Signatures!
#print config_lxa["affix_type"], 51
Lexicon = CLexicon()
Lexicon.infolder = config_lxa["complete_infilename"]
Lexicon.outfolder = config_lxa["outfolder"]
Lexicon.graphicsfolder = config_lxa["graphicsfolder"]
if config_lxa["affix_type"] == "prefix":
    Lexicon.FindSuffixesFlag = False
else:
    Lexicon.FindSuffixesFlag = True
# ---------------------.-----------------------------------------------##
#        read wordlist (dx1)
# --------------------------------------------------------------------##


infile = open(config_lxa["complete_infilename"])
read_data(config_lxa["datatype"],
          infile,
          Lexicon,
          config_lxa["BreakAtHyphensFlag"],
          config_lxa["word_count_limit"])
print "\n1. Finished reading word list. Word count:", len(Lexicon.Word_counts_dict), "\n"

# --------------------------------------------------------------------##
#        Initialize some output files
# --------------------------------------------------------------------##
 
if not os.path.isdir(config_lxa["outfolder"]):
    try:
        os.mkdir(config_lxa["outfolder"])
    except OSError:
        print ("Creation of the directory %s failed." % path)
    else:
        print ("Successfully created the directory %s ." % path)


# --------------------------------------------------------------------##
#        For finite state automaton
# --------------------------------------------------------------------##

if False:
    splitEndState = True
    morphology = FSA_lxa(splitEndState)

# ---------------------------------------------------------------------------##
# -- We can control which functions we are working on at the moment. -------#
#
#       This is the developer's way of deciding which functions s/he wishes to explore....


if True:
    
    newpath = "1_crab2"
    oldpath = create_and_change_path (newpath)
 
    print "2. Crab 1: Make signatures.", config_lxa["affix_type"]
    MakeSignatures_Crab_1(Lexicon, config_lxa["affix_type"], Lexicon.MinimumStemLength)

    print "3. Printing signatures."
    Lexicon.printSignatures(config_lxa)
    find_families(Lexicon, config_lxa["affix_type"])

    change_path(oldpath)

# --------------------------------------------------------------------##

if True:
    newpath ="2_widen_signatures"
    oldpath = create_and_change_path (newpath)

    print "3. Crab 2: Widen scope of affixes."
 
    MakeSignatures_Crab_2(Lexicon, config_lxa["affix_type"], verboseflag)
    Lexicon.printSignatures(config_lxa)

    change_path(oldpath)

# --------------------------------------------------------------------##
 
# --------------------------------------------------------------------##

# --------------------------------------------------------------------##
if True:
   dropJoints(Lexicon, config_lxa["affix_type"])
   for line in Lexicon.produce_lexicon_report():
       print line
# --------------------------------------------------------------------##


if True:
    newpath = "3_cut_up_affixes"
    oldpath = create_and_change_path (newpath)

    print "4. Crab 3: Interactions of multiple signatures on single words."
 
    MakeSignatures_Crab_3(Lexicon, config_lxa["affix_type"], verboseflag)
    Lexicon.printSignatures(config_lxa)

    change_path(oldpath)
 
    for line in Lexicon.produce_lexicon_report():
       print line
# --------------------------------------------------------------------##

if False:
    newpath = "4_close_stem_pairs"
    oldpath = create_and_change_path (newpath)

    print "5. Crab 4: Close stem pairs = complex signatures."
 
    MakeSignatures_Crab_5(Lexicon, config_lxa["affix_type"], verboseflag)
    Lexicon.printSignatures(config_lxa)

    change_path(oldpath)


# 4 --------------------------------------------------------------------


if config_lxa["dynamics"] and config_lxa["datatype"]  == "CORPUS":
    dynamics_file = open(config_lxa["outfolder"] + "dynamics.txt", "w")
    Dynamics(Lexicon, dynamics_file)

 

 
if False:
    print     "5. Printing signature transforms for each word."
    printWordsToSigTransforms(Lexicon.SignatureToStems,
                              Lexicon.WordToSig,
                              Lexicon.StemCorpusCounts,
                              g_encoding,
                              FindSuffixesFlag)
 
if config_lxa["FSA"]:
    print
    "7. Adding signatures to the FSA."
    AddSignaturesToFSA(Lexicon, Lexicon.SignatureStringsToStems, morphology, FindSuffixesFlag)

if config_lxa["FSA"]:
    print outfolder + "fsa.txt"
    "8. Printing the FSA."
    fsa_file = open(outfolder +  "fsa.txt", "w")
    print >> fsa_file, language, complete_infilename, config_lxa["word_count_limit"]
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

if config_lxa["FSA"] and config_lxa["PrintFSAgraphs"]:
    print     "  11. Printing graphs of the FSA."
    for state in morphology.States:
        # do not print the entire graph:
        # if state == morphology.startState:
        #    continue
        ###
        graph = morphology.createPySubgraph(state)
        # if the graph has 3 edges or fewer, do not print it:

        if len(graph.edges()) < 2:
            continue

        graph.layout(prog='dot')
        filename = graphicsfolder + 'morphology' + str(state.index) + '.png'
        graph.draw(filename)
        if False:
            filename = graphicsfolder + 'morphology' + str(state.index) + '.dot'
            graph.write(filename)

# ---------------------------------------------------------------------------------#
#    5d. Print FSA again, with these changes.
# ---------------------------------------------------------------------------------#


fsa_word_parses = open(config_lxa["outfolder"] + "fsa_word_parses.txt", "w")
if config_lxa["FSA"]:
    print    "12. Parsing all words through FSA."
    morphology.parse_words(Lexicon.WordToSig.keys(), fsa_word_parses)

if config_lxa["FSA"]:
    print     "13. Printing all the words' parses."
    morphology.printAllParses(fsa_word_parses)


# ------------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------------------#
#        User inquiries about morphology
# ------------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------------------#

if False:
    morphology_copy = morphology.MakeCopy()

    initialParseChain = ParseChain()
    CompletedParses = list()
    IncompleteParses = list()
    word = ""
while True:
    word = raw_input('Inquire about a word: ')

    if False and word in Lexicon.WordBiographies:
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


if False:    

    del CompletedParses[:]
    del IncompleteParses[:]
    del initialParseChain.my_chain[:]
    startingParseChunk = parseChunk("", word)
    startingParseChunk.toState = morphology.startState

    initialParseChain.my_chain.append(startingParseChunk)
    IncompleteParses.append(initialParseChain)
    while len(IncompleteParses) > 0:
        CompletedParses, IncompleteParses = morphology.lparse(CompletedParses, IncompleteParses)
    if len(CompletedParses) == 0: print "no analysis found."

    for parseChain in CompletedParses:
        for thisParseChunk in parseChain.my_chain:
            if thisParseChunk.edge:
                print
                "\t", thisParseChunk.morph,
        print
    print

    for parseChain in CompletedParses:
        print
        "\tStates: ",
        for thisParseChunk in parseChain.my_chain:
            if thisParseChunk.edge:
                print "\t", thisParseChunk.fromState.index,
                print "\t", thisParseChunk.toState.index
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
#    Logging information
# ---------------------------------------------------------------------------------#

localtime = time.asctime(time.localtime(time.time()))
print
"Local current time :", localtime


# --------------------------------------------------#
