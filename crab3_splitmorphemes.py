from class_lexicon import *
from class_morphemetosignature import *

# ----------------------------------------------------------------------------------------------------------------------------#
def	Words_with_multiple_analyses_high_entropy (Lexicon, affix_type):
# ----------------------------------------------------------------------------------------------------------------------------
        outfile = open("6_Biparses.txt", "w") 
        outfileTex = open ("6_Biparses.tex", "w")

        header1 = "\\documentclass[10pt]{article}" 
        header2 = "\\usepackage{booktabs}" 
        header3 = "\\usepackage{geometry}" 
        header4 = "\\usepackage{longtable}" 
        header5 = "\\geometry{verbose,letterpaper,lmargin=0.5in,rmargin=0.5in,tmargin=1in,bmargin=1in}"
        header6 = "\\begin{document} "
        starttab = "\\begin{longtable}{lllllllllll}"
        endtab = "\\end{longtable}"
        enddoc = "\\end{document}"

        print >>outfileTex, header1
        print >>outfileTex, header2
        print >>outfileTex, header3
        print >>outfileTex, header4
        print >>outfileTex, header5
        print >>outfileTex
        print >>outfileTex, header6
        print >>outfileTex
        print >>outfileTex, starttab
        print >>outfileTex,  " diff & stem 1  & sig 1 & stem 2 & sig 2 \\\\ \\toprule"

        formatstring = "{0:10s} {1:18s}  {2:30s} {3:18s} {4:30s}"
        formatstringTex = "{0:10s} & {1:18s}  &  {2:30s}  & {3:18s}  & {4:30s} \\\\"
	words = Lexicon.Word_list_forward_sort
	sigpaires = list()
        Biparses = dict()
	for word in Lexicon.WordToSig:
            if (Lexicon.WordToSig[word]) > 1:
                sigpairs = sorted(Lexicon.WordToSig[word], key = lambda x: len(x[0]) )   #sort by length of stem 
	        for i in range(len(sigpairs)):
                     stem1, sig1 = sigpairs[i]
                     for j in range(i+1,len(sigpairs)):
                         stem2, sig2 = sigpairs[j]
                         biparse_string = stem1 + " "+ sig1 + " " + stem2 + " " + sig2
                         if biparse_string not in Biparses:
                             biparse = Biparse(affix_type, stem1,  stem2, sig1, sig2)
			     Biparses[biparse_string] = biparse 
        Biparses_list = Biparses.values()                        
	Biparses_list.sort(key = lambda x: x.m_sigstring1)
	Biparses_list.sort(key = lambda x: x.m_sigstring2)
	Biparses_list.sort(key = lambda x: x.m_difference)


        if False:  
		for x in Biparses_list:
			print >>outfile, formatstring.format(x.m_difference, x.m_stem1,  x.m_sigstring1,x.m_stem2, x.m_sigstring2)
		        print >>outfileTex, formatstringTex.format(x.m_difference, x.m_stem1, x.m_sigstring1,x.m_stem2,  x.m_sigstring2)
		print >>outfileTex, endtab
		print >>outfileTex, enddoc

        Biparses2 = dict()
	for biparse in Biparses_list:
            key = (biparse.m_difference, biparse.m_sigstring1, biparse.m_sigstring2)
            if key not in Biparses2:
                Biparses2[key] = list()
            Biparses2[key].append((biparse.m_stem1, biparse.m_stem2))
        for k,v in Biparses2.items():
               v.sort()     
	Biparses2_list = sorted(Biparses2.keys())

        MorphemesToSignatures = list() 
	for k,v in Biparses2.items():
            morph_to_sig = MorphemeToSignature(k[0], k[1], k[2])
            for pair in v:
                morph_to_sig.add_stem(pair[0])
            MorphemesToSignatures.append(morph_to_sig)
 	
        MorphemesToSignatures.sort(key  = lambda x: x.m_diff ) 
        MorphemesToSignatures.sort(key  = lambda x: len(x.m_stemlist), reverse = True) 
        for x in MorphemesToSignatures :
            print >>outfile, x.make_rule(), " " , x.display_old()
        print >>outfile, "\n"
	
	# the real work! For cutting affixes into two parts
        ENTROPY_THRESHOLD = 1.0
        for i in range(len(MorphemesToSignatures)):
    	    morph_to_sig = MorphemesToSignatures[i]
            cutting_signature_string = morph_to_sig.m_sig2
            cutting_signature = Lexicon.Signatures[cutting_signature_string]
            if cutting_signature.get_stability_entropy() > ENTROPY_THRESHOLD:
                morph_to_sig.simplify1(outfile, Lexicon)

	print >>outfile, "\n\n" + "=="*50 + "\n\n"
 
        outfile.close()
        outfileTex.close()
# ----------------------------------------------------------------------------------------------------------------------------#
def	Words_with_multiple_analyses_low_entropy (Lexicon, affix_type):
# ----------------------------------------------------------------------------------------------------------------------------
        outfile = open("6_Biparses-2.txt", "w") 
        outfileTex = open ("6_Biparses-2.tex", "w")

        header1 = "\\documentclass[10pt]{article}" 
        header2 = "\\usepackage{booktabs}" 
        header3 = "\\usepackage{geometry}" 
        header4 = "\\usepackage{longtable}" 
        header5 = "\\geometry{verbose,letterpaper,lmargin=0.5in,rmargin=0.5in,tmargin=1in,bmargin=1in}"
        header6 = "\\begin{document} "
        starttab = "\\begin{longtable}{lllllllllll}"
        endtab = "\\end{longtable}"
        enddoc = "\\end{document}"

        print >>outfileTex, header1
        print >>outfileTex, header2
        print >>outfileTex, header3
        print >>outfileTex, header4
        print >>outfileTex, header5
        print >>outfileTex
        print >>outfileTex, header6
        print >>outfileTex
        print >>outfileTex, starttab
        print >>outfileTex,  " diff & stem 1  & sig 1 & stem 2 & sig 2 \\\\ \\toprule"

        formatstring = "{0:10s} {1:18s}  {2:30s} {3:18s} {4:30s}"
        formatstringTex = "{0:10s} & {1:18s}  &  {2:30s}  & {3:18s}  & {4:30s} \\\\"
	words = Lexicon.Word_list_forward_sort
	sigpairs = list()
        Biparses = dict()
	for word in Lexicon.WordToSig:
            if word[0] == ":":
                continue
            if (Lexicon.WordToSig[word]) > 1:
                sigpairs = sorted(Lexicon.WordToSig[word], key = lambda x: len(x[0]) )   #sort by length of stem 
	        for i in range(len(sigpairs)):
                     stem1, sig1 = sigpairs[i]                     
                     for j in range(i+1,len(sigpairs)):
                         stem2, sig2 = sigpairs[j]
                         biparse_string = stem1 + " "+ sig1 + " " + stem2 + " " + sig2
                         if biparse_string not in Biparses:
                             biparse = Biparse(affix_type, stem1,  stem2, sig1, sig2)
			     Biparses[biparse_string] = biparse 
        Biparses_list = Biparses.values()                        
	Biparses_list.sort(key = lambda x: x.m_sigstring1)
	Biparses_list.sort(key = lambda x: x.m_sigstring2)
	Biparses_list.sort(key = lambda x: x.m_difference)

        print >>outfile, "\n", 155

        if True:  
		for x in Biparses_list:
			print >>outfile, 158, formatstring.format(x.m_difference, x.m_stem1,  x.m_sigstring1,x.m_stem2, x.m_sigstring2)
		        print >>outfileTex, formatstringTex.format(x.m_difference, x.m_stem1, x.m_sigstring1,x.m_stem2,  x.m_sigstring2)
		print >>outfileTex, endtab
		print >>outfileTex, enddoc

        Biparses2 = dict()
	for biparse in Biparses_list:
            key = (biparse.m_difference, biparse.m_sigstring1, biparse.m_sigstring2)
            if key not in Biparses2:
                Biparses2[key] = list()
            Biparses2[key].append((biparse.m_stem1, biparse.m_stem2))
        for k,v in Biparses2.items():
               v.sort()     
	Biparses2_list = sorted(Biparses2.keys())

        MorphemesToSignatures = list() 
	for k,v in Biparses2.items():
            morph_to_sig = MorphemeToSignature(k[0], k[1], k[2])
            for pair in v:
                morph_to_sig.add_stem(pair[0])
            MorphemesToSignatures.append(morph_to_sig)

        print >>outfile, "\n"

        MorphemesToSignatures.sort(key  = lambda x: x.m_sig2 )  	
        MorphemesToSignatures.sort(key  = lambda x: x.m_diff ) 
        for x in MorphemesToSignatures :
            print >>outfile, 186, x.display()


        print >>outfile, "\n"




  
        print >>outfile, "========\n, 189"
        ENTROPY_THRESHOLD = 1.0
        # for pairs of closely related signatures
        for i in range(len(MorphemesToSignatures)):
            if i == len(MorphemesToSignatures): 
                break
    	    morph_to_sig = MorphemesToSignatures[i]
            cutting_signature_string = morph_to_sig.m_sig2
            cutting_signature = Lexicon.Signatures[cutting_signature_string]
            if cutting_signature.get_stability_entropy() <= ENTROPY_THRESHOLD:
                if len(morph_to_sig.m_diff) > 1:
                    print >>outfile, 200, morph_to_sig.m_diff, morph_to_sig.display_old()
 
        outfile.close()
        outfileTex.close()

