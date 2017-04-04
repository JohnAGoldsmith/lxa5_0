def dynamics( lex, corpus):
    Signatures = dict()
    StemToSig = dict()
    for word in corpus:
        siglist_for_word = lex.WordToSig[word]
        for (stem,sig) in siglist_for_word:
            affixlength = len(word) - len(stem)
            affix = word[-1 * affixlength:]
            print stem, affix,sig
            if stem in StemToSig:
                sig = StemToSig[stem]
                if affix in sig:
                    sig.StemToWordCount[sig][affix] += 1
                    sig.Stem[stem] +=  1
                else:
                    #move stem to a bigger sig
                    pass

            else:
                newsig = CSignature()




