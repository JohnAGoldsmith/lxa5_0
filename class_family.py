#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 10:53:02 2019

@author: john
"""
import operator
from signaturefunctions import list_to_string
from signaturefunctions import contains
from signaturefunctions import list_contains
from signaturefunctions import signature_string_to_signature_list
from signaturefunctions import NumberOfAffixesInSigString
from makelatextable import *

class family:
    def __init__(self, nucleus_sig_string):
        self.m_nucleus_string = nucleus_sig_string # is a singnature
        self.m_nucleus_list = signature_string_to_signature_list(nucleus_sig_string)
        self.m_children = list()  # list of signatures
        self.m_satellite_affixes = dict() # key is affix, value is list of signature_strings containing that affix
        self.m_affix_counts = dict()

    def add_signature(self, this_signature):
        sig_string = this_signature.get_affix_string()
        affix_list = list(this_signature.get_affix_list()) 
        if sig_string not in self.m_children:
            self.m_children.append(sig_string)
        for affix in self.m_nucleus_list:
            if affix not in affix_list:
                print "29  Error!", affix , "should be present but it is not."
        affix_list = [affix for affix in affix_list if affix not in self.m_nucleus_list  ]        
        for affix in affix_list:
            if affix not in self.m_satellite_affixes:
                self.m_satellite_affixes[affix] = list()
                self.m_affix_counts[affix] = 0
            self.m_satellite_affixes[affix].append(sig_string)                
            self.m_affix_counts[affix] += this_signature.get_stem_count()
    def print_family(self, this_file):
        print >>this_file, self.m_nucleus_string,  "Satellite affixes:\n"
        affix_list = sorted(self.m_satellite_affixes.keys())
        affix_list.sort(key = lambda affix: self.m_affix_counts[affix], reverse= True)
        for affix in affix_list:
            print >>this_file,"  ", affix, self.m_affix_counts[affix]
        print >>this_file
 
        self.m_children.sort(key = lambda x: NumberOfAffixesInSigString(x) )
        for sigstring in self.m_children:
           print >>this_file, sigstring
        print >>this_file, "\n----------------------------------\n"  

    def latex(self, this_file):
        newpage = "\\newpage"
        print >>this_file, newpage, "{\\bf", self.m_nucleus_string,"}",  "\n\\\\{\\bf Satellite affixes:}\n"
        print >>this_file, "\\begin{tabular}{ll}" 
        affix_list = sorted(self.m_satellite_affixes.keys())
        affix_list.sort(key = lambda affix: self.m_affix_counts[affix], reverse= True)
        for affix in affix_list:
            print >>this_file, affix, " & " , self.m_affix_counts[affix], "\\\\" 
        print >>this_file, "\\end{tabular}" 
        print >>this_file
 
        self.m_children.sort(key = lambda x: NumberOfAffixesInSigString(x) )
        print >>this_file, "\\begin{tabular}{ll}" 
        for sigstring in self.m_children:
           print >>this_file, sigstring, "\\\\" 
        print >>this_file, "\n----------------------------------\n"  
        print >>this_file, "\\end{tabular}"
        print >>this_file
     







def find_families(Lexicon, affix_type):
    MINIMUM_ROBUSTNESS = 400
    # search_list is a list of the signatures. We successively remove from it signatures that are not larger than one of its
    # up-neighbors or down-neighbors
    signatures = sorted(Lexicon.Signatures.values(), key = lambda x:  x.get_internal_robustness(), reverse = True)
    families = Lexicon.Families
    search_list = list(signatures)
    temp_sig_list = list()
    
    family_file = open ("families_old_method.txt", "w")
    
    for signo in range(len(signatures)):
        comparing_sig = signatures[signo]   
        if comparing_sig.get_internal_robustness() < MINIMUM_ROBUSTNESS:
            break;
        #comparing_sig_string = comparing_sig.get_affix_string()
        comparing_sig_length = comparing_sig.get_affix_length()
        comparing_sig_list = comparing_sig.get_affix_list()
        comparing_sig_robustness = comparing_sig.get_internal_robustness()
        
        lower_sig_list = list()
        while search_list and search_list[0].get_internal_robustness() > comparing_sig_robustness:
            lower_sig = search_list.pop(0)
            families.add_family(lower_sig)
        while search_list: 
            lower_sig = search_list.pop(0)
            if lower_sig.get_internal_robustness() < MINIMUM_ROBUSTNESS:
                break;
            lower_sig_list = lower_sig.get_affix_list()
            length = lower_sig.get_affix_length()
            if (length == comparing_sig_length  or
                length > comparing_sig_length + 1 or
                length < comparing_sig_length -1 ):
                temp_sig_list.append(lower_sig)
            elif length == comparing_sig_length + 1:
                if list_contains(lower_sig_list, comparing_sig_list):
                    pass
                else:
                    temp_sig_list.append(lower_sig)
            elif length == comparing_sig_length - 1:
                if list_contains(comparing_sig_list, lower_sig_list):
                    pass
                else:
                    temp_sig_list.append(lower_sig)

        if len(temp_sig_list) == 0:
            break
        search_list = temp_sig_list
        temp_sig_list = list()
    for sig in signatures:
        #print 100, "adding signature", sig.get_affix_string()
        families.add_signature(sig)
    families.print_families(family_file)
    family_file.close()



class family_collection:
    def __init__(self):
        self.m_families = dict() # key is signature_string and value is a family
    def nucleus_to_children(self, sigstring):
        return self.m_families[sigstring]   #this is a *list*
    def create_families(self, lexicon, number_of_families = 30):
        tempfile = open ("create_families.tex", "w" )
	StartLatexDoc(tempfile)

        signature_list = lexicon.Signatures.values()
        signature_list.sort(key = lambda  sig: sig.get_stem_count(), reverse=True)
        if number_of_families > len(lexicon.Signatures):
            number_of_families = len(lexicon.Signatures)
        nucleus_list = list()
        for signo in range(number_of_families):
            self.add_family(signature_list[signo])
            nucleus_list.append(signature_list[signo])
        signature_list = signature_list[number_of_families: ]

        n= 1
        print >>tempfile , "\n =================\n"
        print >>tempfile , "Nuclei of families, sorted by robustness\n"  
        print >>tempfile, "\\begin{tabular}{lll}" 
        for sig in nucleus_list:
            print >>tempfile, n, " & " , sig.latex()
            n+=1
        print >>tempfile, "\\end{tabular}" 

        signature_list.sort(key = lambda sig: sig.get_affix_length(), reverse = True)
        signature_list = [sig for sig in signature_list if sig.get_stability_entropy() > 1.5]
        nucleus_list.sort(key = lambda sig: sig.get_affix_length(), reverse=True )

        n= 1
        print >>tempfile , "\\newpage" 
        print >>tempfile, "Sorted by number of affixes, high stability\n" 
        print >>tempfile, "\\begin{tabular}{lll}" 
        for sig in nucleus_list:
            if sig.get_stem_count()  > 0:
		    print >>tempfile, n, " & " , sig.latex()
		    n+= 1
        print >>tempfile, "\\end{tabular}" 



        # check if one of these seeds contains the other  
  
        # now add signatures to these families
        # sort for longest signature first, so that when we look at the rest of the signatures, it's the longest signature 
	# of the nucleus signatures that captures each of the signatures
	
        print >>tempfile, "\nNo family found:\n" 
        in_family_count = 0
        out_of_family_count = 0
        none_found_list = list()
        for signo in range(len(signature_list)):
            foundflag = False
            this_sig = signature_list[signo]
            for nucleus_sig in nucleus_list:
                if this_sig.contains(nucleus_sig):
                    self.m_families[nucleus_sig.display()].add_signature(this_sig)
                    foundflag = True
                    in_family_count += 1
                    break
            if foundflag == False :
                #print >>tempfile, this_sig.display() 
                out_of_family_count += 1
                none_found_list.append(this_sig)

        print >>tempfile, "\\newpage" 
        print >>tempfile, "\nOut of family (Count: " , out_of_family_count, ")"  
        print >>tempfile , "\n =================\n" 
        print >>tempfile, "\\begin{tabular}{ll}" 
	none_found_list.sort()
        for sig in none_found_list:
            print >>tempfile, sig.latex()
        print >>tempfile, "\\end{tabular}" 

        print >>tempfile, "\\newpage" 
        print >>tempfile, "\nOut of family, sorted by stem count"   
        print >>tempfile , "\n =================\n" 
        print >>tempfile, "\\begin{tabular}{ll}" 
	none_found_list.sort(key = lambda x: x.get_stem_count(),reverse=True)
        for sig in none_found_list:
            print >>tempfile, sig.latex()
        print >>tempfile, "\\end{tabular}" 

        print >>tempfile , "\n =================\n" 

        print >>tempfile, "\nIn family Count: " , in_family_count 

        self.print_families(tempfile) 
	
	EndLatexDoc(tempfile)
        tempfile.close()

    def add_family(self, nucleus_sig):
        nucleus_sig_string = nucleus_sig.display()
        new_family = family(nucleus_sig_string)
        self.m_families[nucleus_sig_string] = new_family
	#print 76, "adding family:" , nucleus_sig_string

    def get_family(self, nucleus_string):
        return self.m_families[nucleus_string]

    def add_signature(self, signature):
        sigstring = signature.get_affix_string()
        for this_family in self.m_families:
            if contains(sigstring, this_family):
                self.m_families[this_family].add_signature(signature)
            else:
                pass
    def print_families(self, this_file):
        family_list = sorted(self.m_families.items(), key = lambda sig: NumberOfAffixesInSigString(sig[0]), reverse = True)
        for this_family in family_list:
            #print 91, this_family[0]
            self.m_families[this_family[0]].latex(this_file)


