# Created by John Goldsmith
# Modified by Lang Yu, 11:27 PM, Jan 31, 2017
# langyu at uchicago dot edu
import sys

wordcountlimit = 1000000
n = 0
words = {}
# language 	= "turkish"
# infolder 	= '../../data/' + language + '/'	
# size 		= 500 #french 153 10 english 14 46
# specificname 	= "turkish"
# infilename 	= infolder + specificname +  ".txt"

infilename = sys.argv[1]

mywords = dict()
punctuation = " 0123456789$/+.,;:?!()\"[]"
file = open(infilename)
for line in file:
    # print line
    if not line:
        break
    line = line[:-1]
    words = line.split()
    # print words
    for word in words:
        for c in punctuation:
            word = word.replace(c, "")
        if len(word) == 0:
            continue
        if word == "--" or word == "-" or word == "---" or word == "----":
            continue
        if len(word) == 0:
            continue
        if word in mywords:
            mywords[word] += 1
        else:
            mywords[word] = 1

top_words = [x for x in mywords.iteritems()]
top_words.sort(key=lambda x: x[1], reverse=True)

# print size
# truesize = size * 1000
# outfolder	= infolder
# outfilename 	= outfolder + specificname + "_" +  str(size) + "Kwords.txt"
outfilename = "./out.dx1"
outfile = open(outfilename, "w")

count = 0
for word in top_words:
    count += 1
    print >> outfile, word[0], word[1]
# if count > truesize:
#	break
outfile.close()
