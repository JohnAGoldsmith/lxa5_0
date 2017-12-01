import math

def start_an_html_file(outfile):
	#outfile = open (outfile_name, "w")
        outfile.write("<!DOCTYPE html>\n")
        outfile.write("<html>\n")
        outfile.write("<head>\n")
        outfile.write("<link rel=\"stylesheet\" href=\"style.css\">\n")
        outfile.write("</head>\n")
        outfile.write("<body>\n")
	return outfile
       
def     end_an_html_file(outfile):
        outfile.write("</body>\n")
        outfile.write("</html>\n")
        #outfile.close()
        
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
   outfile.write("\n</div>\n\n")

def print_an_html_table_entry(outfile,item):
   outfile.write("<td>{0:1s}</td>\n".format(item))

def add_an_html_header_entry(outfile,item):
   outfile.write("<th>{0:1s}</th>\n".format(item))

	


class Page:
    def __init__(self,label=""):
	self.my_label =label
        self.my_width=10000
	self.window_bottom = 0
	self.window_left = 0
	self.window_right = 20000
	self.window_top = 0
	self.my_column_width = 250
	self.my_row_height = 200
	self.highest_row = 1
        self.Node_to_row_col_dict = dict()   # key is a string (like, a signature string), value is a pair of row and column (indexes, not page-locations)
        self.Arrow_dict = dict() #key is a string of the form: "sig1 sig2"; value is not currently used
	self.Signatures = list()
	self.column_counts = dict()
	self.Table=list()

    def add_to_table(string):
	self.Table.append(string)
	
   
    def add_pair_to_table(self,(string1, string2)):
	self.Table.append((string1,string2))

    def print_table(self,outfile):
	start_an_html_table(outfile)
	for item in self.Table:
	    if len(item) == 2:
		start_an_html_table_row(outfile)
		print_an_html_table_entry(outfile,item[0])
		print_an_html_table_entry(outfile,item[1])
		end_an_html_table_row(outfile)
	    else:  
		start_an_html_table_row(outfile)
		print_an_html_table_entry(outfile,item)
		end_an_html_table_row(outfile)
	end_an_html_table(outfile)

	 	

    def display(self):
	print "\n\n" + "-"* 20
	print "Display of Page:"
	print "Label: ", self.my_label
	print "Number of nodes:", len(self.Signatures)
	print "Number of arrows: ", len(self.Arrow_dict)
	print "Nodes: "
	for node in self.Signatures:
		print node
	print "Number of items in Table:", len(self.Table)
	print "-"* 20 

    def print_arrow(self, outfile, from_node, to_node):
        from_row, from_column = self.Node_to_row_col_dict[from_node]
        to_row, to_column     = self.Node_to_row_col_dict[to_node]
	x1,y1 = self.coor_from_row_col(from_row, from_column)
	x2,y2= self.coor_from_row_col(to_row, to_column)
	if self.window_left and (x1 < self.window_left or x2< self.windows_left):
		return
	if self.window_right and (x1 > self.window_right or x2 > self.window_right):
		return
	if self.window_top and (y1 > self.window_top or y2 > self.window_top):
		return
	if self.window_bottom and (y1 < self.window_bottom or y2 < self.window_bottom):
		return 

	piece1 = "<line x1=\"{0:d}\" y1=\"{1:d}\""
	piece2 = " x2=\"{2:d}\" y2=\"{3:d}\""
	piece3 = " style=\"stroke:rgb(255,0,0);stroke-width:\"2\" />"
        arrow_code = piece1 + piece2 + piece3
        outfile.write(arrow_code.format(x1,y1,x2,y2) + "\n")
	
	

    def start_an_html_file(self, outfile):
        start_an_html_file(outfile)
	return outfile

    def end_an_html_file(self,outfile):
        end_an_html_file(outfile)

    def start_a_page(self,outfile):
        string1 = "<svg width=\"{0:2d}\" height=\"{1:2d}\">\n"
	self.my_height = self.highest_row * self.my_row_height + 100
	max_col = 0
	for (node,(row,col)) in self.Node_to_row_col_dict.items():
		if col > max_col:
		    max_col = col
	self.my_width = max_col * self.my_column_width + 400
        outfile.write(string1.format(self.my_width,self.my_height))
        return outfile

    def end_a_page(self,outfile):
        outfile.write("</svg>\n")
	return outfile

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
	x = self.my_column_width * (colno) + rowno * 30 # the 30 gives it a slant so the lines don't go through nodes unintentionally
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
          radius=15 * math.log(count)
          outfile.write( circle_string.format(xcoord,ycoord,radius) )	        	
 
    #deprecated:
    def print_signature (self,outfile,text, count, rowno, colno  ):
        self.print_circle(outfile, rowno,colno,count)
 	self.print_text(outfile,rowno, colno, text)

	# this adds the information to the object, but does not print it.
    def add_signature(self,Lexicon, sig): 
	self.Signatures.append(sig)
	row_no= sig.count("=")+1
        if row_no not in self.column_counts:
		self.column_counts[row_no] = 1
	else:
 	    self.column_counts[row_no] += 1
	col_no = self.column_counts[row_no]	
	self.Node_to_row_col_dict[sig] = ((row_no,col_no))  
	if row_no > self.highest_row:
		self.highest_row = row_no

    def add_signature_pair_for_arrow (self, from_sig, to_sig):
	signature_pair_string = from_sig + " " + to_sig
	self.Arrow_dict[signature_pair_string] = (from_sig, to_sig)


    def print_signatures (self,Lexicon,   outfile):
	self.start_a_page(outfile)
        outstring1 = "<text x=\"80\" y=\"100\" font-family=\"Verdana\" text-anchor=\"middle\" font-size=\"50\">\n"
	outstring2 = "</text>\n"
	outfile.write(outstring1 + self.my_label + outstring2)
	for sig in self.Signatures:
	    radius_guide = math.log(Lexicon.Robustness[sig]) #  FIX THIS
	    (row_no,col_no) = self.Node_to_row_col_dict[sig]
	    x,y = self.coor_from_row_col (row_no, col_no)
	    if self.window_left and x < self.window_left:
		continue
	    if self.window_right and x > self.window_right:
		continue
	    if self.window_top and y > self.window_top:
		continue
	    if self.window_bottom and y < self.window_bottom:
		continue    
	    self.print_circle(outfile, row_no,col_no,radius_guide)
	    self.print_text(outfile,row_no, col_no,sig)
	    for node_pair in self.Arrow_dict:
	        (node_key1,node_key2) = node_pair.split()

	        self.print_arrow(outfile, node_key1, node_key2)
	self.end_a_page(outfile)    
	
	self.print_table(outfile)


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
                print_an_html_table_entry(outfile,morph)
                end_an_html_table_row(outfile)
            end_an_html_table(outfile)
        else:   
                colno=0
                for stemno in range(len(this_box.my_string_list)):
                  if colno == 0:
                        start_an_html_table_row(outfile)
                  print_an_html_table_entry(outfile,this_box.my_string_list[stemno])
                  colno += 1
                  if colno == this_box.number_of_columns:
                        end_an_html_table_row(outfile)
                        colno = 0
                while colno < this_box.number_of_columns :
                     print_an_html_table_entry(outfile,"")
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
                print_an_html_table_entry(outfile,morph)
                end_an_html_table_row(outfile)
            end_an_html_table(outfile)
        else:   
            colno=0
            for stemno in range(len(self.my_string_list)):
                if colno == 0:
                        start_an_html_table_row(outfile)
                print_an_html_table_entry(outfile,self.my_string_list[stemno])
                colno += 1
                if colno == self.number_of_columns:
                    end_an_html_table_row(outfile)
                    colno = 0
                while colno < self.number_of_columns :
                    print_an_html_table_entry(outfile,"")
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



 

  
