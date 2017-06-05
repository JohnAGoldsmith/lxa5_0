class Page:
    def __init__(self):
        self.my_height =1000
        self.my_width=1000


    def start_an_html_file(self, outfile):
 

 
        outfile.write("<!DOCTYPE html>\n")
        outfile.write("<html>\n")
        outfile.write("<head>\n")
        outfile.write("<link rel=\"stylesheet\" href=\"style.css\">\n")
        outfile.write("</head>\n")
        outfile.write("<body>\n")
        #string1 = "<svg width=\"{0:1d}\" height=\"{1:1d}\">\n"
        #outfile.write(string1.format(self.my_width,self.my_height))
        return outfile

    def end_an_html_file(self,outfile):
        #outfile.write("</svg>\n")
        outfile.write("</body>\n")
        outfile.write("</html>\n")
        outfile.close()
        


    def print_box(self, outfile,  this_box,x,y):
        # x and y are the lower left points of the box, in Page-logical units, where the origin of the Page is its lower left-hand corner
        
        #this_box.number_of_columns = int(len(this_box.my_string_list)/this_box.max_column_height + 0.5)
 
        startpoint_x = x
        startpoint_y = self.my_height - y - this_box.my_height
 
        if this_box.genre == "suffix":
                div_first="\n\n<div class=\"suffixclass\">\n"
        else:
                div_first="\n\n<div class=\"morphemeclass\">\n"
        div_last = "</div>\n    "
        line_first="<table>\n"
        line_last = "</table>\n"
        line_begin = "<tr>\n"
        line_end = "</tr>\n"
        entry = "<td>{0:1s}</td>\n"
        
        outfile.write(div_first)
        outfile.write(line_first)

        if this_box.genre=="suffix":
            for morph in this_box.my_string_list:
                outfile.write(line_begin)
                outfile.write(entry.format(morph))
                outfile.write(line_end) 
            outfile.write(line_last)

        else:   
                colno=0
                for stemno in range(len(this_box.my_string_list)):
                  if colno == 0:
                        outfile.write(line_begin)
                  outfile.write(entry.format(this_box.my_string_list[stemno]) )
                  colno += 1
                  if colno == this_box.number_of_columns:
                        outfile.write(line_end)
                        colno = 0
                while colno < this_box.number_of_columns :
                     outfile.write(entry.format(""))
                     colno += 1
                outfile.write(line_last)
         
        outfile.write(div_last)

    def print_signature_box(self,outfile,this_signature_box,x,y):
        deltax = this_signature_box.my_box1.my_width + 25
        div_first="\n\n<div class=\"signature\">\n"
        div_last ="</div>"
        outfile.write(div_first)
        self.print_box(outfile, this_signature_box.my_box1,x,y)
        self.print_box(outfile, this_signature_box.my_box2,x+deltax, y)
        outfile.write(div_last)
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
        

 
class SignatureBox:
    def __init__(self,stem_list,affix_list):
        self.my_box1=Box(stem_list,"stem")
        self.my_box2=Box(affix_list,"suffix")
        self.my_box1.genre="stem"
        self.my_box2.genre="suffix"

 

 

  
