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

class family:
    def __init__(self, nucleus_sig):
        #print 12, "family constructor", nucleus_sig
        self.m_nucleus = nucleus_sig # is a singnature
        #print 14, self.m_nucleus

















def find_families(Lexicon, affix_type):
    MINIMUM_ROBUSTNESS = 400
    # search_list is a list of the signatures. We successively remove from it signaures that are not larger than one of it
    # up-neighbors or down-neighbors
    signatures = sorted(Lexicon.Signatures.values(), key = lambda x:  x.get_internal_robustness(), reverse = True)
    families = Lexicon.Families
    search_list = list(signatures)
    temp_sig_list = list()
    
    for signo in range(len(signatures)):
        comparing_sig = signatures[signo]   
        if comparing_sig.get_internal_robustness() < MINIMUM_ROBUSTNESS:
            break;
        comparing_sig_string = comparing_sig.get_affix_string()
        comparing_sig_length = comparing_sig.get_affix_length()
        comparing_sig_list = comparing_sig.get_affix_list()
        comparing_sig_robustness = comparing_sig.get_internal_robustness()
        
        lower_sig_list = list()
        while search_list and search_list[0].get_internal_robustness() > comparing_sig_robustness:
            lower_sig = search_list.pop(0)
            lower_sig_list = lower_sig.get_affix_list()
            new_family = family(lower_sig)
            families.append(new_family)
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
	
    for fam in families:
        print fam.m_nucleus.get_affix_list()
    # here we bring all remaining signatures in search_list to families, if they are big enough. 