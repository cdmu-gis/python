import arcpy
from arcpy import env


# Parameters

workspace = arcpy.GetParameter(0)
raster = arcpy.GetParameter(1)
name = arcpy.GetParameterAsText(2)

arcpy.env.workspace = workspace
name2 = name[:-4]
print(name2)

arcpy.CopyRaster_management(raster,name)