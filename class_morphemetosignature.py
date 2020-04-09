
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
        diff = lexicon.get_new_name(raw_diff)  #adds to affix a unique integer
        old_sig1 = self.m_sig1
        old_sig2 = self.m_sig2
        new_sig1 = self.m_new_sig1
        new_sig2 = self.m_new_sig2
        print >>outfile, "\n", 683, self.display_rule(), "From:", self.display_old()
	# fix long-stem signature, new_sig2:
        for affix in new_sig2.split("="):
            lexicon.Parses[(diff,affix)] = 1
            print >>outfile, " adding new parses" , diff, affix

        # remove long stems parses from the old_sig2
	for stem in self.m_stemlist:
            stem += raw_diff
            for affix in old_sig2.split("="):
                if (stem,affix) in lexicon.Parses:
                    print >>outfile, 65, "Removing (", stem, affix, ")"
                    del lexicon.Parses[(stem,affix)]
                else:
                    print >>outfile, 68, "Can't remove ", stem, affix 
             

	# fix short-stem signature, new_sig1
        for stem in self.m_stemlist:
            for affix in old_sig1.split("="):
                if affix.startswith(raw_diff):
                    if affix == raw_diff:
                        continue
                    if (stem,affix)  in lexicon.Parses:
		            print >>outfile, 77, "Removing (", stem, "," , affix, ")"     
			    del lexicon.Parses[(stem,affix)]
		    else:
                            print >>outfile, "Couldn't find  ", stem, affix, "must have already been deleted."
	# fix short-stem signature


