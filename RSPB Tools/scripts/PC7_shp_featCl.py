## To convert a postcode field to 7 characters, upper case
## User specifies a shapefile or feature class 
## A new field "PC7" is added to the file with the 7 character postcode

## function to return 7 character postcode
def pc_7_char(pc):
    import re

    # remove all spaces
    pc_chars = re.sub('[\s+]', '', pc)

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
pc_fieldname = arcpy.GetParameterAsText(1)

# add new "PC7" field to contain converted postcode
arcpy.AddField_management(pc_file, "PC7", "TEXT", field_length = 7)
cursor = arcpy.UpdateCursor(pc_file)
for row in cursor:
    this_pc = row.getValue(pc_fieldname)
    pc7 = pc_7_char(this_pc)
    row.setValue("PC7", pc7)
    cursor.updateRow(row)

# Delete cursor amd row objects to remove locks on the data
del cursor
del row
