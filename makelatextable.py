		

#--------------------------------------------------------------------##
#		Start, end latex doc
#--------------------------------------------------------------------##
def StartLatexDoc(outfile):
	header0 = "\documentclass[10pt]{article} \n\\usepackage{booktabs} \n\\usepackage{geometry} \n\\geometry{verbose,letterpaper,lmargin=0.5in,rmargin=0.5in,tmargin=1in,bmargin=1in} \n\\begin{document}  \n" 
	print >>outfile, header0

def EndLatexDoc(outfile):
	footer = "\\end{document}"
	print >>outfile, footer
	outfile.close()
	
#--------------------------------------------------------------------##
#		Make latex table
#--------------------------------------------------------------------##
def MakeLatexFile(outfile, headers, datalines):
	"""
	When there are datalines that begin with a #, contain a single character
	as their second item, then that second item will be replaced
	by the third. This allows an easy conversion to latex specifications.
	"""
	tablelines = list()
	printlines = list()
	longestitem = 1
	numberofcolumns = len(headers)+1
	translations = dict()
	translations["NULL"] = "\\emptyset"
	header1 = "\\begin{centering}\n"
	header2 = "\\begin{tabular}{" 
	header3 = "\\toprule "
	footer1 = "\\end{tabular}"
	footer2 = "\\end{centering}\n"
	
	for line in datalines:
		if line[0] == "#":
			if len(line) == 3 and len(line[1]) == 1:
				translations[line[1]] = line[2]
		else:
			linelist = list()
			if len(line) > numberofcolumns:
				numberofcolumns = len(line)
			for item in line:
				for a in item:
					if a in translations:
						item.replace(a,translations[a])
				if len(item) > longestitem:
					longestitem = len(item)
				linelist.append(item)
			tablelines.append(linelist)
		print linelist
#	print file=outfile,  header1
#	print (header2,'l'*numberofcolumns, "}",  header3,file=outfile)
	print >>outfile,  header1
	print >>outfile, header2,'l'*numberofcolumns, "}",  header3 



	# Calculate length of items in  the top header line:
	redone_words = list()
	thisline = list()
	thisline.append("")
	for word in headers:
		for a in word:
			if a in translations:
				word.replace(a,translations[a])
			if len(word) > longestitem:
				longestitem = len(word)
		redone_words.append(word)
		thisline.append(word)

	# if an item in a line is of the form "a:b", then it will generate \frac{a}{b} 
	for m in range(len(tablelines)):	
		thisline = list()
		line = tablelines[m]
		#print word in first column:
		thisline.append(redone_words[m]) 
		for n in range(len(line)): 
			field = line[n]
			if field == "@":
				thisline.append("")	
			elif len(field.split(":")) == 2:
				fraction = field.split(":")
				field = "$\\frac{" + fraction[0] + "}{" + fraction[1] + "}$"
				thisline.append(field)
			else:			
				thisline.append(field)
			if len(field) > longestitem:
				longestiem = len(field)
		printlines.append(thisline)
 
 	for wordno in range(len(redone_words)):
		thisword = redone_words[wordno]
		print >>outfile, " & " + thisword + " "*(longestitem - len(thisword)) ,
#	print ("\\\\ \\midrule",file=outfile)
	print >>outfile, "\\\\ \\midrule"
				
	for line in printlines:
		for no in range(len(line)):
			item = line[no]
			print >>outfile, item, 
			if no < len(line) -1:
				print >>outfile, "&",
#		print (  "\\\\",file=outfile)
		print >>outfile, "\\\\"
			
#	print ("\\bottomrule", "\n",file=outfile)
#	print ( footer1,file=outfile)
#	print ( footer2,file=outfile)
#	print ("\\vspace{.4in}",file=outfile)
	print >>outfile,  "\\bottomrule", "\n"
	print >>outfile, footer1
	print >>outfile, footer2
	print >>outfile, "\\vspace{.4in}" 

	

 
# ----------------------------------------------------------------------------------------------------------------------------#
def print_signatures_to_latex(outfile, 
                           signatures,
                           affix_side):
    header1 = "\\documentclass[10pt]{article}" 
    header2 = "\\usepackage{booktabs}" 
    header3 = "\\usepackage{geometry}" 
    header4 = "\\usepackage{longtable}" 
    header5 = "\\geometry{verbose,letterpaper,lmargin=0.5in,rmargin=0.5in,tmargin=1in,bmargin=1in}"
    header6 = "\\begin{document} "
    starttab = "\\begin{longtable}{lllllllllll}"
    endtab = "\\end{longtable}"

    print "   Printing signature file in latex."
    running_sum = 0.0
#    print (header1, file = outfile)
#    print (header2, file = outfile)
#    print (header3, file = outfile)
#    print (header4, file = outfile)            
#    print (header5, file = outfile)
#    print ("\n" + header6, file = outfile)
#    print ("\n" + starttab, file = outfile)
#    print (" & Signature & Stem count & Robustness & Proportion of robustness\\\\ \\toprule", file = outfile)
    print >>outfile, header1
    print >>outfile, header2
    print >>outfile, header3
    print >>outfile, header4            
    print >>outfile, header5
    print >>outfile, "\n" + header6
    print >>outfile, "\n" + starttab
    print >>outfile, " & Signature & Stem count & Robustness & Proportion of robustness\\\\ \\toprule"
 
    total_robustness = 0.0
    for sig in signatures:
    	total_robustness += sig.robustness
    colwidth = 20
    sigs = sorted(signatures, key = lambda x: x.robustness, reverse=True)
    count = 1
    for sig in sigs:
    	# ADD EXAMPLE STEM
        running_sum += sig.robustness
        robustness_proportion = float(sig.robustness) / total_robustness
        running_sum_proportion = running_sum / total_robustness
#        print ( count,  sig, " "*(colwidth-len(sig)), "&",  stemcount, "&",  robustness, "&", "{0:2.3f}".format(robustness_proportion), "\\\\", file=outfile)
        print >>outfile,  count,  sig, " "*(colwidth-len(sig)), "&",  stemcount, "&",  robustness, "&", "{0:2.3f}".format(robustness_proportion), "\\\\"
        count += 1
#    print (endtab,file=outfile)
    print >>outfeil, endtab
    number_of_stems_per_line = 6
    stemlist = []
#    print ("\n", file = outfile)
    print >>outfile, "\n"
    for sig in sigs:
#        print (starttab, file = outfile)
#        print (sig, "\\\\", file = outfile)
        print >>outfile, starttab 
        print >>outfile, sig, "\\\\" 
        n = 0
        stemlist = sig.get_stems()
        numberofstems = len(stemlist)
        for stem in stemlist:
            n += 1
#            print (stem, " & ", end = " ",file = outfile)
            print >>outfile, stem, " & ", 
            if n % number_of_stems_per_line == 0:
#                print ( "\\\\", file=outfile)
                print >>outfile, "\\\\"
#        print (endtab, "\n\n\n\n",file=outfile)
#        print (starttab, file=outfile)
        print >>outfile, endtab, "\n\n\n\n"
        print >>outfile, starttab

        numberofcolumns = 4
        colno = 0
        #stemlist.sort(key = lambda x : Lexicon.StemCorpusCounts[x], reverse = True)
        #ARIS: DO WE HAVE STEM COUNTS HERE?
        for stem in stemlist:
            print >> this_file, stem, "&",  stem.counts, "&",
            #print (stem, "&", file=outfile)
            colno += 1
            if colno % numberofcolumns == 0:
                print >> this_file, "\\\\"
#        print (endtab, file = outfile)
#        print ("\n",file = outfile)    
        print >>outfile, endtab
        print >>outfile,"\n"   
#    print ("\\end{document}", file = outfile)	
    print >>outfile, "\\end{document}"
    outfile.close()

