# LCSC2ALDI.py
# A python script to create labels for LCSC parts for small parts container
# like https://www.aldi-sued.de/de/p.workzone-kleinteilemagazin-oder--depot.490000000000802859.html
# 
# It takes your exported BOM (CSV files) from LCSC.com, collects information about the parts
# and puts it into document in form of a table - to be cut and glued on the containers

# Definitions

# Sheet format
# currently only A4 is supported
PAPER_H = 247
PAPER_W = 170 

# Label sizes (in mm)
LABEL_W = 63
LABEL_H = 12





# # # 0. Parse arguments - use argparse module for that

#parser.add_argument('file', type=argparse.FileType('r'), nargs='+')

# # # 1. Extract the Cxxx part numbers from CSV files (BOM-Export on LCSC)

# Example CSV File
CSV_File = 'example.csv'

listOfParts = []

with open(CSV_File, "r", encoding="utf-8") as file:
    for line in file:
        part = line.split(',')[0]
        
        if part.lower().startswith('c'):
            listOfParts.append(part)
        
    #print(lines.encode('cp1250', errors="replace"))
    #print(file.read().encode('cp1250', errors="replace"))

print(listOfParts)

# # # 2. Iterate over the listOfParts, Get data from LCSC.com and gather info to the database (Part type, values etc)
#       this step is pretty complex and it might take some time until we get it right

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

# # # 3. Create a PDF document with labels.