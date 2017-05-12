from signaturefunctions import *


def signature_by_stem_data(Lexicon):
    SignatureStemList = dict()
    SigDataDict = dict()
    for sig_string in Lexicon.SignatureStringsToStems:
        sig_list = MakeSignatureListFromSignatureString(sig_string)
        SignatureStemList[sig_string] = list()
        for stem in Lexicon.SignatureStringsToStems[sig_string]:
            SignatureStemList[sig_string].append(stem)

        SigDataDict[sig_string] = dict()
        for affix in sig_list:
            SigDataDict[sig_string][affix] = list()
            for stem in SignatureStemList[sig_string]:
                word = stem + affix
                SigDataDict[sig_string][affix].append(Lexicon.WordCounts[word])
    return (SignatureStemList, SigDataDict)
