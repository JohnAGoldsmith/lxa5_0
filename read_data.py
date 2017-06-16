
def read_data(datatype, filelines, Lexicon,BreakAtHyphensFlag,wordcountlimit):


        if datatype == "DX1":
            for line in filelines:
                pieces = line.split()
                word = pieces[0]
                if '#' in word:
                    print "We cannot accept a word with # in it.", word
                    continue
                if len(pieces) > 1:
                    count = int(pieces[1])
                else:
                    count = 1
                word = word.lower()
                if (BreakAtHyphensFlag and '-' in word):
                    words = word.split('-')
                    for word in words:
                        if word not in Lexicon.WordCounts:
                            Lexicon.WordBiographies[word] = list()
                            Lexicon.WordCounts[word] = 0
                        Lexicon.WordCounts[word] += count
                        if len(Lexicon.WordCounts) >= wordcountlimit:
                            break
                else:
                    if word not in Lexicon.WordCounts:
                        Lexicon.WordBiographies[word] = list()
                        Lexicon.WordCounts[word] = 0
                    Lexicon.WordCounts[word] = count
                    if len(Lexicon.WordCounts) >= wordcountlimit:
                        break

                Lexicon.WordList.AddWord(word)
                Lexicon.WordBiographies[word] = list()
        else:
            tokencount = 0
            typecount = 0
            for line in filelines:
                if tokencount - wordcountlimit > 0:
                    break
                for token in line.split():
                    if token[0] == '$' or token[0] == '(' or token[0] == ',' or token[0] == '-' or token[0] == '\\' or token[
                        0] == '(' or token[0] == '1' or token[0] == '2':
                        token = token[1:]
                    if len(token) == 0:
                        continue;
                    if token[-1] == '.' or token[-1] == '!' or token[-1] == ',' or token[-1] == ';' or token[-1] == ': ' or \
                                    token[-1] == '?' or token[-1] == ')' or token[-1] == ']':
                        token = token[:-1]
                    if len(token) == 0:
                        continue
		    token.lower()	
                    if token in Lexicon.WordCounts:
                        Lexicon.WordCounts[token] += 1
                        tokencount += 1
                    else:
                        Lexicon.WordBiographies[token] = list()
                        Lexicon.WordCounts[token] = 1
                        tokencount += 1
                        typecount += 1
                     
                    Lexicon.WordList.AddWord(token)
                    Lexicon.Corpus.append(token)
                    Lexicon.WordBiographies[token] = list()
