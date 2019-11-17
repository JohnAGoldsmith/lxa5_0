#  This script takes a wordlist as input, and a specific signature is hard coded (about 7 lines down from here). 
#  It determines all of the stems that match this signature perfectly, and then it seeks stems that match it imperfectly.
#  It can output the data in a format readable by R for color-coded display of words against this signature.


import string
import makelatextable
from collections import defaultdict
Signature1 = 'ing.ed.s.NULL'
Signature2 = 'ting.ted.s.NULL'
def makesortedstring(string):
	letters=list(string)
	letters.sort()
	return letters
## -------------------- 

	
	

def Difference1(string1, string2, maxdiff):
	
	minimalcommonprefix = 3	 
	if string1==string2:
		return 0
	length1 = len(string1)
	length2 = len(string2)
	if length1 - length2 > maxdiff or length2 - length1 > maxdiff:
		return 99
 	commonprefixlength = 0
	for i in range(1, length1+1):
		if i > length2:
			break
		if string1[0:i] == string2[0:i]:
			commonprefixlength = i
		else:
			break
	
	difference = length1 + length2 - 2*commonprefixlength
	return difference

def stringdiff(instring1, instring2, positive, negative):
	 
	if instring1 == 'NULL':
		instring1 = ''
	if instring2 == 'NULL':
		instring2 = ''
	if (False):
		string1 = makesortedstring(instring1)	 
		string2 = makesortedstring(instring2)	 
	else:
		string1 = list(instring1)
		string2 = list(instring2)
	i = 0
	j=0 
	del positive[:]
	del negative[:]
	while (1):
		if ( i < len(string1) and j < len(string2) ):
			if (string1[i]==string2[j]):
				i=i+1
				j=j+1			 
			elif (string1[i]<string2[j]):
				positive.append(string1[i])
				i=i+1			 
			else:
				negative.append(string2[j])
				j=j+1			 
		elif (i>=len(string1)):
				for k2 in range (j,len(string2)):
					negative.append(string2[k2])
					 
				break;
		elif (j>=len(string2)):
				 
				for k1 in range(i,len(string1)):
					positive.append(string1[k1])
					 
				break;
	#print 'positive', positive, 'negative', negative

def DifferenceOfDifference ( (X1, X2), (Y1, Y2)):
	x1 = list(X1)
	x2 = list(X2)
	y1 = list(Y1)
	y2 = list(Y2)
	r1 = []
	r2 = []
	x1.extend(y2)	#add y2 to x1
	del y2[:]
	x1.sort()

	x2.extend(y1)
	del y1[:]
	x2.sort()

	while len(x1) > 0:   #   remove anything in y1 from x1		 
		if len(x2)==0:
			r1.extend(x1)
			del x1[:]
			break
		else:
			if x1[0]<x2[0]:
				r1.append (x1.pop(0))			
			elif x1[0] == x2[0]:
				x1.pop(0)
				x2.pop(0)
			else:	
				r2.append(x2.pop(0)) 
	if len(x2) >0:
		r2.extend(x2)
		del x2[:]
	
	return (r1, r2)





class intrasignaturetable:
	def setsignature(self,sig):
		self.affixes= sig.split('.')
		for affix in self.affixes:
			if affix=='NULL':
				affix = ''
		self.differences={}
		positive=[]
		negative=[]

		for index1 in range (len(self.affixes)):
			for index2 in range (len(self.affixes)):
				affix1 = self.affixes[index1]
				affix2 = self.affixes[index2]
				stringdiff(affix1, affix2, positive, negative)
				positivelabel=''.join(positive)
				negativelabel=''.join(negative)
				self.differences[(index1,index2)] = (positivelabel, negativelabel)
	def display(self):
		positive=[]
		negative=[]
		print 'making table'
		print '\t',
		for affix in self.affixes:
			print affix, '\t',
		print
 
		for index1 in range(len(self.affixes)):
			affix1 = self.affixes[index1]
			print affix1, ':','\t',
			for index2 in range(len(self.affixes)): 
				affix2 = self.affixes[index2]
				print self.differences[(index1, index2)][0],':',self.differences[(index1, index2)][1],
			print


	def displaytofile(self, outfile):
		positive=[]
		negative=[]
		print >>outfile, '      ',
		for affix in self.affixes:
			print >>outfile, '%18s' %affix,
		print >>outfile
 
		for index1 in range(len(self.affixes)):
			print >>outfile,'%10s' %self.affixes[index1], 
			for index2 in range(len(self.affixes)): 
				print >>outfile, '%12s %-6s' %(self.differences[(index1, index2)][0],self.differences[(index1, index2)][1]) ,
			print >>outfile
	def minus(self, other):
		for index1 in range(0, len(self.affixes)):
			for index2 in range(0, len(self.affixes)):
				thispiece1 =self.affixes[index1]
				thispiece2 =self.affixes[index2]
				otherpiece1=other.affixes[index1]
				otherpiece2=other.affixes[index2]
 
				(thispositive, thisnegative)  =  self.differences[(index1, index2)]				 
				(otherpositive, othernegative)= other.differences[(index1, index2)]	
				self.differences[(index1,index2)] =  DifferenceOfDifference( (thispositive, thisnegative), (otherpositive, othernegative))
					

 
outfilename = "sigdiff.txt"
outfile = open(outfilename, "w")
 
basictableau1=intrasignaturetable()
basictableau1.setsignature(Signature1)
basictableau1.displaytofile(outfile)

basictableau2=intrasignaturetable()
basictableau2.setsignature(Signature2)
basictableau2.displaytofile(outfile)

  
basictableau2.minus(basictableau1)
basictableau2.displaytofile(outfile)
print >>outfile, '\n\n'
 
 
 
 
