import string

def read_dx1(infile, Lexicon, BreakAtHyphensFlag, wordcountlimit):
            punctuation = "$(),;.:-?%&\\1234567890\"\/'[]"
            for line in infile:
            #for line in filelines:

                pieces = line.split()
                word = pieces[0]
                #if word.endswith("NULL=ly"):
                #    print 11, "NULL-ly"
                if '#' in word:
                    #print "We cannot accept a word with # in it.", word
                    continue
                if '=' in word:
                    #print "We cannot accept a word with = in it.", word
                    continue
                if len(word) == 1 and word in punctuation:
                    #print ("We cannot accept a one-character word consisting of punctuation:", word)
                    continue
                if len(pieces) > 1:
                    count = int(pieces[1])
                else:
                    count = 1
                #word.translate(None, string.punctuation)
                if (BreakAtHyphensFlag and '-' in word):
                    words = word.split('-')
                    for word in words:
                        #if word == "&":
                        #    print 24
                        while word and word[-1] in punctuation:
                            word = word[:-1]
                        while word and word[0] in punctuation:
                            word = word[1:]
                        if word not in Lexicon.Word_counts_dict:
                            Lexicon.WordBiographies[word] = list()
                            Lexicon.Word_counts_dict[word] = 0
                        Lexicon.Word_counts_dict[word] += count
                        if len(Lexicon.Word_counts_dict) >= wordcountlimit:
                            break
                else:
                    while word and word[-1] in punctuation:
                            word = word[:-1]
                    while word and word[0] in punctuation:
                            word = word[1:]
                    if word not in Lexicon.Word_counts_dict:
                        Lexicon.WordBiographies[word] = list()
                        Lexicon.Word_counts_dict[word] = 0
                        Lexicon.Word_list_forward_sort.append(word)
                        Lexicon.Word_list_reverse_sort.append(word)
                    Lexicon.Word_counts_dict[word] = count
                    if len(Lexicon.Word_counts_dict) >= wordcountlimit:
                        break
                Lexicon.WordBiographies[word] = list()

            Lexicon.sort_words()

def read_corpus(infile, Lexicon, BreakAtHyphensFlag, wordcountlimit):
            punctuation = "$(),;.:-?\\1234567890[]\"\'"
            tokencount = 0
            typecount = 0
            for line in infile:
                if tokencount - wordcountlimit > 0:
                    break
                for token in line.split():
                    exclude = set(string.punctuation)
                    word = "".join(ch for ch in token if ch not in exclude)
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

def read_data(datatype,infile, Lexicon, BreakAtHyphensFlag, wordcountlimit):
        if datatype == "DX1":
            read_dx1(infile, Lexicon, BreakAtHyphensFlag, wordcountlimit)
        else:
            read_corpus(infile, Lexicon, BreakAtHyphensFlag, wordcountlimit)
        infile.close()