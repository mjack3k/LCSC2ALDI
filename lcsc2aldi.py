# LCSC2ALDI.py
# A python script to create labels for LCSC parts for small parts container
# like https://www.aldi-sued.de/de/p.workzone-kleinteilemagazin-oder--depot.490000000000802859.html
# 
# It takes your exported BOM (CSV files) from LCSC.com, collects information about the parts
# and puts it into document in form of a table - to be cut and glued on the containers

# Install https://miktex.org/, then latexmk in Packages inside miktex MikTeX console
# Install Perl (Windows: https://strawberryperl.com/ Linux: Your distro probly already provided perl for you)
# Install python modules: argparse, pylatex, pdflatex

# Imports
import math
import argparse
import subprocess
import requests


# Definitions and variables

# Sheet format
# currently only A4 is supported
PAPER_H = 247
PAPER_W = 170 

# Label sizes (in mm)
LABEL_W = 63
LABEL_H = 12








# # # 0. Parse arguments - use argparse module for that

# Get list of csv_files
def ParseArgs():
    parser = argparse.ArgumentParser(description='Create labels for your LCSC parts')
    parser.add_argument('csv_file', type=str, nargs='+')
    args = parser.parse_args()

    return args.csv_file



# # # 1. Extract the Cxxx part numbers from CSV files (BOM-Export on LCSC)

def GetCNumberssFromCSV(fileList):
    cList = []

    for f in fileList:
        with open(f, "r", encoding="utf-8") as file:
            for line in file:
                part = line.split(',')[0]
        
                if part.lower().startswith('c'):
                    cList.append(part)
    
    cList = list(dict.fromkeys(cList))  # remove duplicates
    return cList


# # # 2. Iterate over the listOfParts, Get data from LCSC.com and gather info to the database (Part type, values etc)
#       this step is pretty complex and it might take some time until we get it right


def GetPartsStrings(listOfParts):
    labels = []
    
    knownCategories=['Capacitors', 'Resistors']
    
    
    for part in listOfParts:
        # Get category
        categories = []
        website = requests.get('https://www.lcsc.com/product-detail/' + part + ".html")

        i = -1
        try:
            while website.text.index('v-breadcrumbs__item', i+1):
                # get "breadcrumbs":
                i = website.text.index('v-breadcrumbs__item', i+1)
                #print(website.text[i2:].encode("utf-8"))
                breadcrumb = website.text[i:].partition('>')[2].partition('<')[0].encode("utf-8")
                #print(breadcrumb)
                categories.append(breadcrumb)
        except:
            #print("No more categories")
            pass
            
        # Get package
        i = website.text.index('>Package<', 0)
        i = website.text.index('<td', i)
        package = website.text[i+9:].partition('>')[2].partition('<')[0].encode("utf-8")
        #print(package)
        
        # Value ?
        i = website.text.index('"description":"', 0)
        #i = website.text.index('', i)
        value = website.text[i+15:].partition('"')[0].replace("ROHS","").split(" ")
        value = ' '.join(value[:4])
        value = value.encode("utf-8")
        
        if str(categories[2].decode("utf-8")) in knownCategories:
            #print((part + " " + str(categories[2]) + " " + str(package) + " " + str(value)).encode("utf-8"), flush=True)
            labels.append((part, categories[2].decode("utf-8"), package.decode("utf-8"), value.decode("utf-8")))
        else:
            #print(categories[2])
            #print((part + " " + str(categories[-1]).split(' ')[-1] + " " + str(package) + " " + str(value)).encode("utf-8"), flush=True)
            labels.append((part, categories[-1].decode("utf-8").split(' ')[-1], package.decode("utf-8"), value.decode("utf-8")))
        
    print(len(labels))
    return labels

# 2.1 Create templates for various part types - resistors, capacitors, diodes, LEDs, microcontrollers, various ICs, connectors etc
#       Not all parts on LCSC are properly defined - very often values are missing and you need to extract them from datasheet
#       Getting information from PDF might be too complex for this simple project. Maybe asking user to input missing info by hand
#       can be considered a viable alternative?
#
# 2.2 Use http requests to get info from website - this is nice project idea on its own. Once we get the basics done, we should be able
#       to gather at least the most important values with ease - probly 80% of what we need. Bit of love might be needed to get 
#       rest of it
#
# 2.3 Put data into database. I'm not sure if we should create a REAL db (SQL, MySQL, MariaDB, SQLite etc), or just keep the data in lists/dicts
#       inside this project. If we kept data in db, we could reuse it in other projects ("warehouse management" or something, other project idea
#       I had - simple gui to manage how many parts are available, and where are they located). 
#       If no external DB should be used, then just keeping parts in local variables is fine (I guess?). 
#       

# Based on the part (category), provide the right icon (filename + path) string to be used in the PDF
def GetIconForPart(part):
    try:
        partStr = part.decode("utf-8")
    except:
        partStr = part

    iconFile = "icons/"

    if partStr == "Capacitors":
        iconFile+="capacitor.png"
    elif partStr == "Resistors":
        iconFile += "resistor.png"
    else:
        iconFile +="microchip.png"

    return iconFile

# # # 3. Create a PDF document with labels.

# 3.1 Check how many cells can fit on one page & how many pages we need

def GetTableSize(listOfParts):
    nCols = math.floor(PAPER_W/LABEL_W)
    nRows = math.floor(PAPER_H/LABEL_H)

    # Cells per sheet
    nCells = nCols*nRows

    nPages = math.ceil(len(listOfParts) / nCells)
    
    return nCols, nRows

# 3.2 Create basic Latex document structure

# 3.3 Create table and fill cells with informations about the parts

# 3.4 Compile to PDF

def CreatePDF(parts):
    #print(listOfParts)
    nCols, nRows = GetTableSize(parts)
    #print(nCols)
    #print(nRows)
    
    TEXFILE="LCSC_Labels.tex"
    
    with open(TEXFILE, "w", encoding="utf-8") as file:
        # Write header
        file.write("\\documentclass{article}\n")
        file.write("\\usepackage{graphicx} % Required for inserting images\n")
        file.write("\\usepackage[thinlines]{easytable}\n")
        file.write("\\usepackage[margin=2cm]{geometry}\n")
        file.write("\\usepackage{longtable}\n")
        file.write("\\usepackage{tabularray}\n")
        #file.write("\\usepackage[utf8x]{inputenc}")
        file.write('\\title{LCSC2ALDI}\n')
        file.write("\\author{mjack3k}\n")
        file.write("\\date{March 2023}\n")
        file.write("\\begin{document}\n")
        #file.write("\\maketitle\n")

        # Put the table HERE!
        file.write("\\begin{longtblr}\n") # begin table
        file.write("[\n")
        file.write("\tcaption = {https://github.com/mjack3k/LCSC2ALDI},\n")
        file.write("]\n")

        file.write("{\n")
        file.write("\thlines,\n")
        file.write("\tvline{odd},\n")
        file.write("\trows = {12mm, font =\\tiny},\n")
        file.write("\tcolumn{odd} = {20mm},\n")
        file.write("\tcolumn{even} = {43mm},\n")
        file.write("\tcells = {c, m},\n")

        file.write("}\n")

        #for x in range(nCols):
        #    file.write("|m{20mm}m{43mm}")   # define columns
        #file.write("|}\n")

        file.write("\\hline\n")

        for x in range(nRows):
            for y in range(nCols):

                if y != 0:
                    file.write(" & ")

                if (len(parts) <= (x * nCols + y)):
                    file.write("0")
                else:
                    file.write("\\includegraphics[height=6mm]{" + GetIconForPart(parts[x*nCols + y][1]) + "} & ")
                    file.write(str(parts[x*nCols + y][0]))
                    file.write(" \\break ")
                    file.write(str(parts[x*nCols + y][1]))
                    file.write(" \\break ")
                    file.write(str(parts[x * nCols + y][2]))
                    file.write(" \\break ")
                    #try:
                    file.write(str(parts[x * nCols + y][3]))
                    #except:
                    #    pass



            #file.write("\\break \\includegraphics[width=10mm]{icons/led.png} & \\break C9999 \\break LED 1206 Emerald & derp & 2\\\\[12mm]")
            #file.write(" \\\\[12mm]")
            #file.write(" \\\\")
            file.write("\n")
            file.write("\\\\ \\hline\n")

        file.write("\\end{longtblr}")    # end table

        # End TEX document
        file.write("\\end{document}\n")






#     \break \includegraphics[width=10mm]{led.png} & \break 1206 EMERALD  & \break \includegraphics[width=10mm]{resistor.png} & \break R 10K 0603 1\% \\[12mm]
#     \hline
#     SYMBOL & R 10K 0603 1\% & SYMBOL & R 10K 0603 1\% \\[12mm]
#     \hline
#     SYMBOL & R 10K 0603 1\% & SYMBOL & R 10K 0603 1\% \\[12mm]
#     \hline
#







    subprocess.run(["xelatex", TEXFILE])




# The actual main() function
def main():
    csvFiles = ParseArgs()
    listOfParts = GetCNumberssFromCSV(csvFiles)
    labels = GetPartsStrings(listOfParts)
    CreatePDF(labels)

if __name__ == "__main__":
    main()
