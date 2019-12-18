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

class family:
    def __init__(self, nucleus_sig_string):
        #print 12, "family constructor", nucleus_sig
        self.m_nucleus_string = nucleus_sig_string # is a singnature
        self.m_nucleus_list = signature_string_to_signature_list(nucleus_sig_string)
        #print 14, self.m_nucleus
        self.m_children = list()  # list of signatures
        self.m_satellite_affixes = dict() # key is affix, value is list of signature_strings containing that affix
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
            self.m_satellite_affixes[affix].append(sig_string)
    def print_family(self, this_file):
        print >>this_file,  "\n35" + self.m_nucleus_string
        print >>this_file, "Satellite affixes: "
        affix_list = sorted(self.m_satellite_affixes.keys())
        for affix in affix_list:
            print >>this_file, affix, 
        print >>this_file
        #for sig_string in self.m_children:
        #    print "\t" + sig_string











def find_families(Lexicon, affix_type):
    MINIMUM_ROBUSTNESS = 400
    # search_list is a list of the signatures. We successively remove from it signaures that are not larger than one of it
    # up-neighbors or down-neighbors
    signatures = sorted(Lexicon.Signatures.values(), key = lambda x:  x.get_internal_robustness(), reverse = True)
    families = Lexicon.Families
    search_list = list(signatures)
    temp_sig_list = list()
    
    family_file = open ("families2.txt", "w")
    
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