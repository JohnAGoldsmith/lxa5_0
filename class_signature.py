import signaturefunctions as Sigfn
import stringfunctions as Strfn
import math
## -------                                                      ------- #
##              Class Signature                                 ------- #
## -------                                                      ------- #

class Signature:
    def __init__(self,affix_side,signature_string):
        self.affix_side = affix_side
        self.affixes_list = Sigfn.signature_string_to_signature_list(signature_string)
        self.stem_counts = dict()
        #if stems:
        #    for stem in stems:
        #        self.stem_counts[stem] = 1
        self.affixes_count_dict = dict()
        self.robustness = 0
        self.robustness_clean = False
        self.affixes_list.sort()
        self.name = ""
        if self.affix_side != affix_side:
            return None
        self.stability_entropy = -1.0

    def add_stem(self,stem, count = 1):
        if not self.stem_counts:
            self.stem_counts = dict()
        self.stem_counts[stem] = count
    def add_affix(self,affix):
        if affix in self.affixes_list:
            return
        self.affixes_list.append(affix)
    def get_affix_length(self):
        return len(self.affixes_list)
    def get_stems(self):
        return sorted(self.stem_counts.keys())
    def get_affix_list(self):
        return self.affixes_list
    def get_affix_string(self):
        #print 142, make_signature_string_from_signature_list(self.affixes_list)
        return Sigfn.make_signature_string_from_signature_list(self.affixes_list)
    def get_affix_count(self, affix):
        return len(self.affixes_list[affix])
    def get_stem_count(self):
        return len(self.stem_counts)
    def contains(self, other_sig):
        for item in other_sig.affixes_list:
            if item not in self.affixes_list:
                return False
        return True

    def get_internal_robustness(self):
        if self.robustness_clean:
	    #print 145, self.robustness
            return self.robustness
        else:
            robustness = 0
            affixes_length = 0
            for affix in self.affixes_list:
                if affix == "NULL":
                    affixes_length += 1
                else:
                    affixes_length += len(affix)
            robustness += affixes_length * (len(self.stem_counts) - 1)
            stems_length = 0
            for stem in self.stem_counts:
                stems_length += len(stem)
            robustness += stems_length * (len(self.affixes_list) - 1)
            self.robustness = robustness
            self.robustness_clean = True
	    #print 162, self.robustness
            return robustness
    def get_stability_entropy (self):
	"""Determines if this signature is prima facie plausible, based on letter entropy.
	       If this value is above 1.5, then it is a stable signature: the number of different letters
	       that precede it is sufficiently great to have confidence in this morpheme break."""

        if self.stability_entropy > -1:
            return self.stability_entropy
        entropy = 0.0
        stem_list = self.get_stems()
        frequency = dict()
        templist = list()
        if self.affix_side == "prefix":
            for chunk in stem_list:
                templist.append(chunk[::-1])
            stemlist = templist
        for stem in stem_list:
            stem = Strfn.remove_label(stem)
            lastletter = stem[-1]
            if lastletter not in frequency:
                frequency[lastletter] = 1.0
            else:
                frequency[lastletter] += 1.0
        for letter in frequency:
            frequency[letter] = frequency[letter] / len(stem_list)
            entropy += -1.0 * frequency[letter] * math.log(frequency[letter], 2)
        self.stability_entropy = entropy
        return entropy   
    def display(self):
        return "=".join(self.get_affix_list())
