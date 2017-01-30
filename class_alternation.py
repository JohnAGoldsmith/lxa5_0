
class CAlloform:
    def __init__(self,form, context, stemcount):
        self.Form = form
        self.Context = context
        self.StemCount = stemcount


# ----------------------------------------------------------------------------------------------------------------------------#
class CAlternation:
    def __init__(self, stemcount = 0):
        self.Alloforms = list() # list of CAlloforms
        self.Count = stemcount
        
    def AddAlloform(self, this_alloform):
            self.Alloforms.append(this_alloform)

    def MakeProseReportLine(self):
        ReportLine = CProseReportLine()


        return ReportLine.MakeReport( )


    def display(self):
        this_datagroup = CDataGroup("KeyAndList",self.Count)         
        for i in range(len(self.Alloforms)):
            alloform = self.Alloforms[i]
            this_datagroup.Count = self.Count
            if alloform.Form ==  "":
                key = "nil" 
            else:
                key = alloform.Form
            if key not in this_datagroup.MyKeyDict:
                this_datagroup.MyKeyDict[key]=list()
            this_datagroup.MyKeyDict[key].append(alloform.Context)
         
        return this_datagroup.display()

 #       for i in range(len(self.Alloforms)):
 #         

#            return_string = ""
#            alloform = self.Alloforms[i]
#            if alloform.Form ==  "":
#                key = "nil" 
#            else:
#                key = alloform.Form
#            this_datagroup.MyListOfKeys.append(key)
#            this_datagroup.MyKeyDict[key]##

#            return_string += key
#            return_string += " in context: "
#            return_string += alloform.Context
            
#            return_list.append(return_string) 
#        return return_list

    def prose_statement(self):
        alloform_dict=dict()
        alloform_list=list()
        elsewhere_case=None
        for alloform in self.Alloforms:
            print "G",   alloform.Form, alloform.Context
            key = alloform.Form
            if key not in alloform_dict:
                alloform_dict[key] = list()
            alloform_dict[key].append(alloform)
            if alloform.Context == "NULL":
                elsewherecase_form = alloform.Form
        number_of_alloforms= len(alloform_dict)

        for item in alloform_dict:
            temp_alloform = CAlloform(item, "", 0)
            alloform_list.append(alloform_dict[item])
            print "W", item, alloform_dict[item]
            for subitem in item:
                temp_alloform.Context += " "+subitem.Context


        return_string = ""
        for alloform_no in range(number_of_alloforms):
            thisreportline = CReportLine()

            #alloform_list[alloform_no] is a  list of alloforms, all with the same Key
            key = alloform_list[alloform_no][0].Key # take the Key from the first one, because they are all the same

            context_list = list()
            for n in range(len(alloform_list[alloform_no])):

                context_list.append(alloform_list[alloform_no].context)  
            return_string += key + ":".join(context_list)    
        return return_string            


# ----------------------------------------------------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------------#
class CProseReportLine:
    def __init__(self):
        self.MyList = list()
        self.MyLastItem = None

    def MakeReport(self):
        for item in self.MyList:
            returnstring += item.MyHead
            for item2 in self.MyTail:
                returnstring += " " + item2
        if self.MyLastItem:
            returnstring += item.MyHead
            for item2 in self.MyTail:
                returnstring += " " + item2  
        return returnstring         

# ----------------------------------------------------------------------------------------------------------------------------#
class CReportLineItem:
    def __init__(self):        
        self.MyHead = NULL
        self.MyTail = NULL
# ----------------------------------------------------------------------------------------------------------------------------#
class CDataGroup:
    def __init__(self, type,count):
        self.Type = type
        self.MyKeyDict = dict()
        self.Count = count


    def display(self):
        colwidth1 = 20
        colwidth2 = 40
        countstring = str(self.Count)
        returnstring = countstring + " "*(4-len(countstring))
        string1 = ""
        string2 =""

        ItemList = list(self.MyKeyDict.keys())
        #if there is a word-finally, put it in last place


        for i in range(len(ItemList)):
            phone = ItemList[i]
            if "\#" in self.MyKeyDict[phone]:
                #word final phoneme
                word_final_phone = ItemList[i]
                del ItemList[i]
                ItemList.append(word_final_phone)
        #if there is a "NIL", then put it in first place.
        for i in range(len(ItemList)):
            phone=ItemList[i]
            if phone== "nil":
                del ItemList[i]
                ItemList.insert(0,"nil")



        if self.Type == "KeyAndList":
            for key in ItemList:
                NULL_flag = False
                string1 = "[" + key + "]" 
                string2 = ""
                returnstring += string1 + " "*(colwidth1-len(string1))
               
                FirstItemFlag= True
                for item in self.MyKeyDict[key]:
                    if item == "NULL":
                        NULL_flag = True
                        continue
                    if FirstItemFlag:
                        string2 += "before " 
                        FirstItemFlag = False
                    string2 += "/"+item + "/ "
                if NULL_flag:
                    if FirstItemFlag == False:
                        string2 += "and word-finally."
                    else:
                        string2 += "word-finally."
                returnstring += string2 + " "*(colwidth2- len(string2))

                     
             
        return returnstring
# ----------------------------------------------------------------------------------------------------------------------------#

