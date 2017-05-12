# Create by Lang Yu, 11:35 PM, Jan 25, 2017
# langyu at uchicago dot edu

from utility import *


class Stem:
    def __init__(self, stem, sig_list):
        self.stem = stem
        self.sig_list = sig_list
        self.forms = []
        self.form_to_sig = {}
        for sig in sig_list:
            if sig == "NULL":
                form = stem
            else:
                form = stem + sig
            self.forms.append(form)
            self.form_to_sig[form] = sig
        self.sig_to_cnt = {}  # sig -> [count, freq] dictionary
        self.total_appr = 0

    def contain(self, word):
        # check whether this stem has a form WORD
        return word in self.form

    def is_in(self, str_list):
        hit = []
        for form in self.forms:
            for index, word in enumerate(str_list):
                if word == form:
                    hit.append((index, self.form_to_sig[form]))
        return hit

    def calc_freq(self, word_cnt_dic):
        total_cnt = 0
        for form in self.forms:
            cnt = word_cnt_dic[form]
            sig = self.form_to_sig[form]
            self.sig_to_cnt[sig] = [cnt, 0]
            total_cnt += cnt

        self.total_appr = total_cnt
        for sig in self.sig_to_cnt:
            cnt = self.sig_to_cnt[sig]
            self.sig_to_cnt[sig][1] = float(cnt[0]) / total_cnt

    def self_print(self):
        logging(str(self.stem), newline=False)
        logging(str(self.sig_list))
        for sig in self.sig_to_cnt:
            logging(str(self.sig_to_cnt[sig][1]), newline=False)
        logging("")

    @staticmethod
    def refine_hits(hits):
        # Remove redundant hit and sort according to index
        tmp = []
        for hit in hits:
            index, sig = hit
            if sig not in tmp:
                tmp.append(sig)
            else:
                hits.remove(hit)
        hits.sort()
