import rhinoscriptsyntax as rs
__commandname__ = "annotateCurveEndPoints"

def AnnotateCurveEndPoints():
    print "annotateCurveEndPoints"
    #Annotates the endpoints of curve objects. If the curve is closed then only the starting point is annotated.
    
    # get the curve object
    objectId = rs.GetObject("Select curve", rs.filter.curve)
    if objectId is None: return

    # Add the first annotation
    point = rs.CurveStartPoint(objectId)
    rs.AddPoint(point)
    #textDot is out of scale
    #rs.AddTextDot(point, point)
    txtString = meters(point)
    rs.AddText(txtString, point, 1000 )
    print (point.X + point.Y + point.Z)

    # Add the second annotation
    if not rs.IsCurveClosed(objectId):
        point = rs.CurveEndPoint(objectId)
        rs.AddPoint(point)
        txtString = meters(point)
        rs.AddText(txtString, point, 1000 )
        #rs.AddTextDot(point, point)
        #text here too

def meters(point):
    txtString = "(%s, %s, %s)" % (int(point.X/1000), int(point.Y/1000), int(point.Z/1000))
    return txtString
def millimeters(point):
    txtString = "(%s, %s, %s)" % (int(point.X), int(point.Y), int(point.Z))    
    return txtString

def RunCommand(is_interactive):
    print "RunCommand"
    AnnotateCurveEndPoints()
    # Annotate the endpoints of curve objects
