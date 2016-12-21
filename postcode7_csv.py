## User specifies a csv file with postcodes to standardise to 7 characters
## A new column is added to the csv file

## function to return 7 character postcode
def pc_7_char(pc):
    import string

    # remove all whitespace
    for whitespace_character in string.whitespace:
        pc_chars = pc.replace(whitespace_character, '')

    #separate incode from outcode and pad outcode to 4 characters
    incode = pc_chars[-3:].upper() # last 3 characters and ensure upper case
    outcode = '{:<4}'.format(pc_chars[:-3].upper()) # may be 2-4 characters
    pc_7 = outcode+incode
    return pc_7


import csv
import arcpy
import os

#get parameters
pc_file = arcpy.GetParameterAsText(0)
pc_col = arcpy.GetParameter(1)
header = arcpy.GetParameter(2)

# open csv file
c = open(pc_file, 'r')
r = csv.reader(c)

# create temporary file for adding new column
filepath = os.path.dirname(pc_file)  #get path
filename = os.path.basename(pc_file) #get filename
tempfile = filepath+"/"+"temp_"+filename
outf = open(tempfile, 'w') 
wr = csv.writer(outf, lineterminator='\n')

pc_col = int(pc_col - 1)  # column numbers start from 0
all =[]

# process first row according to whether it is a header or not
row0 = r.next()
if header:  # add heading for new column
    row0.append('pc_formatted')
else:       # apply pc_7_char to first row
    this_pc = row0[pc_col]
    pc7 = pc_7_char(this_pc)
    row0.append(pc7)
all.append(row0)

# apply pc_7_char to each postcode
for item in r:
    this_pc = item[pc_col]
    pc7 = pc_7_char(this_pc)
    item.append(pc7)
    all.append(item)

wr.writerows(all)
c.close()
outf.close()
os.remove(pc_file)
os.rename(tempfile, pc_file)
