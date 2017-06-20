def start_an_html_file(outfile):
        outfile.write("<!DOCTYPE html>\n")
        outfile.write("<html>\n")
        outfile.write("<head>\n")
        outfile.write("<link rel=\"stylesheet\" href=\"style.css\">\n")
        outfile.write("</head>\n")
        outfile.write("<body>\n")
       
def     end_an_html_file(outfile):
        outfile.write("</body>\n")
        outfile.write("</html>\n")
        outfile.close()
        
def start_an_html_table(outfile):
        outfile.write("<table>\n")

def end_an_html_table(outfile):
        outfile.write("</table>\n")

def start_an_html_table_row(outfile):
        outfile.write("<tr>\n")

def end_an_html_table_row(outfile):
        outfile.write("</tr>\n")


def start_an_html_div(outfile, class_type=""):
   outfile.write("\n\n<div class=\""+ class_type + "\">\n")

def end_an_html_div(outfile):
   outfile.write("\n\n</div>\n")

def add_an_html_table_entry(outfile,item):
   outfile.write("<td>{0:1s}</td>\n".format(item))

def add_an_html_header_entry(outfile,item):
   outfile.write("<th>{0:1s}</th>\n".format(item))



class Page:
    def __init__(self):
        self.my_height =1000
        self.my_width=1000


    def start_an_html_file(self, outfile):
        start_an_html_file(outfile)
        return outfile

    def end_an_html_file(self,outfile):
        end_an_html_file(outfile)

    def print_box(self, outfile,  this_box,x,y):
        # x and y are the lower left points of the box, in Page-logical units, where the origin of the Page is its lower left-hand corner
        #this_box.number_of_columns = int(len(this_box.my_string_list)/this_box.max_column_height + 0.5)
        startpoint_x = x
        startpoint_y = self.my_height - y - this_box.my_height
        if this_box.genre == "suffix":
                div_class="suffixclass"
        else:
                div_class="morphemeclass"
        start_an_html_div(outfile,div_class)
        start_an_html_table(outfile)
        if this_box.genre=="suffix" or this_box.genre=="prefix":
            for morph in this_box.my_string_list:
                start_an_html_table_row(outfile)
                add_an_html_table_entry(outfile,morph)
                end_an_html_table_row(outfile)
            end_an_html_table(outfile)
        else:   
                colno=0
                for stemno in range(len(this_box.my_string_list)):
                  if colno == 0:
                        start_an_html_table_row(outfile)
                  add_an_html_table_entry(outfile,this_box.my_string_list[stemno])
                  colno += 1
                  if colno == this_box.number_of_columns:
                        end_an_html_table_row(outfile)
                        colno = 0
                while colno < this_box.number_of_columns :
                     add_an_html_table_entry(outfile,"")
                     colno += 1
                end_an_html_table_row(outfile)
                end_an_html_table(outfile)
        end_an_html_div(outfile)

    def print_signature_box(self,outfile,this_signature_box,x,y):
        deltax = this_signature_box.my_stack1.my_width + 25
        start_an_html_div(outfile, class_type="signature")
        self.print_box(outfile, this_signature_box.my_stack1,x,y)
        self.print_box(outfile, this_signature_box.my_stack2,x+deltax, y)
        end_an_html_div(outfile)

class Stack:
    def __init__(self):       
        self.my_box_list = list()


class Box:

    def __init__(self, string_list,genre="None"):
        self.my_string_list = list(string_list)
        if len(string_list) > 200:
            self.number_of_columns = 30  
        elif len(string_list) > 50:
            self.number_of_columns = 10
        else:
            self.number_of_columns = 4
        self.max_column_height = 10
        self.my_height = 100
        self.my_width = 100
        self.heightperletter = 15
        self.widthperletter = 10
        self.alignment = "start"
        self.genre=genre
        templist = []
        if genre=="stem":               
            for stem in self.my_string_list:
                templist.append(stem[::-1])
            templist.sort()
            self.my_string_list = list()
            for stem in templist:
                newstem=stem[::-1]
                self.my_string_list.append(newstem) 
    def print_box(self,  outfile, genre= "neutral" ):
        start_an_html_div(outfile, class_type="genre") 
        if this_box.genre == "suffix":
                div_class="suffixclass"
        else:
                div_class="neutral"
         
        start_an_html_table(outfile)
        if this_box.genre=="suffix" or this_box.genre=="prefix":
            for morph in this_box.my_string_list:
                start_an_html_table_row(outfile)
                add_an_html_table_entry(outfile,morph)
                end_an_html_table_row(outfile)
            end_an_html_table(outfile)
        else:   
                colno=0
                for stemno in range(len(this_box.my_string_list)):
                  if colno == 0:
                        start_an_html_table_row(outfile)
                  add_an_html_table_entry(outfile,this_box.my_string_list[stemno])
                  colno += 1
                  if colno == this_box.number_of_columns:
                        end_an_html_table_row(outfile)
                        colno = 0
                while colno < this_box.number_of_columns :
                     add_an_html_table_entry(outfile,"")
                     colno += 1
                end_an_html_table_row(outfile)
                end_an_html_table(outfile)
        end_an_html_div(outfile)




















        
        end_an_html_div(outfile)

 

 
class SignatureBox:
    def __init__(self,stem_list,affix_list,FindSuffixesFlag):
        self.my_two_column_box = TwoColumnBox()
        if FindSuffixesFlag:
            self.my_stack1 = Box(stem_list,"stem")
            self.my_stack2 = Box(affix_list,"suffix")
        else:
            self.my_stack1 = Box(stem_list,"prefix")
            self.my_stack2 = Box(affix_list,"stem")       

    def print_signature_box(self,  outfile, Page, x, y):
        deltax = self.my_stack1.my_width + 25
        start_an_html_div(outfile, class_type="signature")
        Page.print_box(outfile, self.my_stack1,x,y)
        Page.print_box(outfile, self.my_stack2,x+deltax, y)
        end_an_html_div(outfile)

 


        
class ComplexSignatureBox:
    def __init__(self,stem_list,affix_list):
        self.my_two_column_box = TwoColumnBox()
        self.my_stack1 = list()
        self.my_stack1 = append.Box(stem_list,"stem")
        self.my_stack2 = Box(affix_list,"suffix")
    def print_complex_signature_box(self):
        deltax = self.my_stack1.my_width + 25
        start_an_html_div(outfile, class_type="signature")
        for box in self.my_stack1:
            Page.print_box(outfile, box)
        Page.print_box(outfile, self.my_stack2,x+deltax, y)
        end_an_html_div(outfile)        
         

class TwoColumnBox:
    def __init__(self):
        self.my_stack1 = Stack()
        self.my_stack2 = Stack()



 

  
