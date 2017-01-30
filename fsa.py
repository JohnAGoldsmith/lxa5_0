import pygraphviz as pgv
from ClassLexicon import ParseChain
from ClassLexicon import parseChunk


# ------------------------------------------------------------------------------------------#


class State_lxa:
    # ----------------------------------------------------------------------------------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, thisIndex, FSA):
        self.index = thisIndex
        self.label = ""
        self.fsa = FSA
        self.acceptingStateFlag = False
        self.deletedFlag = False
        self.maximalDepth = -1

    def findFinalLetterOfIncomingEdges():
        edgelist = self.fsa.getAllEdgesToThisState(self)
        FinalLetterDict = dict()  # its keys are the edges going into this state. Its values are dicts from Final Letters to integer counts.
        for edge in edgelist:
            FinalLetterDict[edge] = dict()
            for morph in edge.labels:
                finalletter = morph[-1]
                if finalletter not in FinalLetterDict[edge]:
                    FinalLetterDict[edge][finalletter] = 1
                else:
                    FinalLetterDict[edge][finalletter] += 1

    def findNumberOfIncomingEdges(self):
        return len(self.getIncomingEdges())

    def getIncomingEdges(self):
        incomingedge = list()
        for edge in self.fsa.Edges:
            if edge.toState == self:
                incomingedge.append(edge)
        return incomingedge

    def getOutgoingEdges(self):
        outgoingedge = list()
        for edge in self.fsa.Edges:
            if edge.fromState == self:
                outgoingedge.append(edge)
        return outgoingedge

    def addLetterToStartOfAllOutedges(Letter):
        outgoingedges = self.getOutgoingEdges()
        for edge in outgoingedges:
            edge.addInitialLetter(InitialLetter)

    def findIdenticalOutEdges(self):
        print
        "\t> Finding identical outedges, labeled identically ", self.index
        myOutEdges = list()
        for edge in self.fsa.Edges:
            if edge.deletedFlag == False and edge.fromState == self:
                myOutEdges.append(edge)
        for i in range(len(myOutEdges)):
            for j in range(i + 1, len(myOutEdges)):
                if '.'.join(myOutEdges[i].labels) == '.'.join(myOutEdges[j].labels):
                    print
                    "\tMerging two edges with identical labels; edge numbers:", myOutEdges[i].index, myOutEdges[j].index
                    self.fsa.mergeTwoStatesCommonMother(myOutEdges[i].toState,
                                                        myOutEdges[j].toState)  # assumes they have a common mother TODO
                    myOutEdges[j].deletedFlag = True
                    myOutEdges[j].fromState = None
                    myOutEdges[j].toState = None
                    myOutEdges[j].dirtyFlag = True
        self.fsa.cleanDeletedStatesAndEdges()
        print
        "\t> End of findIdenticalOutedges"


# ----------------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------------#

class Edge_lxa:
    # ----------------------------------------------------------------------------------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------------------------#

    def __init__(self, thisIndex, instate, outstate, StemFlag):
        self.index = thisIndex
        self.fromState = instate
        self.toState = outstate
        self.labels = []
        self.stemFlag = StemFlag
        self.DoNotChangeList = list()  # a list of those hypotheses about stem-final chunks that have already been rejected and should not be reconsidered.
        self.clean = False  # it is "dirty"  if its best candidate for sub-affix has not yet ever been computed, or if it has been changed recently.
        self.bestChunk = ""
        self.bestChunkWeight = 0
        self.bestChunkCount = 0
        self.deletedFlag = False
        self.dirtyFlag = False

    # ----------------------------------------------------------------------------#
    def changeFromState(self, newstate):
        self.fromState = newstate

    # ----------------------------------------------------------------------------#
    def addLabel(self, label):
        self.labels.append(label)

    # ----------------------------------------------------------------------------#
    def removeLabel(self, label):
        self.labels.remove(label)

    # ----------------------------------------------------------------------------#
    def addLabels(self, labelList):
        for label in labelList:
            self.addLabel(label)
            # ----------------------------------------------------------------------------#

    def printLabels(self):
        for word in self.labels:
            print
            word
            # ----------------------------------------------------------------------------#

    def getIndex(self):
        return self.index

    # ----------------------------------------------------------------------------#

    def getLetterCount(self):
        count = 0
        for label in self.labels:
            if label == "NULL":
                count += 1
            else:
                count += len(label)
        return count

    # ----------------------------------------------------------------------------#
    def testIfAllLabelsEndWithCommonLetter(FinalLetter):
        for label in self.labels:
            if label[-1] != FinalLetter:
                return False
        return True

    # ----------------------------------------------------------------------------#
    def testIfAllLabelsEndWithCommonLetter():
        FinalLetter = self.labels[0][-1]
        if testIfAllLabelsEndWithCommonLetter(FinalLetter):
            return FinalLetter
        else:
            return ""

    # ----------------------------------------------------------------------------#
    def removeFinalLetterFromLabels(FinalLetter):
        labelcopy = list(self.labels[:])
        del self.labels[:]
        for label in labelcopy:
            if label[-1] != FinalLetter:
                return -1
            self.addLabel(label[:-1])
            # ----------------------------------------------------------------------------#

    def addInitialLetter(InitialLetter):
        labelcopy = list(self.labels[:])
        del self.labels[:]
        for label in labelcopy:
            self.addLabel(InitialLetter + label)
            # ----------------------------------------------------------------------------#

    def findMaximalRobustSuffix(wordlist):
        print
        "\tEdge function"
        return maximalrobustsuffix(self.labels)

    # ----------------------------------------------------------------------------#
    def find_highest_weight_affix(self, FindSuffixesFlag, outfile):  # Edge function
        numberOfMorphemesOnThisEdge = len(self.labels)

        maximalchunksize = 5  #
        totalweight = 0
        weightthreshold = 0.02
        MinimalCount = 10
        chunkcounts = {}
        chunkweights = {}
        chunkweightlist = []
        tempdict = {}
        templist = []
        minstemsize = 2
        # -----------------------------#
        exceptionthreshold = 15
        proportionthreshold = .9
        # -----------------------------#

        if self.clean == True:  # this was already found on a previous iteration, and it's still good to go.
            return (self.bestChunk, self.bestChunkWeight, self.bestChunkCount)
        else:
            self.bestChunkWeight = 0
            self.bestChunk = ""
            self.bestChunkCount = 0
            if FindSuffixesFlag:
                for word in self.labels:
                    if word == "NULL":
                        continue
                    for width in range(1,
                                       maximalchunksize + 1):  # width is the size (in letters) of the suffix being considered
                        if width + minstemsize > len(word):
                            break
                        chunk = word[-1 * width:]

                        if not chunk in chunkcounts:
                            chunkcounts[chunk] = 1
                        else:
                            chunkcounts[chunk] += 1

            else:
                for word in self.labels:
                    if word == "NULL":
                        continue
                    for width in range(1,
                                       maximalchunksize + 1):  # width is the size (in letters) of the prefix being considered
                        if width + minstemsize > len(word):
                            break
                        chunk = word[:width]
                        if not chunk in chunkcounts:
                            chunkcounts[chunk] = 1
                        else:
                            chunkcounts[chunk] += 1
            SkipMeFlag = False
            for chunk in chunkcounts.keys():
                this_chunk_count = chunkcounts[chunk]
                chunkweights[chunk] = this_chunk_count * len(chunk)
                if chunkweights[chunk] < weightthreshold * totalweight:
                    continue
                if this_chunk_count < MinimalCount:
                    continue
                ##-------- if this chunk is on the Do Not Change List, then just ignore it and carry on as if it hadn't been there.----------##
                for (someEdge, someChunk, someWeight, someCount) in self.DoNotChangeList:

                    if someChunk == chunk and someWeight == chunkweights[chunk] and someCount == this_chunk_count:
                        SkipMeFlag = True
                        # print >>outfile, "Found this on do not change list"
                        continue
                if SkipMeFlag == True:
                    SkipMeFlag = False
                    continue
                if len(chunk) == 1:
                    ExceptionCount = numberOfMorphemesOnThisEdge - this_chunk_count
                    proportion = 1 - float(ExceptionCount) / float(numberOfMorphemesOnThisEdge)
                    if ExceptionCount < exceptionthreshold and proportion > proportionthreshold:  # and edge.toState.findNumberOfIncomingEdges() == 1:
                        self.bestChunkWeight = chunkweights[chunk]
                        self.bestChunk = chunk
                        self.bestChunkCount = this_chunk_count
                        break
                if chunkweights[chunk] > self.bestChunkWeight:
                    self.bestChunkWeight = chunkweights[chunk]
                    self.bestChunk = chunk
                    self.bestChunkCount = this_chunk_count

        self.clean = True
        return (self.bestChunk, self.bestChunkWeight, self.bestChunkCount)

    # ----------------------------------------------------------------------------#
    def clipCommonSuffix(commonsuffix):
        length = -1 * len(commonsuffix)
        newlabels = []
        for morpheme in self.labels:
            if not morpheme[length:] == commonsuffix:
                return -1
            newlabels.append(morpheme[:len(morpheme) + length])
        self.labels = newlabels
        return 1


# ---------------------------------------------------------------------------#
"""class FSA_change:
		def __init__(self):
			self.type = "" # state-merger, edge-merger
			self.states = None
		def mergeStates ( (state1, state2) ):
			change = SFA_change()
			change.type = "state-merger"
			change.items = (state1,state2)
		def mergeEdges ( (edge1, edge2) ):
			change = SFA_change()
			change.type = "edge-merger"
			change.items = (edge1, edge2)
"""


# ----------------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------------#

class FSA_lxa:
    # ----------------------------------------------------------------------------------------------------------------------------#
    # ----------------------------------------------------------------------------------------------------------------------------#
    def __init__(self, splitEndState=False):
        self.States = list()
        self.StateDict = dict()  # key is index, value is state
        self.Edges = list()
        self.startState = self.addState()  # start state
        self.startState.label = "Start"
        self.endState = self.addState()  # end state
        self.endState.acceptingStateFlag = True
        self.endState.label = "End"
        self.morphemeToEdgeDict = dict()  # key is morpheme, value is a list of the indices of the states it is linked to.

        if splitEndState == True:
            self.splitEndState = True
        else:
            self.splitEndState = False
        # self.historyOfChanges = list() # a history of changes made to the FSA by the learner
        self.wordParseDict = dict()  # the key is the word; the value is a list of parses of the word, where a parse is a list of edges.
        self.EdgePairsToIgnore = list()
        self.WordParses = dict()  # the values of this dict are *lists* of parses, which are themselves lists of "parseChunks" (see below).

    # -----------------------------------------------------------#
    def addState(self):
        thisState = State_lxa(len(self.States), self)
        # print thisState.label
        self.States.append(thisState)
        self.StateDict[thisState.index] = thisState
        return thisState

    # -----------------------------------------------------------#
    def addStateAfter(self, afterState):
        thisState = State_lxa(len(self.States), self)
        for index in range(len(self.States)):
            if self.States[index] == afterState:
                self.States.insert(index + 1, thisState)
        self.StateDict[thisState.index] = thisState
        # print "this state label", thisState.label, "," , afterState.label
        return thisState

    # -----------------------------------------------------------#
    def addEdge(self, stateFrom, stateTo, stemFlag):  # = True):
        thisEdge = Edge_lxa(len(self.Edges), stateFrom, stateTo, stemFlag)
        self.Edges.append(thisEdge)
        assert (stateFrom.index < len(self.States))
        assert (stateTo.index < len(self.States))
        return thisEdge

    # -----------------------------------------------------------#	Copy constructor
    def MakeCopy(self):
        newFSA = FSA_lxa()
        newFSA.WordParses = dict()  # TODO Fix this, make it a copy.
        for state in self.States:
            newstate = State_lxa(state.index, newFSA)
            newstate.acceptingStateFlag = state.acceptingStateFlag
            newstate.label = state.label
            newFSA.StateDict[newstate.index] = newstate
        for edge in self.Edges:
            newedge = Edge_lxa(edge.index, edge.fromState, edge.toState, edge.stemFlag)
            newedge.labels = list(edge.labels)
            newedge.stemFlag = edge.stemFlag
            newedge.DoNotChangeList = list(edge.DoNotChangeList)
            newedge.clean = edge.clean
            newedge.bestChunk = edge.bestChunk
            newedge.bestChunkWeight = edge.bestChunkWeight
            newedge.bestChunkCount = edge.bestChunkCount
            newedge.deletedFlag = edge.deletedFlag
            newedge.dirtyFlag = edge.dirtyFlag
        return newFSA

    # -----------------------------------------------------------#
    def getStateFromIndex(self, index):
        return self.StateDict[index]

    # -----------------------------------------------------------#
    def addChange(self, change):
        self.historyOfChanges.append(change)

    def addEdgeMerger(self, edge1, edge2):
        change1 = FSA_change()
        change1.mergeEdges((edge1, edge2))
        self.historyOfChanges.append(change1)

    # -----------------------------------------------------------#

    def addEdgeAfter(self, stateFrom, stateTo, afterEdge):
        stemFlag = False  # TODO this should be corrected -- we don't know yet if it is.
        correctEdgeNumber = -1
        for index in range(len(self.Edges)):
            if self.Edges[index] == afterEdge:
                correctEdgeNumber = index + 1
                break
        if correctEdgeNumber == -1:
            return False
        thisEdge = self.addEdge(correctEdgeNumber, stateFrom, stateTo, stemFlag)
        self.Edges.insert(index + 1, thisEdge)

        assert (stateFrom.index < len(self.States))
        assert (stateTo.index < len(self.States))
        return thisEdge

    # -----------------------------------------------------------#
    def addEdgeFromSameStartState(self, otherEdge, stateTo):
        thisEdge = Edge_lxa(len(self.Edges), otherEdge.fromState, stateTo, otherEdge.stemFlag)
        for index in range(len(self.Edges)):
            if self.Edges[index] == otherEdge:
                self.Edges.insert(index + 1, thisEdge)
        return thisEdge

    # -----------------------------------------------------------#
    def cleanDeletedStatesAndEdges(self):
        # print "\tWe are in clean Deleted states and edges line 327"
        templist = self.States
        self.States = list()
        for state in templist:
            if state.deletedFlag == False:
                self.States.append(state)
        templist = self.Edges
        self.Edges = list()
        for edge in templist:
            if edge.deletedFlag == False:
                self.Edges.append(edge)
            else:
                print
            "\t\t> We found an edge to eliminate:", edge.index

            # ----------------------------------------------------------------------------#

    def initializeWithWordList(self, wordlist):
        self.addEdge(self.startState, self.endState).addLabels(wordlist)

    # -----------------------------------------------------------#
    def addSignature(self, leftlist, rightlist, suffixFlag):
        if self.splitEndState == True:
            myEndState = self.addState()
            myEndState.acceptingStateFlag = True
        else:
            myEndState = self.endState

        newMiddleState = self.addState()
        if suffixFlag:
            thisedge = self.addEdge(self.startState, newMiddleState, True)
            thisedge.addLabels(leftlist)
            thatedge = self.addEdge(newMiddleState, myEndState, False)
            thatedge.addLabels(rightlist)
        else:
            thisedge = self.addEdge(self.startState, newMiddleState, False)
            thisedge.addLabels(leftlist)
            thatedge = self.addEdge(newMiddleState, myEndState, True)
            thatedge.addLabels(rightlist)
        if suffixFlag:
            for stem in leftlist:
                for affix in rightlist:
                    if affix == "NULL":
                        affix = ""
                        newMiddleState.acceptingStateFlag = True
                    word = stem + affix
                    if not word in self.wordParseDict:
                        self.wordParseDict[word] = list()
                    self.wordParseDict[word].append((thisedge, thatedge))
        else:
            for stem in rightlist:
                for affix in leftlist:
                    if affix == "NULL":
                        affix = ""
                        newMiddleState.acceptingStateFlag = True
                    word = affix + stem
                    if not word in self.wordParseDict:
                        self.wordParseDict[word] = list()
                    self.wordParseDict[word].append((thisedge, thatedge))
                    # -----------------------------------------------------------#
                    #	def addSignatures(self, Signatures, type = "suffixal"):
                    #		tempthreshold = 10
                    #		SortedListOfSignatures = sorted( Signatures.items(), lambda x,y: cmp(len(x[1]), len(y[1]) ) , reverse=True)
                    #		for sig, stemlist in SortedListOfSignatures:
                    #			if len(stemlist) > tempthreshold:
                    #				self.addSignature(stemlist, sig)

                    # -----------------------------------------------------------#

    def getAllEdgesFromThisState(self, thisState):
        edgelist = list()
        for edge in self.Edges:
            if edge.fromState == thisState:
                edgelist.append(edge)
        return edgelist

    # -----------------------------------------------------------#
    def getAllEdgesToThisState(self, thisState):
        edgelist = list()
        for edge in self.Edges:
            if edge.toState == thisState:
                edgelist.append(edge)
        return edgelist

    # -----------------------------------------------------------#
    # this function and the one after it (find common stems on two edges) is used to determine if two edges might be collapsed into one, allowing their mother states to be merged.
    def updateMorphemeToEdgeDict(self):
        self.morphemeToEdgeDict = dict()
        for edge in self.Edges:
            edgeno = edge.index
            for label in edge.labels:
                if label not in self.morphemeToEdgeDict:
                    self.morphemeToEdgeDict[label] = []
                self.morphemeToEdgeDict[label].append(edgeno)

                # -----------------------------------------------------------#

    def findCommonStemsOnTwoEdges(self, edge1, edge2):  # returns list of morphs shared by two edges
        sharedMorphs = list()
        for morph in edge1.labels:
            if edge2 in self.morphemeToEdgeDict[morph]:
                sharedMorphs.append(morph)
        return sharedMorphs

    # -----------------------------------------------------------#
    def testIfAllIncomingEdgesEndWithCommonLetter(thisState, CommmonLetter):
        edgelist = getAllEdgesToThisState(self, thisState)
        for edge in edgelist:
            if testIfAllLabelsEndWithCommonLetter(FinalLetter) == False:
                return False
        return True

    # -----------------------------------------------------------#
    def getLetterCount(self):
        count = 0
        for edge in self.Edges:
            count += edge.getLetterCount()
        return count

    # -----------------------------------------------------------#
    def printAllParses(self, outfile):
        wordlist = self.WordParses.keys()
        wordlist.sort()
        print
        "in printallparses, with this many words", len(wordlist)
        for word in wordlist:
            print >> outfile, word
            if self.WordParses[word]:
                for parsechain in self.WordParses[word]:
                    parsechain.Print(outfile)
            print >> outfile

            # -----------------------------------------------------------#

    def printFSA(self, outfile=None):
        numberOfColumns = 6
        colwidth = 15
        print
        "FSA has letter count: ", str(self.getLetterCount() / 1000) + "K."
        Morphemes = dict()

        for edge in self.Edges:
            # if edge.stemFlag == True:
            for item in edge.labels:
                if edge not in Morphemes:
                    Morphemes[item] = list()
                Morphemes[item].append(edge.index)
        DubiousMorphemes = dict()
        for stem in Morphemes:
            if stem[:-1] in Morphemes:
                DubiousMorphemes[stem] = 1
                DubiousMorphemes[stem[:-1]] = 1
        for stem in sorted(Morphemes):
            # if stem in DubiousMorphemes:
            #	print >>outfile, stem, "*"
            # else:
            print >> outfile, stem

        for state in self.States:
            print >> outfile, "\n\nState number: ", state.index, "accepting state? ", state.acceptingStateFlag
            for edge in self.Edges:
                if edge.fromState == state:
                    printlist = list()
                    print >> outfile, "\n\tEdge number", edge.index, "To state:", edge.toState.index,
                    if edge.stemFlag == False:
                        print >> outfile, "Affix"
                    if edge.stemFlag == True:
                        print >> outfile, "Stem"
                    colno = 0
                    reverselist = list()
                    # del edge.labels[:]
                    for item in edge.labels:
                        temp = item[::-1]
                        reverselist.append(temp)
                    reverselist.sort()
                    for item in reverselist:
                        printlist.append(item[::-1])
                    for label in printlist:
                        if colno == numberOfColumns:
                            colno = 0
                            print >> outfile
                            continue
                        print >> outfile, label.rjust(20),
                        colno += 1
                    print >> outfile
        print >> outfile, "---------------------------------------------------------------"

    # -------------------------------#

    def find_highest_weight_affix_in_an_edge(self, outfile, FindSuffixesFlag):

        candidates = list()
        candidatelist = list()

        # -----------------------------#
        exceptionthreshold = 15
        proportionthreshold = .9
        # -----------------------------#


        for edge in self.Edges:
            (chunk, weight, count) = edge.find_highest_weight_affix(FindSuffixesFlag, outfile)
            if len(chunk):
                candidates.append((edge, chunk, weight, count))
        candidatelist = sorted(candidates, key=lambda features: features[2], reverse=True)

        # print "\tafter first edge loop"

        if len(candidatelist) == 0:
            print >> outfile, "No more candidates found."
            return 0

        (bestedge, bestchunk, bestweight, bestcount) = candidatelist[0]

        print >> outfile, "_" * 80
        print >> outfile, bestchunk, ' ' * (
            10 - len(bestchunk)), bestedge.index, "weight: ", bestweight, ", and count:", bestcount, "out of", len(
            bestedge.labels), "on its edge."
        print >> outfile, "_" * 80
        # print "\t before len best chunk"
        if len(bestchunk) == 1:  # we set higher conditions on this re-analysis
            # print "\t len is 1"
            numberOfMorphemesOnThisEdge = len(bestedge.labels)
            ExceptionCount = numberOfMorphemesOnThisEdge - bestcount
            proportion = 1 - float(ExceptionCount) / float(numberOfMorphemesOnThisEdge)
            if ExceptionCount < exceptionthreshold and proportion > proportionthreshold:  # and edge.toState.findNumberOfIncomingEdges() == 1:
                self.splitSignature(bestedge, bestchunk, FindSuffixesFlag, outfile)
                bestedge.clean = False
                return 1
            else:
                bestedge.DoNotChangeList.append((bestedge, bestchunk, bestweight, bestcount))
                bestedge.clean = False
                # print >>outfile, "This went on Do Not Change list" , ExceptionCount, proportion
        else:
            # print "\t len is not 1"
            self.splitSignature(bestedge, bestchunk, FindSuffixesFlag, outfile)
            bestedge.clean = False
            return 1

            # -----------------------------------------------------------#

    def splitSignature(self, edge, stemcondition, FindSuffixesFlag, outfile):
        # stemedge and suffixedge indicate a signature: with a sequential structure.
        # This function will create a new middle state, and move all stems that end with "stemcondition"
        # to that new state.

        stemconditionlength = len(stemcondition)
        stems = []
        newMidState = self.addStateAfter(edge.fromState)

        print >> outfile, "\tOld stem      New stem:\n\n",
        if FindSuffixesFlag == True:
            for stem in edge.labels:
                if stem[-1 * len(stemcondition):] == stemcondition:
                    stems.append(stem)
            # print "\t A"
            if len(stems) == 0:
                return;
            if len(stems) == len(
                    edge.labels) and edge.toState.findNumberOfIncomingEdges == 1:  # all the stems would be moved! Unnecessary.
                newedge2 = self.addEdge(newMidState, edge.toState)
                newedge2.addLabel(stemcondition)
                templist = list(edge.labels)
                del edge.labels[:]
                for string in templist:
                    edge.labels.append(string[: -1 * stemconditionlength])
                    # print "\t B"
            else:  # normal case:
                newedge1 = self.addEdgeFromSameStartState(edge, newMidState)
                newedge2 = self.addEdge(newMidState, edge.toState, False)
                for stem in stems:
                    edge.removeLabel(stem)
                    newstem = stem[:-1 * stemconditionlength]
                    newedge1.addLabel(newstem)
                    print >> outfile, "\t\t", stem, " " * (15 - len(stem)), newstem
                newedge2.addLabel(stemcondition)
                # print "\t C"
        else:  # Prefix case
            for stem in edge.labels:
                if stem[:len(stemcondition)] == stemcondition:
                    stems.append(stem)
            if len(stems) == 0:
                return;
            if len(stems) == len(edge.labels):  # all the stems would be moved! Unnecessary.
                newedge2 = self.addEdge(edge.fromState, newMidState, False)
                newedge2.addLabel(stemcondition)
                templist = list(edge.labels)
                del edge.labels[:]
                for string in templist:
                    edge.labels.append(string[stemconditionlength:])
                edge.changeFromState(newMidState)
            else:  # normal case:
                # print "breaking off ", stemcondition
                newedge1 = self.addEdgeFromSameStartState(edge, newMidState)
                newedge2 = self.addEdge(newMidState, edge.toState, False)
                for stem in stems:
                    edge.removeLabel(stem)
                    stem = stem[stemconditionlength:]
                    newedge2.addLabel(stem)
                newedge1.addLabel(stemcondition)

        return

    # -----------------------------------------------------------#
    def shiftSingleLetterPeripherally(self, edge, Letter, FindSuffixesFlag):
        # This function takes a letter (Letter) at the end of a set of labels on an edge, and shifts it to the labels of the following edge,
        # if no other edges enter that state.


        goodMorphs = list()
        if FindSuffixesFlag == True:  # Suffix case
            nextState = edge.toState

            if nextState.findNumberOfIncomingEdges() > 1:
                print
                "Problem! shiftSingleLetterPeripherally"

            for morph in edge.labels:
                if morph[-1:] == Letter:
                    goodMorphs.append(morph)
            if len(goodMorphs) == 0:
                return;
            if len(goodMorphs) == len(
                    edge.labels):  # all 'stems' end with the Letter; so we don't need to create any new nodes
                del edge.labels[:]
                for string in goodMorphs:
                    edge.labels.append(string[1:])
                nextStateOutEdges = nextState.getOutgoingEdges()
                for edge in nextStateOutEdges:
                    edge.addInitialLetter(Letter)

            else:  # more normal case:
                newedge1 = self.addEdgeFromSameStartState(edge, newMidState)
                newedge2 = self.addEdge(newMidState, edge.toState)
                labelcopy = list(edge.labels)
                del edge.labels[:]
                for morph in labelcopy:
                    if morph[-1] == Letter:
                        newedge1.addLabel(morph[:-1])
                    else:
                        edge.addLabel(morph)
                nextState.addLetterToStartOfAllOutedges(Letter)

        if FindSuffixesFlag == False:  # Prefix case
            if edge.fromState == self.startState:  # This means the edge we are looking at is at the periphery, no good...
                return

            fromState = edge.fromState
            for edge in self.Edges:
                if edge.toState == fromState:
                    motherEdge = edge  # This is where we make the assumption that each prefix has only one state "before" it.
                    break
            for morph in edge.labels:
                if morph[-1:] == stemcondition:
                    stems.append(morph)
            if len(stems) == 0:
                return;
            if len(stems) == len(
                    edge.labels):  # all 'stems' end with the Letter; so we don't need to create any new nodes
                labelcopy = list(edge.labels())
                del edge.labels[:]
                for string in labelcopy:
                    edge.labels.append(string[1:])
            else:  # normal case:
                newedge1 = self.addEdgeFromSameStartState(edge, newMidState)
                newedge2 = self.addEdge(newMidState, edge.toState)
                labelcopy = list(edge.labels)
                for morph in motherEdge:
                    newedge1.addLabel(morph + Letter)
                del edge.labels[:]
                for morph in labelcopy:
                    if morph[0] == Letter:
                        morph = morph[1:]
                        newedge2.addLabel(morph)
                newedge2.addLabel(stemcondition)

        return

    # -----------------------------------------------------------#
    def clipCommonSuffix(edge, commonsuffix):  # Not used.
        # ----------------------------------------------#
        # This snips off a common suffix of a bunch of strings and puts it onto a following new edge
        # ----------------------------------------------#
        results = edge.clipCommonSuffix(commonsuffix)
        if results < 0:  # if some label on this edge does not in fact end with commonsuffix
            return
        newState = self.addState()
        newEdge = self.addEdge(newState, edge.toState)
        edge.toState = newState
        edge.label = commonsuffix
        return

    # -----------------------------------------------------------#
    def mergeTwoStatesCommonMother(self, state1, state2):  # assumes they have a common mother
        # ------------------- Check if they lie in parallel  ----------------------------------------#
        # That is, if one of them simply extends the other.
        for edge in self.Edges:
            if edge.fromState == state1 and edge.toState == state2:
                # print "line 644"
                newedge = self.addEdge(state1, state2, True)  # TODO we don't know if this is true or false
                newedge.labels.append("NULL")
                # print "\t Merge 2 states common mother one extends the other"
                return
            elif edge.fromState == state2 and edge.toState == state1:
                # print "line 649"
                # print "\t merge 2 states common mother one extends the other"
                newedge = self.addEdge(state2, state1, True)  # TODO we don't know if this is true or false
                newedge.labels.append("NULL")
                return

        # ------------------- Find edges to state1 and state2  ----------------------------------------#
        for edge in self.Edges:
            if edge.deletedFlag == True:
                continue
            if edge.toState == state2:
                edge.toState = state1
            # print "\t1m. We are changing edge", edge.index, ", which went from state",  edge.fromState.index, "to", state2.index
            # print "\t2m. It now goes to state", state1.index
            if edge.fromState == state2:
                edge.fromState = state1
                # print "\t3m. We are changing edge", edge.index, ", which went from state",  state2.index, "to state", edge.toState.index
                # print "\t4m. It now goes from state", state1.index, "(and its to-state is unchanged)."
                edge.dirtyFlag = True

        self.lookForTwinEdges()
        state1.findIdenticalOutEdges()

        return True

    # -----------------------------------------------------------#
    def mergeTwoStatesCommonDaughter(self, state1, state2):  # assumes they have a common daughter

        # ------------------- Check if they lie in parallel  ----------------------------------------#
        # That is, if one of them simply extends the other.
        for edge in self.Edges:
            if edge.fromState == state1 and edge.toState == state2:
                newedge = self.addEdge(state1, state2, True)  # TODO we don't know if this is true or false
                newedge.labels.append("NULL")
                print
                "\t merge 2 states common daughter one extends the other"
                return
            elif edge.fromState == state2 and edge.toState == state1:
                newedge = self.addEdge(state2, state1, True)  # TODO we don't know if this is true or false
                newedge.labels.append("NULL")
                print
                "\t merge 2 states common daughter one extends the other"
                return

        # ------------------- Find edges to state1 and state2  ----------------------------------------#
        for edge in self.Edges:
            if edge.deletedFlag == True:
                continue
            if edge.toState == state2:
                edge.toState = state1
            # print "\t1m. We are changing edge", edge.index, ", which went from state",  edge.fromState.index, "to", state2.index
            # print "\t2m. It now goes to state", state1.index
            if edge.fromState == state2:
                edge.fromState = state1
                # print "\t3m. We are changing edge", edge.index, ", which went from state",  state2.index, "to state", edge.toState.index
                # print "\t4m. It now goes from state", state1.index, "(and its to-state is unchanged)."
                edge.dirtyFlag = True
        self.lookForTwinEdges()
        state1.findIdenticalOutEdges()
        return True

    # -----------------------------------------------------------#
    def lookForTwinEdges(
            self):  # this might blow up if there are 3 or more twins on a single node. Plan for this. TODO
        ActionList = list()
        Threshold = 10
        print
        "\tLooking for twin edges"
        for e1 in range(len(self.Edges)):
            edge1 = self.Edges[e1]
            # print edge1.index, edge1.stemFlag, edge1.labels
            # if edge1.deletedFlag:
            #	continue
            for e2 in range(e1 + 1, len(self.Edges)):
                edge2 = self.Edges[e2]
                # if edge2.deletedFlag:
                #	continue
                if edge1.fromState == edge2.fromState and edge1.toState == edge2.toState:
                    # print "\tSame from and to", edge1.index, edge2.index
                    # if  edge1.stemFlag == True and edge2.stemFlag == True  : # TODO this flag is not working right. Fix It.
                    if len(edge1.labels) > Threshold and len(edge2.labels) > Threshold:
                        ActionList.append((edge1, edge2))

        for (edge1, edge2) in ActionList:
            self.mergeTwoTwinEdges(edge1, edge2)

            # -----------------------------------------------------------#

    def mergeTwoTwinEdges(self, edge1, edge2):
        print
        "\n\tMerging two sister edges", edge1.index, edge2.index
        if edge1.fromState != edge2.fromState or edge1.toState != edge2.toState:
            print
            "Problem...edge1", edge1.fromState.index, edge1.toState.index, edge2.fromState.index, edge2.toState.index
            return None
        edge1.labels.extend(edge2.labels)
        del edge2.labels[:]
        edge2.deletedFlag = True
        edge2.fromState = None
        edge2.toState = None
        self.cleanDeletedStatesAndEdges()

    # -----------------------------------------------------------#
    # -----------------------------------------------------------#
    def shiftLettersToRight(self, sizethreshold, exceptionalthreshold, proportionthreshold, proportion,
                            MaximalLettersToShift, outfile, FindSuffixesFlag):
        for loopno in range(MaximalLettersToShift):
            for edge in self.Edges:
                stemlist = sorted(edge.labels)
                if len(stemlist) < sizethreshold:
                    continue
                (CommonLastLetter, ExceptionCount, proportion) = TestForCommonSuffix(stemlist, outfile,
                                                                                     FindSuffixesFlag)
                if ExceptionCount <= exceptionthreshold and proportion >= proportionthreshold:
                    StemToWord, newsig = ShiftFinalLetter(StemToWord, StemCounts, stemlist, CommonLastLetter, sig,
                                                          FindSuffixesFlag, outfile)
                    print >> outfile, outputtemplate % (sig, newsig, CommonLastLetter, proportion)
            NoLengthLimitFlag = True
            # -----------------------------------------------------------#

    def createPygraph(self):
        Graph = pgv.AGraph(strict=False, directed=True)
        for state in self.States:
            n = Graph.add_node(str(state.index), index=state.index)
        # print state.index
        for edge in self.Edges:
            Graph.add_edge(str(edge.fromState.index), str(edge.toState.index), edge.labels)
        return Graph

        # -----------------------------------------------------------#
        def computeMaximalDepths(self):
            """ Finds the longest path to the root for each state."""

        self.startState.maximalDepth = 0
        # This flag keeps track of whether there are states whose depth is not yet computed
        ComputationCompleteFlag = False
        while ComputationCompleteFlag == False:
            ComputationCompleteFlag = True
            for state in self.States:
                if state.maximalDepth >= 0:
                    continue
                arewereadyflag = True
                thismaximum = -1
                for edge in getAllEdgesFromThisState(self, state):
                    state2 = edge.fromState
                    if state2.maximalDepth < 0:
                        arewereadyflag = False
                        ComputationCompleteFlag = False
                        break
                    elif thismaximum < state2.maximalDepth + 1:
                        thismaximum = state2.maximalDepth + 1
                if arewereadyflag == True:
                    state.maximalDepth = thismaximum

                    # -----------------------------------------------------------#

    def createPySubgraph(self, node_lxa):
        Graph = pgv.AGraph(strict=False, directed=True)
        tempStateIndexDict_L = dict()
        tempStateIndexDict_L[node_lxa.index] = 1
        tempStateIndexDict_R = dict()
        tempStateIndexDict_R[node_lxa.index] = 1
        tempEdgeDict_L = dict()
        tempEdgeDict_R = dict()

        while (True):
            NewEdgeAddedFlag = False
            # iterate through edges...
            for edge in self.Edges:
                if edge.deletedFlag == True:
                    continue
                toNode = edge.toState.index
                fromNode = edge.fromState.index
                # ... if this-edge hasn't been identified in the Left side yet, and its source hasn't been either, and it goes TO a state in the left side...
                if toNode in tempStateIndexDict_L and edge not in tempEdgeDict_L and fromNode not in tempStateIndexDict_L:
                    # ...then put its source state in the Left dict.
                    tempStateIndexDict_L[edge.fromState.index] = 1
                # ... if this edge goes TO a state in the left side, and this-edge hasn't been identified in the Left side yet...
                if toNode in tempStateIndexDict_L and edge not in tempEdgeDict_L:
                    # ...put this-edge in the Edge set, with the flag set as True
                    tempEdgeDict_L[edge] = 1
                    NewEdgeAddedFlag = True
            if NewEdgeAddedFlag == False:
                break
        while (True):
            NewEdgeAddedFlag = False
            for edge in self.Edges:
                if edge.deletedFlag == True:
                    continue
                toNode = edge.toState.index
                fromNode = edge.fromState.index
                # same thing on the right side:
                # if this edge goes FROM a state in the right side, its target hasn't been identified in the Right side yet, and the edge has not been identified...
                if fromNode in tempStateIndexDict_R and edge not in tempEdgeDict_R and toNode not in tempStateIndexDict_R:
                    # ...put its target in the Right dict
                    tempStateIndexDict_R[edge.toState.index] = 1
                if fromNode in tempStateIndexDict_R and edge not in tempEdgeDict_R:
                    tempEdgeDict_R[edge] = 1
                    NewEdgeAddedFlag = True
                    # else: print
            if NewEdgeAddedFlag == False:
                break

        for state in tempStateIndexDict_L:
            Graph.add_node(state)
        for state in tempStateIndexDict_R:
            Graph.add_node(state)

        for edge in tempEdgeDict_L:
            mylabel = ""
            for morph in edge.labels:
                morph = morph.decode('ascii', 'ignore')
                mylabel += morph + "-"
            # if edge.stemFlag == False:
            #	mylabel += "*"
            if len(mylabel) < 10:
                # print mylabel
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=mylabel.encode('ascii', 'replace'))
            else:
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=str(edge.index))
        for edge in tempEdgeDict_R:
            mylabel = ""
            for morph in edge.labels:
                morph = unicode(morph, errors='replace')
                mylabel += morph + "-"
            # if edge.stemFlag == False:
            #	mylabel += "*"
            if len(edge.labels) < 10:
                # print mylabel
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=mylabel.encode('ascii', 'replace'))
            else:
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=str(edge.index))
        return Graph

    # -----------------------------------------------------------#

    # -----------------------------------------------------------#
    def createPySubgraphMinimalDepth(self, minimaldepth):
        Graph = pgv.AGraph(strict=False, directed=True)
        tempStateIndexDict_L = dict()
        tempStateIndexDict_L[node_lxa.index] = 1
        tempStateIndexDict_R = dict()
        tempStateIndexDict_R[node_lxa.index] = 1
        tempEdgeDict_L = dict()
        tempEdgeDict_R = dict()

        while (True):
            NewEdgeAddedFlag = False
            # iterate through edges...
            for edge in self.Edges:
                if edge.deletedFlag == True:
                    continue
                toNode = edge.toState.index
                fromNode = edge.fromState.index
                # ... if this-edge hasn't been identified in the Left side yet, and its source hasn't been either, and it goes TO a state in the left side...
                if toNode in tempStateIndexDict_L and edge not in tempEdgeDict_L and fromNode not in tempStateIndexDict_L:
                    # ...then put its source state in the Left dict.
                    tempStateIndexDict_L[edge.fromState.index] = 1
                # ... if this edge goes TO a state in the left side, and this-edge hasn't been identified in the Left side yet...
                if toNode in tempStateIndexDict_L and edge not in tempEdgeDict_L:
                    # ...put this-edge in the Edge set, with the flag set as True
                    tempEdgeDict_L[edge] = 1
                    NewEdgeAddedFlag = True
            if NewEdgeAddedFlag == False:
                break
        while (True):
            NewEdgeAddedFlag = False
            for edge in self.Edges:
                if edge.deletedFlag == True:
                    continue
                toNode = edge.toState.index
                fromNode = edge.fromState.index
                # same thing on the right side:
                # if this edge goes FROM a state in the right side, its target hasn't been identified in the Right side yet, and the edge has not been identified...
                if fromNode in tempStateIndexDict_R and edge not in tempEdgeDict_R and toNode not in tempStateIndexDict_R:
                    # ...put its target in the Right dict
                    tempStateIndexDict_R[edge.toState.index] = 1
                if fromNode in tempStateIndexDict_R and edge not in tempEdgeDict_R:
                    tempEdgeDict_R[edge] = 1
                    NewEdgeAddedFlag = True
                    # else: print
            if NewEdgeAddedFlag == False:
                break

        for state in tempStateIndexDict_L:
            Graph.add_node(state)
        for state in tempStateIndexDict_R:
            Graph.add_node(state)

        for edge in tempEdgeDict_L:
            mylabel = ""
            for morph in edge.labels:
                morph = morph.decode('ascii', 'ignore')
                mylabel += morph + "-"
            if edge.stemFlag == False:
                mylabel += "*"
            if len(mylabel) < 10:
                # print mylabel
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=mylabel.encode('ascii', 'replace'))
            else:
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=str(edge.index))
        for edge in tempEdgeDict_R:
            mylabel = ""
            for morph in edge.labels:
                morph = unicode(morph, errors='replace')
                mylabel += morph + "-"
            if edge.stemFlag == False:
                mylabel += "*"
            if len(edge.labels) < 10:
                # print mylabel
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=mylabel.encode('ascii', 'replace'))
            else:
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=str(edge.index))
        return Graph

    # -----------------------------------------------------------#



    # -----------------------------------------------------------#
    def createDoublePySubgraph(self, node1, node2):
        Graph = pgv.AGraph(strict=False, directed=True)

        tempStateIndexDict_L = dict()  # This is a dict of states (or rather, their indexes) that precede node1 (or node2, resp.)
        tempStateIndexDict_R = dict()  # This is a dict of state indexes that follow node1 (or node2, resp.)
        tempEdgeDict_L = dict()  # These are the edges we will want to draw, too.
        tempEdgeDict_R = dict()
        tempEdgeDict = dict()
        for loopno in range(2):

            if loopno == 0:
                node_lxa = node1.index
            else:
                node_lxa = node2.index
            tempStateIndexDict_L[node_lxa] = 1  # We include the node that we are focusing on...
            tempStateIndexDict_R[node_lxa] = 1
            while (True):
                NewEdgeAddedFlag = False
                for edge in self.Edges:
                    if edge.deletedFlag == True:
                        continue
                    toNode = edge.toState.index
                    fromNode = edge.fromState.index
                    if toNode in tempStateIndexDict_L and edge not in tempEdgeDict_L and fromNode not in tempStateIndexDict_L:
                        tempStateIndexDict_L[edge.fromState.index] = 1
                    if toNode in tempStateIndexDict_L and edge not in tempEdgeDict_L:
                        tempEdgeDict_L[edge] = 1
                        NewEdgeAddedFlag = True
                if NewEdgeAddedFlag == False:
                    break
            while (True):
                NewEdgeAddedFlag = False
                for edge in self.Edges:
                    if edge.deletedFlag == True:
                        continue
                    toNode = edge.toState.index
                    fromNode = edge.fromState.index
                    if fromNode in tempStateIndexDict_R and edge not in tempEdgeDict_R and toNode not in tempStateIndexDict_R:
                        tempStateIndexDict_R[edge.toState.index] = 1
                    if fromNode in tempStateIndexDict_R and edge not in tempEdgeDict_R:
                        tempEdgeDict_R[edge] = 1
                        NewEdgeAddedFlag = True
                        # else: print
                if NewEdgeAddedFlag == False:
                    break

        for state in tempStateIndexDict_L:
            Graph.add_node(state)
        for state in tempStateIndexDict_R:
            Graph.add_node(state)

        for edge in tempEdgeDict_L:
            if edge in tempEdgeDict:
                continue
            tempEdgeDict[edge] = 1
            mylabel = ""
            for morph in edge.labels:
                morph = unicode(morph, errors='replace')
                mylabel += morph + "-"
            if edge.stemFlag == False:
                mylabel += "*"
            if len(mylabel) < 10:
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=mylabel.encode('ascii', 'ignore'))
            else:
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=str(edge.index))

        for edge in tempEdgeDict_R:
            if edge in tempEdgeDict:
                continue
            tempEdgeDict[edge] = 1
            mylabel = ""
            for morph in edge.labels:
                morph = unicode(morph, errors='replace')
                mylabel += morph + "-"
            if edge.stemFlag == False:
                mylabel += "*"
            if len(edge.labels) < 10:
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=mylabel.encode('ascii', 'ignore'))
            else:
                Graph.add_edge(edge.fromState.index, edge.toState.index, label=str(edge.index))

        return Graph

    # -----------------------------------------------------------#
    def createSubgraph(self, node_lxa):
        Graph = FSA_lxa
        tempStateIndexDict_L = dict()
        tempStateIndexDict_L[node_lxa.index] = 1
        tempStateIndexDict_R = dict()
        tempStateIndexDict_R[node_lxa.index] = 1
        tempEdgeDict_L = dict()
        tempEdgeDict_R = dict()

        while (True):
            NewEdgeAddedFlag = False
            for edge in self.Edges:
                if edge.deletedFlag == True:
                    continue
                toNode = edge.toState.index
                fromNode = edge.fromState.index
                if toNode in tempStateIndexDict_L and edge not in tempEdgeDict_L and fromNode not in tempStateIndexDict_L:
                    tempStateIndexDict_L[edge.fromState.index] = 1
                if toNode in tempStateIndexDict_L and edge not in tempEdgeDict_L:
                    tempEdgeDict_L[edge] = 1
                    NewEdgeAddedFlag = True
            if NewEdgeAddedFlag == False:
                break
        while (True):
            NewEdgeAddedFlag = False
            for edge in self.Edges:
                if edge.deletedFlag == True:
                    continue
                toNode = edge.toState.index
                fromNode = edge.fromState.index
                if fromNode in tempStateIndexDict_R and edge not in tempEdgeDict_R and toNode not in tempStateIndexDict_R:
                    tempStateIndexDict_R[edge.toState.index] = 1
                if fromNode in tempStateIndexDict_R and edge not in tempEdgeDict_R:
                    tempEdgeDict_R[edge] = 1
                    NewEdgeAddedFlag = True
                    # else: print
            if NewEdgeAddedFlag == False:
                break

        for state in tempStateIndexDict_L:
            Graph.addState(state)
        for state in tempStateIndexDict_R:
            Graph.addState(state)

        for edge in tempEdgeDict_L:
            mylabel = ""
            for morph in edge.labels:
                morph = morph.decode('ascii', 'ignore')
                mylabel += morph + "-"
            if edge.stemFlag == False:
                mylabel += "*"
            if len(mylabel) < 10:
                print
                mylabel
                Graph.addEdge(edge.fromState.index, edge.toState.index, label=mylabel.encode('ascii', 'replace'))
            else:
                Graph.addEdge(edge.fromState.index, edge.toState.index, label=str(edge.index))
        for edge in tempEdgeDict_R:
            mylabel = ""
            for morph in edge.labels:
                morph = unicode(morph, errors='replace')
                mylabel += morph + "-"
            if edge.stemFlag == False:
                mylabel += "*"
            if len(edge.labels) < 10:
                print
                mylabel
                Graph.addEdge(edge.fromState.index, edge.toState.index, label=mylabel.encode('ascii', 'replace'))
            else:
                Graph.addEdge(edge.fromState.index, edge.toState.index, label=str(edge.index))
        return Graph

    # -----------------------------------------------------------#

    def findCommonMorphemes(self, outfile):
        CommonMorphemes = dict()  # key is pair of edges, value is list of morphemes
        for index1 in range(len(self.Edges)):
            # print "\nindex1 ", index1
            for index2 in range(index1 + 1, len(self.Edges)):
                for morph in self.Edges[index1].labels:
                    # print morph
                    if index2 in self.morphemeToEdgeDict:
                        if (index1, index2) not in CommonMorphemes:
                            CommonMorphemes[(index1, index2)] = list()
                        CommonMorphemes[(index1, index2)].append(morph)
                        print >> outfile, index1, index2, morph
                        # print morph




                        # -----------------------------------------------------------#
                        #	def printpyvizgraph (Graph, filename):
                        #		Graph.draw(filename)

                        # -----------------------------------------------------------#
                        #	Find common stems
                        #
                        #	Look at edges with stems, and find stems in common
                        # this will be replaced -- it's very clunky and poorly done.
                        # -----------------------------------------------------------#

    def findCommonStems(self, outfile):
        ThisPairIsBadFlag = False
        print
        "Finding common stems"
        EdgeToEdgeCommonMorphs = dict()
        for edgeno in range(len(self.Edges)):
            ThisPairIsBadFlag == False
            edge1 = self.Edges[edgeno]
            for edgeno2 in range(edgeno + 1, len(self.Edges)):
                edge2 = self.Edges[edgeno2]
                ThisPairIsBadFlag == False
                for pair in self.EdgePairsToIgnore:
                    if pair == (edge1, edge2) or pair == (edge2, edge1):
                        print
                        "\tA: found pair that should not be reconsidered", edge1.index, edge2.index
                        ThisPairIsBadFlag = True
                        continue
                if ThisPairIsBadFlag == False:
                    for morph in edge1.labels:
                        if morph in edge2.labels:
                            if (edge1, edge2) not in EdgeToEdgeCommonMorphs:
                                EdgeToEdgeCommonMorphs[(edge1, edge2)] = list()
                            EdgeToEdgeCommonMorphs[(edge1, edge2)].append(morph)
        for (edge1, edge2) in EdgeToEdgeCommonMorphs.keys():
            if len(EdgeToEdgeCommonMorphs[(edge1, edge2)]) < 5:
                del EdgeToEdgeCommonMorphs[(edge1, edge2)]
            else:
                print >> outfile, edge1.labels
                print >> outfile, edge2.labels

                print
                "***"
                print
                edge1.labels
                print
                edge2.labels
                print
                "common: ", EdgeToEdgeCommonMorphs[(edge1, edge2)]

        if len(EdgeToEdgeCommonMorphs) == 0:
            print
            "There are no edge pairs that have been nominated!"

        # This may be changed. TODO
        # Only consider edges that share either a mother or a daughter node
        motherState = None
        daughterState = None
        for (edge1, edge2) in EdgeToEdgeCommonMorphs.keys():
            for edge3 in self.Edges:
                if edge3.toState == edge1.fromState:
                    for edge4 in self.Edges:
                        if edge4.fromState == edge3.fromState and edge4.toState == edge2.fromState:
                            motherState = edge3.fromState
                            # print "\t(", edge1.index, edge2.index, ") Found common mother state", motherState.index
            if motherState != None:
                for edge3 in self.Edges:
                    if edge3.fromState == edge1.toState:
                        for edge4 in self.Edges:
                            if edge4.toState == edge3.toState and edge4.fromState == edge2.toState:
                                daughterState = edge4.toState
                                print
                                "\t(", edge1.index, edge2.index, ") Found common daughter state", daughterState.index
            if daughterState == None and motherState == None:
                print
                "\tDeleting (", edge1.index, edge2.index, ") because they have no mother or daughter in common."
                del EdgeToEdgeCommonMorphs[(edge1, edge2)]

        commonEdgePairs = EdgeToEdgeCommonMorphs.keys()
        commonEdgePairs.sort(key=lambda x: len(EdgeToEdgeCommonMorphs[x]), reverse=True)

        return (commonEdgePairs, EdgeToEdgeCommonMorphs)

    # ------------------------------------------------------------------------------------------#
    # ------------------------------------------------------------------------------------------#
    #			Parsing
    # ------------------------------------------------------------------------------------------#
    # ------------------------------------------------------------------------------------------#
    # -----------------------------------------------------------------------------#
    # -----------------------------------------------------------#
    def parseWords(self, wordlist, outfile):
        # -----------------------------------------------------------------------------#
        self.WordParses = dict()
        index = 1
        wordlist.sort()
        for word in wordlist:
            if index % 1000 == 0:
                print
                index
            index += 1
            self.WordParses[word] = self.parseWord(word)
            print >> outfile, word
            if self.WordParses[word]:
                for parsechain in self.WordParses[word]:
                    parsechain.Print(outfile)
            print >> outfile

            # -----------------------------------------------------------------------------#

    def lparse(self, CompletedParses, IncompleteParses):
        # -----------------------------------------------------------------------------#
        currentParseChain = IncompleteParses.pop()
        # print "------------------"
        # print "length of current parsechain",  len(currentParseChain.my_chain)
        currentParseChunk = currentParseChain.my_chain[-1]
        # print "morph: ", currentParseChunk.morph, "remaining:",  currentParseChunk.remainingString
        currentParseToState = currentParseChunk.toState
        outgoingedges = currentParseToState.getOutgoingEdges()
        currentRemainingString = currentParseChunk.remainingString

        # print "current remaining string: ", currentRemainingString
        # print "Current parse To-state", currentParseChunk.toState.index
        for edge in outgoingedges:
            for label in edge.labels:
                if label == "NULL" and len(
                        currentParseChunk.remainingString) == 0 and edge.toState.acceptingStateFlag == True:
                    CopyOfCurrentParseChain = ParseChain()
                    CopyOfCurrentParseChain.Copy(currentParseChain)
                    newParseChunk = parseChunk(label, "", edge)
                    CopyOfCurrentParseChain.Append(newParseChunk)
                    CompletedParses.append(CopyOfCurrentParseChain)
                    # print "Completion, apparently, with a final NULL."
                    break  # break in label's for

                labellength = len(label)
                if currentRemainingString[:labellength] == label:
                    CopyOfCurrentParseChain = ParseChain()
                    CopyOfCurrentParseChain.Copy(currentParseChain)
                    if labellength == len(currentRemainingString) and edge.toState.acceptingStateFlag == True:
                        newParseChunk = parseChunk(label, "", edge)
                        CopyOfCurrentParseChain.Append(newParseChunk)
                        CompletedParses.append(CopyOfCurrentParseChain)
                    # print "1366 Completed parse with a real affix."
                    # print CopyOfCurrentParseChain.Display()
                    else:
                        # print "Good edge found, its to state is", edge.toState.index
                        newRemainingString = currentRemainingString[labellength:]
                        newParseChunk = parseChunk(label, newRemainingString, edge)
                        CopyOfCurrentParseChain.Append(newParseChunk)
                        IncompleteParses.append(CopyOfCurrentParseChain)
                        # print "Partial match found ", label
                        # for parsechain in IncompleteParses:
                        #	print "1377", "lenth of IncompletePrses", len(IncompleteParses), parsechain.Display()

        return (CompletedParses, IncompleteParses)

    # -----------------------------------------------------------------------------#
    def parseWord(self, word):
        # -----------------------------------------------------------------------------#
        CompletedParses = list()
        IncompleteParses = list()
        initialParseChain = ParseChain()
        startingParseChunk = parseChunk("", word)
        startingParseChunk.toState = self.startState

        # print "\nBegin parse of this word:", word

        initialParseChain.Append(startingParseChunk)
        IncompleteParses.append(initialParseChain)

        while len(IncompleteParses) > 0:
            CompletedParses, IncompleteParses = self.lparse(CompletedParses, IncompleteParses)
        # print "1403: incompleted parses now:", len(IncompleteParses), "completed parses", len(CompletedParses)
        if len(CompletedParses) == 0:
            # print "No parse found.-------------------------------------------------------------------------------------------"
            return None
        # for parsechain in CompletedParses:
        # print "in parseword:", parsechain.Display()

        # print "completing parse of this word -------------------------------------------------------------------------------------"
        return CompletedParses
