import os.path

def Initialization(argparse, config_lxa ):

# --------------------------------------------------------------------##
#        parse command line arguments
# --------------------------------------------------------------------##

# The config.py file contains default or preferred values. 
# Anything not specified on the command line will be governed by the config file.

    parser = argparse.ArgumentParser(description='Compute morphological analysis.')
    parser.add_argument('-l', action="store", dest="language", help="name of language")
    parser.add_argument('-w', action="store", dest="wordcountlimit", help="number of words to read")
    parser.add_argument('-f', action="store", dest="infilename", help="name of file to read")
    parser.add_argument('-d', action="store", dest="data_folder", help="data directory")
    parser.add_argument('-o', action="store", dest="outfolder", help="folder where results are posted")
    parser.add_argument('-s', action="store", dest="affix_type", help="prefix or suffix")
    parser.add_argument('-F', action="store", dest="FSA", help="generate and print FSA")

    results = parser.parse_args()
    language = results.language

    if results.language != None:
            config_lxa["language"] = results.language
    if results.wordcountlimit != None:
            config_lxa["word_count_limit"] = int(results.wordcountlimit)
    if results.infilename != None:
            config_lxa["infilename"] = results.infilename
    if results.data_folder != None:
            config_lxa["data_folder"] = results.data_folder
    if results.outfolder !=None:
            config_lxa["outfolder"] = results.outfolder
    if results.affix_type in ["prefix","False","prefixes"]:
        config_lxa["affix_type"] = "prefix"
    elif results.affix_type in ["suffix", "suffixes", "True"]:
        config_lxa["affix_type"] = "suffix"
    if results.FSA == "FSA" or results.FSA== "True":
        config_lxa["FSA"] = True
    elif results.FSA == "False":
        config_lxa["FSA"] = False
    else:
        FSA_flag = config_lxa["FSA"]
 


    # --------------------------------------------------------------------##
    #    Determine folders for input, output; initialize output files
    # --------------------------------------------------------------------##

    config_lxa["datafolder"] = config_lxa["data_folder"]  +  config_lxa["infilename"] + "/"
    config_lxa["outfolder"] = config_lxa["data_folder"] + config_lxa["language"] + "/"+ "lxa/"
    config_lxa["dx1_folder"] = config_lxa["data_folder"] +  "/"
    if  config_lxa["infilename"][-4:] == ".txt":
        config_lxa["datatype"] = "CORPUS"
        config_lxa["complete_infilename"] = config_lxa["datafolder"] + config_lxa["infilename"]
    else:
        config_lxa["datatype"] = "DX1"
        config_lxa["complete_infilename"] = config_lxa["dx1_folder"] + config_lxa["infilename"]

    graphicsfolder  = config_lxa["outfolder"] + "graphics/"
    if not os.path.exists(graphicsfolder):
        os.makedirs(graphicsfolder)

    config_lxa["encoding"] = "asci"  # "utf8"
    config_lxa["BreakAtHyphensFlag"] = True

    # --------------------------------------------------------------------##
    #        Tell the user what we will be doing.
    # --------------------------------------------------------------------##

    formatstring_initial_1 = "{:40s}{:>15s}"
    print "\n\n" + "-" * 100
    print("Language:", language)
    if config_lxa["affix_type"] == "prefix":
        print     "Finding prefixes."
    else:
        print     "Finding suffixes."
    if config_lxa["datatype"] == "DX1":
        print formatstring_initial_1.format("Reading dx file: ", config_lxa["complete_infilename"])
    else:
        print formatstring_initial_1.format("Reading corpus: ", config_lxa["complete_infilename"])
    print formatstring_initial_1.format("Logging to: ", config_lxa["outfolder"])
    print formatstring_initial_1.format("Number of words: ", str(config_lxa["word_count_limit"]))
    print
    print "-" * 100
