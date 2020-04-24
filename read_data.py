import string

def read_dx1(infile, Lexicon, BreakAtHyphensFlag, wordcountlimit):
            punctuation = "$(),;.:-?%&\\1234567890\"\/'[]"
            longest_word_length = 0
            for line in infile:
                pieces = line.split()
                word = pieces[0]
                if '#' in word:
                    continue
                if '=' in word:
                    continue
                if len(word) == 1 and word in punctuation:
                    continue
                if len(pieces) > 1:
                    count = int(pieces[1])
                else:
                    count = 1
                if (BreakAtHyphensFlag and '-' in word):
                    words = word.split('-')
                    for word in words:
                        while word and word[-1] in punctuation:
                            word = word[:-1]
                        while word and word[0] in punctuation:
                            word = word[1:]
                        if word not in Lexicon.Word_counts_dict:
                            Lexicon.WordBiographies[word] = list()
                            Lexicon.Word_counts_dict[word] = 0
                            Lexicon.WordBiographies[word].append("original")
                        Lexicon.Word_counts_dict[word] += count
                        if len(word) > longest_word_length:
                            longest_word_length = len(word)
                        if len(Lexicon.Word_counts_dict) >= wordcountlimit:
                            break
                else:
                    while word and word[-1] in punctuation:
                            word = word[:-1]
                    while word and word[0] in punctuation:
                            word = word[1:]
                    if word not in Lexicon.Word_counts_dict:
                        Lexicon.WordBiographies[word] = list()
                        Lexicon.WordBiographies[word].append("original")
                        Lexicon.Word_counts_dict[word] = 0
                        Lexicon.Word_list_forward_sort.append(word)
                        Lexicon.Word_list_reverse_sort.append(word)
                    Lexicon.Word_counts_dict[word] = count
                    if len(word) > longest_word_length:
                        longest_word_length = len(word)
                    if len(Lexicon.Word_counts_dict) >= wordcountlimit:
                        break
                if word not in Lexicon.WordBiographies:
                    Lexicon.WordBiographies[word] = list()
                    print 53
            Lexicon.LongestWordLength = longest_word_length
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
