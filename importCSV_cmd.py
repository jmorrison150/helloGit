# Import points from a CSV file
import rhinoscriptsyntax as rs
__commandname__ = "importCSV"


def ImportPoints():
    #prompt the user for a file to import
    filter = "Comma Seperated Values (*.csv)|*.csv|All Files (*.*)|*.*||"
    filename = rs.OpenFileName("Open Point File", filter)
    if not filename: return
    
    #read each line from the file
    file = open(filename, "r")
    contents = file.readlines()
    file.close()

    # local helper function
    def __point_from_string(text):
        items = text.strip("()\n").split(",")
        x = float(items[0])
        y = float(items[1])
        z = float(items[2])
        return x, y, z

    contents = [__point_from_string(line) for line in contents]
    rs.AddPoints(contents)



def RunCommand(is_interactive):
    ImportPoints()
    return 0