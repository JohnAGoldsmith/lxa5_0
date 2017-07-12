import math

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
        outfile.write("</table>")

def start_an_html_table_row(outfile):
        outfile.write("<tr>\n")

def end_an_html_table_row(outfile):
        outfile.write("</tr>\n")


def start_an_html_div(outfile, class_type=""):
   outfile.write("\n\n<div class=\""+ class_type + "\">\n")

def end_an_html_div(outfile):
   outfile.write("\n</div>\n")

def add_an_html_table_entry(outfile,item):
   outfile.write("<td>{0:1s}</td>\n".format(item))

def add_an_html_header_entry(outfile,item):
   outfile.write("<th>{0:1s}</th>\n".format(item))




class Page:
    def __init__(self):
        self.my_height =5000
        self.my_width=10000
	self.my_column_width = 250
	self.my_row_height = 200
        self.Node_dict = dict()
        self.Arrow_dict = dict()

    def add_arrow(self, outfile, from_node, to_node):
        from_row, from_column = self.Node_dict[from_node]
        to_row, to_column     = self.Node_dict[to_node]
        arrow_code = "<line x1=\"" + {0:d} + "\ y1 = \"" + {1:d} + "\" x2=\"" + {2:d} + "\"y2 = \"" +{3:d} + "\" style=\"strike:rgb(255,0,0); stroke-width:2\" />"
        outfile.write(arrow_code)


    def start_an_html_file(self, outfile):
        start_an_html_file(outfile)
        string1 = "<svg width=\"{0:2d}\" height=\"{1:2d}\">\n"
        outfile.write(string1.format(self.my_width,self.my_height))
        return outfile

    def end_an_html_file(self,outfile):
        outfile.write("</svg>\n")
        end_an_html_file(outfile)


    def print_text(self,outfile,rowno,colno,text):
        (x,y) = self.coor_from_row_col(rowno,colno)
        row_factor = 0.10
        y += self.my_row_height * row_factor + 10
	outstring1 = "<text x=\"{}\" y=\"{}\" font-family=\"Verdana\" text-anchor=\"middle\" font-size=\"20\">"
	outstring2 = "</text>\n"
	if len(text) < 15:
		outfile.write(outstring1.format(x,y) + text + outstring2)
	elif len(text)<30:
	    text_height = self.my_row_height * row_factor
	    sig_list = text.split("=")
	    number_of_affixes = len(sig_list)
	    half = number_of_affixes / 2
	    first_line_list = sig_list[0:half]
	    second_line_list = sig_list[half:number_of_affixes]
	    outstring1 = "<text x=\"{}\" y=\"{}\" font-family=\"Verdana\" text-anchor=\"middle\" font-size=\"20\">\n"
	    outstring2 = "</text>\n"
	    outfile.write(outstring1.format(x,y) + "=".join(first_line_list) + outstring2)
	    outfile.write(outstring1.format(x,y + text_height) + "=".join(second_line_list) + outstring2)

        else:	    
	    text_height = self.my_row_height * row_factor
	    sig_list = text.split("=")
	    number_of_affixes = len(sig_list)
	    third = number_of_affixes/3
	    first_line_list = sig_list[0:third]
	    second_line_list = sig_list[third:2 * third]
	    third_line_list = sig_list[2*third:number_of_affixes]
	    outstring1 = "<text x=\"{}\" y=\"{}\" font-family=\"Verdana\" text-anchor=\"middle\" font-size=\"20\">\n"
	    outstring2 = "</text>\n"
	    outfile.write(outstring1.format(x,y) + "=".join(first_line_list) + outstring2)
	    outfile.write(outstring1.format(x,y + text_height) + "=".join(second_line_list) +outstring2)
	    outfile.write(outstring1.format(x,y + 2* text_height) + "=".join(third_line_list) + outstring2)
	    
	    
	    
    def coor_from_row_col (self, rowno, colno):
	x = self.my_column_width * (colno)
	y = self.my_height - self.my_row_height * (rowno)
        return (x,y)

    def print_circle (self, outfile, rowno,colno, count = 10):
	(xcoord,ycoord) = self.coor_from_row_col (rowno, colno)
	if count == 1:
          circle_string =  "<circle cx=\"{0:3d}\" cy=\"{1:3d}\" r=\"{2:1d}\"  stroke=\"black\" stroke-width=\"3\" fill=\"red\" />\n"
          radius=1
          outfile.write( circle_string.format(xcoord,ycoord,radius) )	
        else:
          circle_string =  "<circle cx=\"{0:3d}\" cy=\"{1:3d}\" r=\"{2:1f}\"  stroke=\"black\" stroke-width=\"3\" fill=\"red\" />\n"
          radius=5 * math.log(count)
          outfile.write( circle_string.format(xcoord,ycoord,radius) )	        	
 
	
    def print_signature (self,outfile,text, count, rowno, colno  ):
        self.print_circle(outfile, rowno,colno,count)
 	self.print_text(outfile,rowno, colno, text)

	    






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


class Stack:
    def __init__(self):       
        self.my_box_list = list()


class Box:

    def __init__(self, string_list,genre="None"):
        if genre == "signature":
            self.my_string_list = string_list.split("=")
        else:
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
        start_an_html_div(outfile, class_type=genre)
        if self.genre == "suffix":
                div_class="suffixclass"
        else:
                div_class="neutral"
         
        start_an_html_table(outfile)
        if self.genre=="suffix" or self.genre=="prefix" or self.genre=="signature":
            for morph in self.my_string_list:
                start_an_html_table_row(outfile)
                add_an_html_table_entry(outfile,morph)
                end_an_html_table_row(outfile)
            end_an_html_table(outfile)
        else:   
            colno=0
            for stemno in range(len(self.my_string_list)):
                if colno == 0:
                        start_an_html_table_row(outfile)
                add_an_html_table_entry(outfile,self.my_string_list[stemno])
                colno += 1
                if colno == self.number_of_columns:
                    end_an_html_table_row(outfile)
                    colno = 0
                while colno < self.number_of_columns :
                    add_an_html_table_entry(outfile,"")
                    colno += 1
                    end_an_html_table_row(outfile)
            end_an_html_table(outfile)
        #end_an_html_div(outfile)




















        
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



 

  
