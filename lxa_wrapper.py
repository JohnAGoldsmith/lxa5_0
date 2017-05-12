import matplotlib.pyplot as mplt
import pickle
import pylab as plt
import sys
from time_analysis import *

from ClassLexicon import *
from stem import *

FULL_CORP = "../workloads/browncorpus.txt"
OUT_FOLDER = "../lxa_data/data/"
FULL_CORP = "../../data/english/browncorpus.txt"
OUT_FOLDER = "../../data/english/lxa/"


# # DeprecationWarning("Extremely slow")
# def lxa_wrapper(lex_class):
#     # lex_class should be the binary dump of the ClassLexicon object in lxa5
#     out = open("./time_ana.csv", "w")
#     sig_dic = lex_class.SignatureToStems
#     f = open(FULL_CORP)
#     for item in sorted(sig_dic.items(), key = lambda x : len(x[1]), reverse = True):
#         sig, stems = item[0], item[1]
#         sig = sig.split("-")
#         for stem in stems:
#             s = Stem(stem, sig)
#             time = search_stems(f, s, 90000, rand = False)
#             #print time

def lxa_time_analysis(lex_class, time_dic):
    out = open(OUT_FOLDER + "test.csv", "w")
    sig_dic = lex_class.SignatureToStems
    for item in sorted(sig_dic.items(), key=lambda x: len(x[1]), reverse=True):
        sigs, stems = item[0], item[1]
        if len(stems) < 20:
            return
        sigs = sigs.split("-")
        sig_ind = {}
        pt = 0
        label = []
        # Use to map signatures to x-axis
        for sig in sigs:
            sig_ind[sig] = pt
            label.append(sig)
            pt += 1
        # out.write("index, stem, sig, offset\n")
        ######### Possible one ##############
        # out.write("index, stem, ")
        # for sig in sigs:
        #    out.write(sig + ", ")
        # out.write("\n")
        index = 0
        for stem in stems:
            s = Stem(stem, sigs)
            time = search_stems(time_dic, s)
            x = []
            y = []
            for sig in sigs:
                # out.write(str(index))
                # out.write(", " + stem + ", ")
                # out.write(str(sig) + ", ")
                # out.write(str(time[sig]) + "\n")
                x.append(sig_ind[sig])

                y.append(time[sig])
                index += 1
            plt.plot(x, y, label=stem)

            # plt.show()
            # if len(sigs) == 4:
            #    plt.show()
            if index == 500:
                break
        plt.xticks(x, label)
        # plt.legend(loc='upper left')
        plt.show()
        # plt.savefig(OUT_FOLDER + "time_" + str(sigs) + ".png")
        plt.clf()
        # print time
        # out.write(str(index))
        # out.write(", " + stem + ", ")
        # for sig in sigs:
        #    out.write(str(time[sig]))
        #    out.write(", ")
        # out.write("\n")
        # index += 1
        # return
        # print time


# def normalize_time_hits(time_hits):
#    pass

if __name__ == '__main__':
    fh = open("./dump", "r")
    f = open(FULL_CORP, "r")
    lex = pickle.load(fh)
    # lxa_wrapper(lex)
    time_dic = build_time_dic(f)
    lxa_time_analysis(lex, time_dic)
