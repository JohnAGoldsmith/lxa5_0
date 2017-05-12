def find_first_and_last_string_in_list(target, wordlist, margin=0):
    # This assumes that wordlist is sorted alphabetically. If margin = 0, then the first word found is the first word that equals or contains target. If margin > 0, then
    # the target chosen for finding the first_word is the target minus its last m characters, where m is the margin.
    shortened_target = target[:-2]
    short_target_length = len(shortened_target)
    print "7", target
    for wordno in range(len(wordlist)):
        word = wordlist[wordno]
        print "10", word
        if word < shortened_target:
            continue
            print "12 skipping", word
        # print "11", target, shortened_target, word
        firstword = word
    firstwordnumber = wordno
    print "14 first word", target, shortened_target, firstword
    for wordno in range(firstwordnumber + 1, len(wordlist)):
        word = wordlist[wordno]
        word = word[:-2]
        if shortened_target < word:
            print "Including ", word
        print "19 last word", word
        break
    return (firstword, lastword)


def filter_by_suffix(suffix, wordlist):
    # this function returns all the words in wordlist that end in the suffix
    newwordlist = list()
    suffixlength = len(suffix)
    for word in wordlist:
        if suffix == word[-1 * suffixlength:]:
            stem = word[:len(word) - suffixlength]
            newwordlist.append((stem, word))
            # print "30", stem, suffix, word
        # print "31", newwordlist
    return newwordlist
