# -*- coding: <utf-16> -*- 
unicode = True
import sys
import codecs
import pygraphviz as pgv
import argparse
from ClassLexicon import *
import os.path
from loose_fit import *


# Important note to user:
# My folder structure is this:
# /linguistica/lxa5_0/lxa5_0.py
#             /lxa5_1/lxa5_1.py
# /data/english/dx1/browncorpus.dx1
#              /lxa/Signatures.txt etc.
#              /graphics
# You can change this to fit your directory structure on line 75 below.

 
# This program looks for extended signatures, which are regular subgraphs among words, where the edges are
# (high-freq) Delta-Right pairs of words, and where a word may be *split differently* (without penalty!) 
# in different Delta-Right pairs: e.g., "moves" is part of the pair (move/move-s) and also of the pair
# (mov-es/mov-ing).
# 	Prototyping for bootstrapping of Lxa5
# 	Accepts name of input file as command-line argument.
#--------------------------------------------------------------------##
#		Main program begins on line 174
#--------------------------------------------------------------------##

import time
import datetime
import operator
import sys
import os
import codecs # for utf8
import string
import copy
from collections import defaultdict
from lxa_module import *
from signatures import *
from fsa import *

#--------------------------------------------------------------------##
#		user modified variables
#--------------------------------------------------------------------##

language = ""
wordcount = 0
shortfilename = ""
NumberOfCorrections = 0
FindSuffixesFlag=True	

parser = argparse.ArgumentParser(description='Compute morphological analysis.')
parser.add_argument('-l', action="store", dest= "language", help = "name of language")
parser.add_argument('-w', action="store", dest= "wordcount", help = "number of words to read", default = 5000)
parser.add_argument('-f', action="store", dest= "filename", help = "name of file to read", default="defaultfilename")
parser.add_argument('-c', action="store", dest= "corrections", help = "number of corrections to make",default=0)

results = parser.parse_args()
language = results.language
numberofwords	 = results.wordcount
shortfilename = results.filename
NumberOfCorrections = results.corrections 


 
g_encoding =  "asci"  # "utf8"
BreakAtHyphensFlag = True 

#----------------- Defining directories we are using ------------------------------#


datafolder 				= "../../data/" + language + "/"
outfolder     			        = datafolder    + "lxa/"
infolder 				= datafolder    + 'dx1/'	

graphicsfolder= outfolder + "graphics/"
if not os.path.exists(graphicsfolder):
	os.makedirs(graphicsfolder)

infilename 				= infolder  + shortfilename + ".dx1"
stemfilename 				= infolder  + shortfilename + "_stems.txt"

FileObject = dict()
fileslist = ("Signatures", "FSA", "SigExemplars", "WordToSig", "SigTransforms",
	"StemToWords", "StemToWords2", "WordParses", "WordCounts", "SigExtensions", 
	"Suffixes", "Rebalancing_Signatures",
	"unlikelysignatures", "Log")
for item in fileslist:
	print item
	FileObject[item] = open (outfolder + item + ".txt", "w")
 
#----------------- Tell the user what we are doing now ------------------------------#


formatstring_initial_1 = "{:40s}{:>15s}"
print "\n\n" + "-"*100 
print ("language" , language)
if FindSuffixesFlag:
	print "Finding suffixes." 
else:
	print "Finding prefixes." 
print  formatstring_initial_1.format("Reading dx file: ", infilename)
print  formatstring_initial_1.format("Logging to: ", outfolder )
print "-"* 100 
 
print "language", language
 
if g_encoding == "utf8":
	infile = codecs.open(infilename, g_encoding = 'utf-8')
else:
	infile = open(infilename) 
 



#-------------------------------------------------------------------------------------------------------# 
#-------------------------------------------------------------------------------------------------------#
# 					Main part of program		   			   	#
#-------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------------------------#


	# This is just part of documentation:
	# A signature is a tuple of strings (each an affix).
	# Signatures is a map: its keys are signatures.  Its values are *sets* of stems. 
	# StemToWord is a map; its keys are stems.       Its values are *sets* of words.
	# StemToSig  is a map; its keys are stems.       Its values are individual signatures.
	# WordToSig  is a Map. its keys are words.       Its values are *lists* of signatures.
	# StemCorpusCounts is a map. Its keys are words. 	 Its values are corpus counts of stems.
	# SignatureToStems is a dict: its keys are tuples of strings, and its values are dicts of stems. We don't need both this and Signatures!

 

Lexicon = CLexicon( )
 
#--------------------------------------------------------------------##
#		read wordlist (dx1)
#--------------------------------------------------------------------##

filelines= infile.readlines()
 
 
#this is for a dx1 file:
for line in filelines:
	pieces = line.split()	
	word=pieces[0] 	
	if word == '#' :
		continue
	if word.isalpha() == False:
		continue
	if len(pieces) > 1:
		count = int(pieces[1])
	else:
		count =1 
	word = word.lower()
	if (BreakAtHyphensFlag and '-' in word):
		words = word.split('-')
		for word in words:
			if word.isalpha() == False:
				continue
			if word not in WordCounts:
				WordCounts[word]=0
			Lexicon.WordCounts[word]+=count
			if len(Lexicon.WordCounts) >= results.wordcount:
				break
			Lexicon.TotalLetterCountInWords  += len(word)
	else:	
		if word not in Lexicon.WordCounts:
			Lexicon.WordCounts[word]=0 
		Lexicon.WordCounts[word]  = count
		Lexicon.TotalLetterCountInWords += len(word)
		if len(Lexicon.WordCounts) >= results.wordcount:
			break
 
	Lexicon.WordList.AddWord(word) 
Lexicon.ReverseWordList =  Lexicon.WordCounts.keys()
Lexicon.ReverseWordList.sort(key = lambda word:word[::-1])
Lexicon.WordList.sort()
print "\n1. Finished reading word list.\n"
Lexicon.PrintWordCounts(FileObject["WordCounts"])
Lexicon.Words = Lexicon.WordCounts.keys()
Lexicon.Words.sort()
 

print >>FileObject["Signatures"], "# ", language, results.wordcount

initialize_files1(Lexicon, FileObject["Log"], language)
initialize_files1(Lexicon, "console", language)

 
splitEndState = True
morphology= FSA_lxa(splitEndState)

#----------------- We can control which functions we are working on at the moment. ------------------------------#

if True: 	
	print "2. Make Signatures."
	Lexicon.MakeSignatures(FileObject["Log"],FileObject["Rebalancing_Signatures"],FindSuffixesFlag,Lexicon.MinimumStemLength)
	
if False: 
	print "3. Find good signatures inside bad."	
	Lexicon.FindGoodSignaturesInsideBad()

if False: 
	print "3. Loose fit."
	loose_fit(Lexicon )
 
if True:
	print "\n4. Printing signatures."
	Lexicon.printSignatures(FileObject["Log"], FileObject["Signatures"],FileObject["unlikelysignatures"], FileObject["WordToSig"], FileObject["StemToWords"], FileObject["StemToWords2"], FileObject["SigExtensions"],FileObject["Suffixes"] ,g_encoding, FindSuffixesFlag)
 
if False:
	print "5. Printing signature transforms for each word."
	printWordsToSigTransforms(Lexicon.SignatureToStems, Lexicon.WordToSig, Lexicon.StemCorpusCounts, FileObject["SigTransforms"], g_encoding, FindSuffixesFlag)
 
if False:
	print "6. Slicing signatures."
	SliceSignatures(Lexicon,  g_encoding, FindSuffixesFlag, FileObject["Log"]	)

if False:
	print "7. Adding signatures to the FSA."
	AddSignaturesToFSA(Lexicon, Lexicon.SignatureToStems, morphology,FindSuffixesFlag) 

if False:
	print "8. Printing the FSA."
	print >>FileObject[FSA], "#", language, shortfilename, results.wordcount
	morphology.printFSA(FileObject[FSA]) 
 
if False :
	print "9. Printing signatures."
	printSignatures(Lexicon, FileObject["Signatures"], FileObject["WordToSig"], FileObject[StemToWords],FileObject[Suffixes], g_encoding, FindSuffixesFlag,letterCostOfStems, letterCostOfSignatures)

if False:
	print "10. Finding robust peripheral pieces on edges in FSA."
	for loopno in range( NumberOfCorrections):
		morphology.find_highest_weight_affix_in_an_edge ( FileObject["Log"], FindSuffixesFlag)

if False:
	print "11. Printing graphs of the FSA."
	for state in morphology.States:	
		# do not print the entire graph:
		#if state == morphology.startState:
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
  	
#---------------------------------------------------------------------------------#	
#	5d. Print FSA again, with these changes.
#---------------------------------------------------------------------------------# 

if False:
	print "11. Printing the FSA."
	morphology.printFSA(FileObject[FSA])
 
if False:
	print "12. Parsing all words through FSA."
	morphology.parseWords(Lexicon.WordToSig.keys(), FileObject[WordParses])
	
if False:	
	print "13. Printing all the words' parses."
	morphology.printAllParses(FileObject[WordParses])


if False:
	print "14. Now look for common morphemes across different edges."
	morphology.findCommonMorphemes(lxalogfile)

if False:
 
	# we will remove this. It will be replaced by a function that looks at all cross-edge sharing of morphemes. 
	print >>FileObject[FSA], "Finding common stems across edges."
	HowManyTimesToCollapseEdges = 0
	for loop in range(HowManyTimesToCollapseEdges): 
	 	print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		print  "Loop number", loop
	 	print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
		(commonEdgePairs,  EdgeToEdgeCommonMorphs) = morphology.findCommonStems(lxalogfile)
	 
		if len( commonEdgePairs ) == 0:
			print "There are no more pairs of edges to consider."
			break
		edge1, edge2 = commonEdgePairs[0]
		state1 = edge1.fromState
		state2 = edge2.fromState
		state3 = edge1.toState
		state4 = edge2.toState
		print "\n\nWe are considering merging edge ", edge1.index,"(", edge1.fromState.index, "->", edge1.toState.index, ") and  edge", edge2.index, "(", edge2.fromState.index, "->", edge2.toState.index , ")"
		 
		print "Printed graph", str(loop), "before_merger"
		graph = morphology.createDoublePySubgraph(state1,state2) 	
		graph.layout(prog='dot')
		filename = graphicsfolder +  str(loop) + '_before_merger' + str(state1.index) + "-" + str(state2.index) + '.png'
		graph.draw(filename) 

		if state1 == state2:
			print "The from-States are identical"
			state_changed_1 = state1
			state_changed_2 = state2
			morphology.mergeTwoStatesCommonMother(state3,state4)
			morphology.EdgePairsToIgnore.append((edge1, edge2))

		elif state3 == state4:
			print "The to-States are identical"
			state_changed_1 = state3
			state_changed_2 = state4	 
			morphology.mergeTwoStatesCommonDaughter(state1,state2) 
			morphology.EdgePairsToIgnore.append((edge1, edge2))

		elif morphology.mergeTwoStatesCommonMother(state1,state2):
			print "Now we have merged two sister edges from line 374 **********"
			state_changed_1 = state1
			state_changed_2 = state2
			morphology.EdgePairsToIgnore.append((edge1, edge2))

	
		elif   morphology.mergeTwoStatesCommonDaughter((state3,state4))  : 
			print "Now we have merged two daughter edges from line 377 **********"
			state_changed_1 = state3
			state_changed_2 = state4
			morphology.EdgePairsToIgnore.append((edge1, edge2))
			 
		graph = morphology.createPySubgraph(state1) 	
		graph.layout(prog='dot')
		filename = graphicsfolder + str(loop) +  '_after_merger_' + str(state_changed_1.index) +  "-" + str(state_changed_2.index) + '.png'
		print "Printed graph", str(loop), "after_merger"
		graph.draw(filename) 
 

#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#
#		User inquiries about morphology
#------------------------------------------------------------------------------------------#
#------------------------------------------------------------------------------------------#

morphology_copy = morphology.MakeCopy()


initialParseChain = list()
CompletedParses = list()
IncompleteParses = list()
word = "" 
while False:
	word = raw_input('Inquire about a word: ')
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
				print "Edge number", edge.index 
				i = 0
				for morph in edge.labels:
					print "%12s" % morph,
					i+=1
					if i%6 == 0: print 
			print "\n\n"		
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
			print "From state", morphology.Edges[edgeno].fromState.index, "To state", morphology.Edges[edgeno].toState.index
			for edge in morphology.Edges:
				if edge.index == int(edgeno):
					morphlist = list(edge.labels)
			for i in range(len( morphlist )):
				print "%12s" % morphlist[i],
				if i%6 == 0:
					print	
			print "\n\n"
			continue
	if word == "graph":
		while True:
			stateno = raw_input("Graph state number:")
			
	del CompletedParses[:]
	del IncompleteParses[:]
	del initialParseChain[:]
	startingParseChunk = parseChunk("", word)
	startingParseChunk.toState = morphology.startState

	initialParseChain.append(startingParseChunk)
	IncompleteParses.append(initialParseChain)
	while len(IncompleteParses) > 0 :
		CompletedParses, IncompleteParses = morphology.lparse(CompletedParses, IncompleteParses)
	if len(CompletedParses) == 0: print "no analysis found." 
	 
	for parseChain in CompletedParses:
		for thisParseChunk in  parseChain:			
			if (thisParseChunk.edge):				 
				print "\t",thisParseChunk.morph,  
		print 
	print

	for parseChain in CompletedParses:
		print "\tStates: ",
		for thisParseChunk in  parseChain:			
			if (thisParseChunk.edge):				 
				print "\t",thisParseChunk.fromState.index, 
		print "\t",thisParseChunk.toState.index 	 
	print 

	for parseChain in CompletedParses:
		print "\tEdges: ",
		for thisParseChunk in  parseChain:			
			if (thisParseChunk.edge):				 
				print "\t",thisParseChunk.edge.index,
		print
	print "\n\n"



#---------------------------------------------------------------------------------------------------------------------------#  
#---------------------------------------------------------------------------------#	
#	Close output files
#---------------------------------------------------------------------------------# 
for item in fileslist:
	print item
	FileObject[item].close()

 
#---------------------------------------------------------------------------------#	
#	Logging information
#---------------------------------------------------------------------------------# 

localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime

 
FileObject["Log"].close()
#--------------------------------------------------#
