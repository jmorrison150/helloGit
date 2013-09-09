import rhinoscriptsyntax as rs
import random
"""
Script written by Ezio Blasetti
Script copyrighted by algorithmicdesign.net
Script version Sunday, June 25, 2011 5:11:59 PM
###########################################################################################
This is a simple mesh navigation example.
It takes as an input a single mesh, a few attractors as points or curves and
a collection of points for the selection of vertices-agents
"""

def MeshVtxAdjacentVtxs (strMesh, index, blnAbsolutConnections=False, blnCreate=False): 
    """---------------------------------------------------------------------------------------------------------------------------------------
    MeshVtxAdjacentVtxs
    finds the adjecent vertices on a mesh for a given index of a vertex.
    written by Ezio Blasetti. Last Revision 062411.
    
    Syntax
    MeshVtxAdjacentVtxs (strMesh, index, blnAbsolutConnections, blnCreate)
    
    Parameters
    strMesh                       Required. String.  The identifier of a mesh object.
    index                         Required. Integer. The index of a vertex object inside the array returned from rs.MeshVertices method.
                                                     Use rs.MeshVertexCount for the length of that array.
    blnAbsolutConnections         Optional. Boolean. If True only the end points of the adjacent edges will be returned.
                                                     Note, if false, all the vertices of the adjacent faces will be returned.
    blnCreate                     Optional. Boolean. Create the adjacent points. If false, points are not created.
    
    Returns
    Array                         If blnCreate is equal to True , an array containing 3D adjacent points if successful.
    Array                         If blnCreate is equal to False, an array containing the indexes of the adjacent vetrices if successful.
    None                          If not successful, or on error.
    
    
    Example
    import rhinoscriptsyntax as rs
    strObject        = rs.GetObject("Select the mesh", 32)
    intRndVtxIndex   = 0
    arr              = MeshVtxAdjacentVtxs (strObject, intRndVtxIndex, True, True)
    ---------------------------------------------------------------------------------------------------------------------------------------"""
    """custom function"""
    #-----------------------------------------------------------------------------------------------------------------------------------------
    def CullDuplicates(seq, idfun=None):  
        # order preserving 
        if idfun is None: 
            def idfun(x): return x 
        seen = {} 
        result = [] 
        for item in seq: 
            marker = idfun(item) 
            if marker in seen: continue 
            seen[marker] = 1 
            result.append(item) 
        return result
    #-----------------------------------------------------------------------------------------------------------------------------------------
    MeshVtxAdjacentVtxs = []
    if rs.IsMesh(strMesh)==False : 
        print "strMesh is not an mesh"
        return None
    if type(index)==type("string"):
        print "index is not an integer"
        return None
    if type(index)==type(0.1): index = int(index)

    arrVertices     = rs.MeshVertices    (strMesh)
    arrFaceVertices = rs.MeshFaceVertices(strMesh)

    intCount = 0
    arrAdjacentVtxs = []
    for arrFace in arrFaceVertices:
        blnIsAdjacent = False
        for arrVtxIndex in arrFace:
            if arrVtxIndex == index :
                blnIsAdjacent = True
        if blnIsAdjacent :
            if blnAbsolutConnections :
                if arrFace[2]==arrFace[3] :
                    for arrVtxIndex in arrFace :
                        if arrVtxIndex != index :
                            arrAdjacentVtxs.append( arrVtxIndex)
                else :
                    if index == arrFace[0] :
                        arrAdjacentVtxs.append( arrFace[3] )
                        arrAdjacentVtxs.append( arrFace[1] )
                    elif index == arrFace[1] :
                        arrAdjacentVtxs.append( arrFace[0] )
                        arrAdjacentVtxs.append( arrFace[2] )
                    elif index == arrFace[2] :
                        arrAdjacentVtxs.append( arrFace[1] )
                        arrAdjacentVtxs.append( arrFace[3] )
                    elif index == arrFace(3) :
                        arrAdjacentVtxs.append( arrFace[2] )
                        arrAdjacentVtxs.append( arrFace[0] )
            else :
                for arrVtxIndex in arrFace :
                    if arrVtxIndex != index :
                        arrAdjacentVtxs.append( arrVtxIndex )
    if type(arrAdjacentVtxs) != type([]) : return None
    arrOrderAdjacentVtxs = CullDuplicates(arrAdjacentVtxs)
    if blnCreate :
        arrStrPts = []
        for arrVtxIndex in arrOrderAdjacentVtxs:
            rs.AddPoint ( arrVertices[arrVtxIndex] )
            arrStrPts.append( arrVertices[arrVtxIndex] )
        return arrStrPts
    else :
        return arrOrderAdjacentVtxs

def RenderAgentsOnMesh(strMesh, arrIndexes):
    arrVertices     = rs.MeshVertices(strMesh)
    arrVertexColors = []
    for i in range(len(arrVertices)):
        arrVertexColors.append( [255,255,255] )
    for index in arrIndexes:
        arrVertexColors[index] = [0,0,0]
    rs.MeshVertexColors (strMesh , arrVertexColors)

def Main():
    #SETUP
    #-------------------------------------------------------------------------------------------------------
    #select the mesh to work on ////////////////////////////////////////////////////////////////////
    strMesh         = rs.GetObject ("select mesh to work on", 32)   
    # store the mesh face vertices - we'll need it later to rebuild the mesh
    arrFaceVertices = rs.MeshFaceVertices(strMesh)
    #select the attractors points       ////////////////////////////////////////////////////////////////////
    attrs           = rs.GetObjects ("select the attractors for direction - either points or curves", 5)
    # here we need to translate the attractors (IDS of points and curves that the user gave us) to coordinates
    #--------------------------------------------------------------------------
    arrAttractors = []
    for attr in attrs:
        if rs.IsCurve(attr) :
            #if it is a curve - i need to find the closest point to the current agent
            #right now i'll set it up to array(0,0,0) and i'll replace those values in the do loop later
            arrAttractors.append([0,0,0])
        else : 
            arrAttractors.append( rs.PointCoordinates(attr) )
    #select the agents          ////////////////////////////////////////////////////////////////////
    arrStrPtAgents = rs.GetObjects ("select Agents to move on the mesh", 1) 
    dblStep        = rs.GetReal("please type the step size of the agents' deformation factor",1)
    # here we need to translate the agents (points that the user gave us
    # to vertices on the mesh....
    #--------------------------------------------------------------------------
    # start a new array same size as the agents-points - call it agentsOnmesh
    agentsOnMesh = []       
    # get the mesh vertices
    arrVTXS         = rs.MeshVertices (strMesh)
    # loop throught the points-agents that the user gave us,
    for strPtAgent in arrStrPtAgents:
        arrPtAgent = rs.PointCoordinates(strPtAgent)
        # use point array closest point to determine which mesh vertex is closest to the current agent-point
        # store that index from pointarrayclosestpoint in the agentsOnMesh(i)       
        agentsOnMesh.append( rs.PointArrayClosestPoint(arrVTXS,arrPtAgent) )
        # end loop  
    #-------------------------------------------------------------------------------------------------------
    #RUN
    #-------------------------------------------------------------------------------------------------------    
    #loop for number of steps
    for e in range(100):
        #   get the mesh vertices of the current mesh arrVTXS
        arrVTXS = rs.MeshVertices (strMesh)
        #   start a arrNEWVTXS and make it equal to arrVTXS (for now)
        arrNEWVTXS = arrVTXS[:]
        #   i loop through each index in agentsOnMesh
        i = 0
        for agentOnMesh in  agentsOnMesh:
            # MOVE THE MESH POINT --------------------------------------------------------------------------
            j = 0
            for attr in attrs :
                if rs.IsCurve(attr) :
                    #here we find the closestpoint on the curve attractors from the current agent
                    dblParam = rs.CurveClosestPoint(attr,arrVTXS[agentOnMesh])
                    arrAttractors[j] = rs.EvaluateCurve(attr,dblParam)
                    j += 1
            ClosestAttIndex = rs.PointArrayClosestPoint(arrAttractors,arrVTXS[agentOnMesh])
            # make a vector from arrVTXS(agentsOnMesh(i)) towards the closest attractor arrAttractors(ClosestAttIndex)
            arrVector = rs.VectorCreate(arrAttractors[ClosestAttIndex], arrVTXS[agentOnMesh])
            arrVector = rs.VectorUnitize(arrVector)
            arrVector = rs.VectorScale(arrVector, dblStep)
            # add the vector to the arrVTXS(agentsOnMesh(i)) and store it in arrNEWVTXS(agentsOnMesh(i))
            arrNEWVTXS[agentOnMesh] = rs.PointAdd(arrVTXS[agentOnMesh], arrVector)
            # MOVE THE AGENT      --------------------------------------------------------------------------
            # get the adjacent mesh vtx indexes from MeshVtxAdjacentVtxs
            arrNeighborIndexes = MeshVtxAdjacentVtxs (strMesh, agentOnMesh, False, False)
            # choose which vtx to "move" to, and store it in agentsOnMesh(i)
            rnd = random.random()
            agentsOnMesh[i] = arrNeighborIndexes[int((rnd)*(len(arrNeighborIndexes)-1))]
            i += 1
        #   add a new mesh in the document using arrNEWVTXS
        strNewMesh = rs.AddMesh(arrNEWVTXS,arrFaceVertices)
        RenderAgentsOnMesh(strNewMesh, agentsOnMesh)
        #   delete the old one 
        rs.DeleteObject(strMesh)
        #   replace the ID of old mesh with the NEW ID
        strMesh = strNewMesh

Main()