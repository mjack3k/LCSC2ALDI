# LCSC2ALDI
Create labels for parts bought on LCSC for ALDI small parts containers

*WORK IN PROGRESS*

Made as a fun little project to help me manage my electronic parts for DIY projects.
The goal is to have a table with labels that you can print, cut and glue on the drawers of
small parts magazine, like the one here:  
 <img src="https://s7g10.scene7.com/is/image/aldi/202101120138" alt="alt text" width="400">



Usage:
python lcsc2aldi.py [CSV FILE]

You can use multiple CSV files in one go (*.csv will work too). 

The script will then gather information from LCSC website and generate a PDF you can print.
Then just cut the labels using scissors and glue on the drawers.

You need to have TEX (Xelatex) installed. 
For windows:
[https://miktex.org/](https://miktex.org/)

On Linux:
check your distribution repositories, most likely:
`sudo apt-get install texlive-xetex`


*Important notice*
This is still early version of the script. It more or less works, but the data in table
is still not quite right (for example - resistor values are missing completely!).

I am still working on it. Feel free to contribute yourself! Or provide feedback via ISSUES.
