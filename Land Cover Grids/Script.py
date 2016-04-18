# The template mxd and spreadsheets to use can be found in the following location: S:\DataUnit\DptShare\Consultancy\Lodge\ConSci\DaveBuckingham\NEW_METHOD_Dec_2015\Template
# Open the Template.mxd and save a copy into your new workspace.
# The list of grid refs to use must be stored in a spreadsheet with column headings ‘Square_ID’ and ‘Grid_Ref’. Use the ‘Input_Data’ spreadsheet as a template. Once this has been saved in your workspace, add ‘Sheet1$’ from the spreadsheet into the mxd and save a copy.
# Enter your workspace into the workspace variable at the top of the script.
# Copy the entire script and run it in the python shell within the mxd. Once the script has finished running, the layers that end in ‘Dissolve’ will contain the % of each land cover category for each buffer – there should be 10 in total.
# The .dbf file for each of these layers can be opened in excel. Open the Output_Data spreadsheet and copy the data from each of the .dbf files above into the relevant tab in the Output_Data spreadsheet and save a copy.
# note that the dissolve stat fields in this script will need to be renamed before running the script, they don't currently fit the  lcm data


#define workspace
workspace = r""



import arcpy

arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True
data = "Sheet1$"


# Produce shapefile for zero buffer (join to grid layer and export)

join_table = data
output_file = "Zero"
arcpy.AddJoin_management("tblGrid1km_region", "GRIDREF1KM", join_table, "Grid_Ref", "KEEP_COMMON")
arcpy.FeatureClassToFeatureClass_conversion("tblGrid1km_region", arcpy.env.workspace, output_file)
arcpy.RemoveJoin_management ("tblGrid1km_region")
arcpy.RepairGeometry_management ("Zero") 




# Produce 1, 2, 5 and 10km square buffers on all squares

buffer_list = ["1 kilometers", "2 kilometers", "5 kilometers", "10 kilometers"]
name_lookup = {"1 kilometers":"One", "2 kilometers":"Two", "5 kilometers":"Five", "10 kilometers":"Ten"}

for buffer_distance in buffer_list:
	name = name_lookup.get(buffer_distance)
	arcpy.Buffer_analysis ("Zero", name, buffer_distance, "", "", "", "", "GEODESIC")
	arcpy.RepairGeometry_management (name)
	name2 = name + "_Buffer"
	arcpy.MinimumBoundingGeometry_management(name, name2, "ENVELOPE")
	arcpy.RepairGeometry_management (name2)





# Perform intersect to produce list of 1km grid refs within each square ID, for each buffer

squares_list = ["Zero", "One_Buffer", "Two_Buffer", "Five_Buffer", "Ten_Buffer"]
for square in squares_list:
	output = square + "_Intersect"
	arcpy.Intersect_analysis(["GB_1kmGrid_Points", square], output, "NO_FID")
	arcpy.RepairGeometry_management (output)




# For each intersect layer, use the LCM 2000 and 2007 summaries to calculate the total of each class for each square ID

intersect_list = ["Zero_Intersect", "One_Buffer_Intersect", "Two_Buffer_Intersect", "Five_Buffer_Intersect", "Ten_Buffer_Intersect"]
for intersect in intersect_list:
	arcpy.AddJoin_management(intersect, "GRIDREF1KM", "LCM20001kmSummariesGB_region", "GRIDREF1KM", "KEEP_COMMON")
	output = intersect + "_Join_2000"
	arcpy.FeatureClassToFeatureClass_conversion(intersect, arcpy.env.workspace, output)
	arcpy.RemoveJoin_management (intersect)
	arcpy.RepairGeometry_management (output)
	arcpy.AddJoin_management(intersect, "GRIDREF1KM", "LCM2007_summary", "GRIDREF1KM", "KEEP_COMMON")
	output2 = intersect + "_Join_2007"
	arcpy.FeatureClassToFeatureClass_conversion(intersect, arcpy.env.workspace, output2)
	arcpy.RemoveJoin_management (intersect)
	arcpy.RepairGeometry_management (output2)




# Perform dissolve to aggregate values based on square ID

LCM2000_layers = ["Zero_Intersect_Join_2000", "One_Buffer_Intersect_Join_2000", "Two_Buffer_Intersect_Join_2000", "Five_Buffer_Intersect_Join_2000", "Ten_Buffer_Intersect_Join_2000"]
statistical_fields = [["LCM20001_2", "MEAN"], ["LCM20001_3", "MEAN"], ["LCM20001_4", "MEAN"], ["LCM20001_5", "MEAN"], ["LCM20001_6", "MEAN"], ["LCM20001_7", "MEAN"], ["LCM20001_8", "MEAN"], ["LCM20001_9", "MEAN"], ["LCM2000_10", "MEAN"], ["LCM2000_11", "MEAN"], ["LCM2000_12", "MEAN"], ["LCM2000_13", "MEAN"], ["LCM2000_14", "MEAN"], ["LCM2000_15", "MEAN"], ["LCM2000_16", "MEAN"], ["LCM2000_17", "MEAN"], ["LCM2000_18", "MEAN"], ["LCM2000_19", "MEAN"], ["LCM2000_20", "MEAN"], ["LCM2000_21", "MEAN"], ["LCM2000_22", "MEAN"], ["LCM2000_23", "MEAN"], ["LCM2000_24", "MEAN"], ["LCM2000_25", "MEAN"], ["LCM2000_26", "MEAN"], ["LCM2000_27", "MEAN"]]
for layer in LCM2000_layers:
	output = layer + "_Dissolve"
	arcpy.Dissolve_management(layer, output, "Sheet1__Sq", statistical_fields)
LCM2007_layers = ["Zero_Intersect_Join_2007", "One_Buffer_Intersect_Join_2007", "Two_Buffer_Intersect_Join_2007", "Five_Buffer_Intersect_Join_2007", "Ten_Buffer_Intersect_Join_2007"]
statistical_fields2 = [["LCM2007__5", "MEAN"], ["LCM2007__6", "MEAN"], ["LCM2007__7", "MEAN"], ["LCM2007__8", "MEAN"], ["LCM2007__9", "MEAN"], ["LCM2007_10", "MEAN"], ["LCM2007_11", "MEAN"], ["LCM2007_12", "MEAN"], ["LCM2007_13", "MEAN"], ["LCM2007_14", "MEAN"], ["LCM2007_15", "MEAN"], ["LCM2007_16", "MEAN"], ["LCM2007_17", "MEAN"], ["LCM2007_18", "MEAN"], ["LCM2007_19", "MEAN"], ["LCM2007_20", "MEAN"], ["LCM2007_21", "MEAN"], ["LCM2007_22", "MEAN"], ["LCM2007_23", "MEAN"], ["LCM2007_24", "MEAN"], ["LCM2007_25", "MEAN"], ["LCM2007_26", "MEAN"], ["LCM2007_27", "MEAN"]]
for layer2 in LCM2007_layers:
	output2 = layer2 + "_Dissolve"
	arcpy.Dissolve_management(layer2, output2, "Sheet1__Sq", statistical_fields2)