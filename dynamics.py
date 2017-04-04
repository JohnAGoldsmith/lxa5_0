def dynamics( lex, corpus):
    for word in corpus:
        siglist_for_word = lex.WordToSig[word]
        for (stem,sig) in siglist_for_word:
            print stem, sig

