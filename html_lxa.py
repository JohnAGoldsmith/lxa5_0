
def start_an_html_file( outfile): 
        outfile.write("<!DOCTYPE html>\n")
        outfile.write("<html>\n")
        outfile.write("<head>\n")
        outfile.write("<link rel=\"stylesheet\" href=\"style.css\">\n")
        outfile.write("</head>\n")
        outfile.write("<body>\n")
        

def end_an_html_file(outfile):
        outfile.write("</body>\n")
        outfile.write("</html>\n")
        outfile.close()

def start_an_html_table(outfile):
    outfile.write("<table>")
 
    
def end_an_html_table(outfile):
   outfile.write("</table>")  

 

def start_table_row(outfile):
    outfile.write("<tr>\n")

def add_table_entry(item, outfile):
  entry = "<td>{0:1s}</td>\n"
  outfile.write(entry.format(item))

def end_table_row(outfile):
  outfile.write("</tr>\n")

