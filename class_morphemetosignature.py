
class MorphemeToSignature:
    """
    An object consisting of a morpheme that point to
    a signature, with its corresponding stems,
    which can be followed by the morpheme.
    """
    def __init__(self, diff="", sig1="", sig2=""):
        self.m_diff = diff
        self.m_sig1 = sig1
        self.m_sig2 = sig2
        self.m_stemlist = list()
        self.m_new_sig1 = list()
        self.m_new_sig2 = list()
    def add_stem(self, stem):
        self.m_stemlist.append(stem)
    def display(self):
        format_string = "{0:5s} {1:20s} {2:20s}"
        return format_string.format(self.m_diff, self.m_sig1, self.m_sig2) + " ".join(self.m_stemlist)
    def display_old(self):
        this_string = "{0:28s} {1:28s}".format(self.m_sig1,self.m_sig2) 
        return this_string  + "  "+ " ".join(self.m_stemlist)
    def display_rule(self):
        format_string = "{0:28s} ==> {1:28s}"  
        newstem = "[" + self.m_new_sig1 + "]_" + self.m_diff
        return format_string.format(newstem , self.m_new_sig2) 
    def make_rule(self):
        diff = self.m_diff
        new_sig1 = set()                  # with shorter stem
        new_sig2 = set()                  # shorter stem + diff, now just for diff
        new_sig1.add (diff)
        for morph in self.m_sig1.split("="):
               if morph == diff:
                   new_sig2.add ( "NULL" )  
               elif morph.startswith( diff ):
                   new_sig2.add( morph[len(diff):] )
               else:
                   new_sig1.add( morph )     
        for morph in self.m_sig2.split("="):
            new_sig2.add(morph)
        new_sig1 = list(new_sig1)
        new_sig1.sort()
	new_sig2 = list(new_sig2)
        new_sig2.sort()

        self.m_new_sig1 = "=".join(new_sig1)
        self.m_new_sig2 = "=".join(new_sig2)

        return self.display_rule()

    def simplify1(self, outfile, lexicon):
        raw_diff = self.m_diff
        diff = lexicon.get_new_name(raw_diff)  #adds to affix a unique integer; and prefixes a ":" to mark as an affix
        old_sig1 = self.m_sig1
        old_sig2 = self.m_sig2
        new_sig1 = self.m_new_sig1
        new_sig2 = self.m_new_sig2
        print >>outfile, "\n", 683, self.display_rule(), "From:", self.display_old()

        for affix in new_sig2.split("="):
            lexicon.Parses[(diff,affix)] = 1
            print >>outfile, 62, " adding new parses" , diff, affix

        # signature with longer stems (including diff)
	for stem in self.m_stemlist:
            stem1 =  stem + raw_diff
            for affix in old_sig2.split("="):
                if affix == "NULL":
                    word = stem1
                else:
                    word = stem1 + affix
                if word == "abductee":
                    print >>outfile, 73, word, "stem1", stem1, "affix", affix
                if (stem1,affix) in lexicon.Parses:
                    print >>outfile, 65, "Removing (", stem1, affix, ")"
                    lexicon.WordBiographies[word].append ("crab3 remove: " + stem1 + "/" + affix) 
                    del lexicon.Parses[(stem1,affix)]
                else:
                    print >>outfile, 68, "Can't remove ", stem1, affix 
                    lexicon.WordBiographies[word].append ("crab 3 couldn't remove (" + stem1 + " " + affix +  ")")
                if word in lexicon.WordBiographies:
                    lexicon.WordBiographies[word].append("crab3, now:   " +  stem + " " + diff + " " + affix + " -> " + stem + " "+ raw_diff + " " + affix)
	# signature with shorter stems             
        for stem in self.m_stemlist:
            lexicon.Parses[(stem,diff)] = 1
            print >> outfile, "85 add parse:", stem, diff
            for affix in old_sig1.split("="):
                if affix.startswith(raw_diff):
                    word = stem + affix
                    new_affix = affix[len(raw_diff):]
                    if len(new_affix) == 0:
                        new_affix = "NULL"
                    if (stem,affix) in lexicon.Parses:
		            print >>outfile, 77, "Removing (", stem, "," , affix, ")"     
			    del lexicon.Parses[(stem,affix)]
                            lexicon.WordBiographies[word].append("crab3: remove: " + stem + "/" + affix)                            
		    else:
                            print >>outfile, "Couldn't find  ", stem, affix, "must have already been deleted."
                    #lexicon.Parses[()] = 1
