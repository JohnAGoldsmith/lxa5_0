		

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
def MakeLatexFile(outfile, wordlist, datalines):
 #when there are datalines that begin with a #, contain a single character as their second item, then that second item will be replaced
 # by the third. This allows an easy conversion to latex specifications.
	tablelines = list()
	printlines = list()
	longestitem = 1
	numberofcolumns = len(wordlist)+1
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

	print >>outfile,  header1
	print >>outfile, header2,'l'*numberofcolumns, "}",  header3

	print "longest item", longestitem

	# Calculate length of items in  the top header line:
	redone_words = list()
	thisline = list()
	thisline.append("")
	for word in wordlist:
		for a in word:
			if a in translations:
				word.replace(a,translations[a])
			if len(word) > longestitem:
				longestitem = len(word)
		redone_words.append(word)
		thisline.append(word)
	print "longest word", longestitem
	#printlines.append(thisline)
	
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
#		if wordno < len(redone_words) - 1:
#			print >>outfile, "&",
	print >>outfile, "\\\\ \\midrule"
				
	for line in printlines:
		for no in range(len(line)):
			item = line[no]
			print >>outfile, item, 
			if no < len(line) -1:
				print >>outfile, "&",
		print >>outfile,  "\\\\"
			
			
	print >>outfile, "\\bottomrule", "\n"
	print >>outfile, footer1
	print >>outfile, footer2
	print >>outfile, "\\vspace{.4in}"

	
