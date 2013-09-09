__commandName__ = "exportCSV"
# Export the coordinates of point and point cloud objects to a text file.
import rhinoscriptsyntax as rs


def ExportPoints():
    #Get the points to export
    objectIds = rs.GetObjects("Select Points",rs.filter.point | rs.filter.pointcloud,True,True)
    if( objectIds==None ): return

    #Get the filename to create
    filter = "Comma Seperated Values (*.csv)|*.csv|All Files (*.*)|*.*||"
    filename = rs.SaveFileName("Save point coordinates as", filter)
    if( filename==None ): return
    
    file = open(filename, "w")
    for id in objectIds:
        #process point clouds
        if( rs.IsPointCloud(id) ):
            points = rs.PointCloudPoints(id)
            for pt in points:
                file.writelines(str(pt))
        elif( rs.IsPoint(id) ):
            point = rs.PointCoordinates(id)
            file.writelines(str(point))
            file.write('\n')
    file.close()

def RunCommand(is_interactive):
    ExportPoints()