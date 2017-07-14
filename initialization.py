import os
import os.path

def Initialization(argparse,config_lxa,FSA_flag):

    # --------------------------------------------------------------------##
    #		parse command line arguments
    # --------------------------------------------------------------------##

    # The config.py file contains default or preferred values. Anything not specified on the command line will be governed by the config file.

    parser = argparse.ArgumentParser(description='Compute morphological analysis.')
    parser.add_argument('-l', action="store", dest="language", help="name of language")
    parser.add_argument('-w', action="store", dest="wordcountlimit", help="number of words to read")
    parser.add_argument('-f', action="store", dest="infilename", help="name of file to read")
    parser.add_argument('-d', action="store", dest="data_folder", help="data directory")
    parser.add_argument('-s', action="store", dest="affix_type", help="prefix or suffix")
    parser.add_argument('-F', action="store", dest="FSA", help="generate and print FSA")


    results                 = parser.parse_args()
    language                = results.language



    if results.language != None:
            config_lxa["language"] = results.language
    if results.wordcountlimit != None:
            config_lxa["word_count_limit"] = int(results.wordcountlimit)
    if results.infilename != None:
            config_lxa["infilename"] = results.infilename

    if results.data_folder != None:
            config_lxa["data_folder"] = results.data_folder
    if results.affix_type == "True":
        FindSuffixesFlag = True
    elif results.affix_type == "False":
        FindSuffixesFlag = False
    else:   FindSuffixesFlag = True
    if results.FSA == "FSA" or results.FSA== "True":
        config_lxa["FSA"] = True
        FSA_flag = True
    elif results.FSA == "False":
        config_lxa.FSA = False
        FSA_flag = False
    else:
            FSA_flag = config_lxa["FSA"]

    print "FSA? ", FSA_flag

    # --------------------------------------------------------------------##
    #	Determine folders for input, output; initialize output files
    # --------------------------------------------------------------------##


    datafolder      = config_lxa["data_folder"] + config_lxa["language"] + "/"
    config_lxa["outfolder"]      = config_lxa["data_folder"] + config_lxa["language"] + "/"+ "lxa/"
    dx1_folder        = config_lxa["data_folder"] + config_lxa["language"] + "/"+ "dx1/"
    if  config_lxa["infilename"][-4:] == ".txt":
        config_lxa["datatype"]= "CORPUS"
        config_lxa["complete_infilename"] = datafolder + config_lxa["infilename"]
    else:
        config_lxa["datatype"]= "DX1"
        config_lxa["complete_infilename"] = dx1_folder + config_lxa["infilename"]

    config_lxa["graphicsfolder"]  = config_lxa["outfolder"] + "graphics/"


    if not os.path.exists(config_lxa["graphicsfolder"]):
        os.makedirs(config_lxa["graphicsfolder"])




    # --------------------------------------------------------------------##
    #		Tell the user what we will be doing.
    # --------------------------------------------------------------------##


    formatstring_initial_1 = "{:40s}{:>15s}"
    print "\n\n" + "-" * 100
    print("Language:", language)
    if FindSuffixesFlag:
        print     "Finding suffixes."
    else:
        print     "Finding prefixes."
    config_lxa["FindSuffixesFlag"] = FindSuffixesFlag
    if config_lxa["datatype"] == "DX1":
        print     formatstring_initial_1.format("Reading dx file: ", config_lxa["complete_infilename"])
    else:
        print     formatstring_initial_1.format("Reading corpus: ", config_lxa["complete_infilename"])
    print formatstring_initial_1.format("Logging to: ", config_lxa["outfolder"])
    print formatstring_initial_1.format("Number of words: ", str(config_lxa["word_count_limit"]))
    print
    print "-" * 100


    return
