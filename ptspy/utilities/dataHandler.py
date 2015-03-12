import json

from ptspy.physical import Fluid
from ptspy.physical import Forces
from ptspy.physical import Particle
from ptspy.physical import PhysicalConstants
from ptspy.simulator import Time
from ptspy.plot import Plot

from numpy import array
from numpy import isnan
from numpy import zeros
from numpy import insert

class Data:
    """2D Vector field data object. 
    
    Attributes:
        quiver : numpy.array used for plotting vector fields
        trace : list used for interpolation and data handling
    """
    def __init__(self,dataArray,XQuiverLength):
        """    
        Args:
            dataArray : numpy.array of the column vectors from the .txt or .csv file
            XQuiverLength : integer of the number of elements for the quiver in X direction
        """
        self.quiver = array(chunks(dataArray.tolist(),XQuiverLength))
        self.quiver[isnan(self.quiver)] = 0
        self.trace = dataArray
        self.trace[isnan(self.trace)] = 0
        self.trace = self.trace.tolist()
        
def getAllData(configFile):
    print "1. Importing and Configurating Data"
    config = jsonFromFile(configFile)
    return setupData(config)

def setupData(cf):
    allData = {}

    allData["X"],allData["Y"],allData["U"],allData["V"],allData["gradE2X"],allData["gradE2Y"],allData["coordinates"],allData["velocity"],allData["gradE2"] = getVectorFieldData(cf["file_locations"]["vectorFieldFile"],cf)
    
    particleData = dataFromFile(cf["file_locations"]["particleFile"])
    allData["particleList"] = buildParticleList(particleData,cf)
    
    fluidData = cf["fluid_data"]
    allData["fluid"] = Fluid(
        density = fluidData["density"],
        viscosity = fluidData["viscosity"],
        name = fluidData["name"],
        velocity = allData["velocity"],
        relativePermittivity = fluidData["relativePermittivity"])

    physicalConstantsData = cf["physicalConstants_data"]
    allData["physicalConstants"] = PhysicalConstants(
        gravitationalAcceleration = physicalConstantsData["gravitationalAcceleration"],
        boltzmannConstant = physicalConstantsData["boltzmannConstant"],
        vacuumPermittivity = physicalConstantsData["vacuumPermittivity"])

    forcesData = cf["forces_data"]
    allData["forces"] = Forces(
        physicalConstants = allData["physicalConstants"],
        includeGravitational = forcesData["includeGravitational"],
        includeStokes = forcesData["includeStokes"],
        includeBuoyant = forcesData["includeBuoyant"],
        includeDEP = forcesData["includeDEP"])

    timeData = cf["time_data"]
    allData["time"] = Time(
        start = timeData["start"],
        stop = timeData["stop"],
        step = timeData["step"])

    allData["repeatX"] = cf["config"]["repeatX"]
    allData["repeatY"] = cf["config"]["repeatY"]

    plotData = cf["plot_data"]
    allData["plot"] = Plot(
        plotTrajectory = plotData["plotTrajectory"] == "True",
        plotFields = plotData["plotFields"] == "True",
        scaleX = plotData["scaleX"],
        scaleY = plotData["scaleY"])

    print "1. Done"
    return allData

def buildParticleList(particleData,config):
    # Can modify this function if you want 1000+ particles
    particleList = []
    for index,arr in enumerate(particleData):
        particleList.append(Particle(
            position = [arr[0],arr[1]],
            velocity = [arr[2],arr[3]],
            acceleration = [arr[4],arr[5]],
            radius = arr[6], 
            density = arr[7],
            mass = arr[8],        
            DEPFactor = arr[9]*config["electrode_data"]["voltageScale"],
            name = "particle"+str(index)))
    return particleList

def getVectorFieldData(fileName,config):
    dupe = config["config"]["multiplyFieldX"]
    scaleX, scaleY = config["fluid_data"]["scaleX"], config["fluid_data"]["scaleY"]
    fieldData = dataFromFile(fileName)
    X,Y,U,V,gradE2X,gradE2Y = buildData(fieldData)
    for i in range(0,dupe):
        doubleFieldXDirection(X,Y,U,V,gradE2X,gradE2Y)
    coordinates, velocity, gradE2 = completeData(X,Y,U,V,gradE2X,gradE2Y,scaleX,scaleY)
    return X,Y,U,V,gradE2X,gradE2Y,coordinates,velocity,gradE2

def dataFromFile(fileName):
    """Imports data from file with comma separated delimiter (imports .csv or .txt files)
    
    Args:
        fileName : string of full file name with path (eg. '/Users/YOURUSERNAME/Documents/FILENAME.txt')
    """
    allData = []
    with open(fileName, 'r') as file1:
        for line in file1:
            if line[0] != '%':
                lineFloat = [float(num) for num in line.split(',')]
                allData.append(lineFloat)
    return array(allData)

def jsonFromFile(fileName):
    with open(fileName, 'r') as inFile:
        return json.load(inFile)

def buildData(allData):
    """Takes allData from the .txt or .csv file and creates an object for each column for particle traces and quiver plots
    
    Outputs an object for each column
    
    Args:
        allData : all the data from the .txt or .csv file imported from rypy.dataFromFile()
    """
    holdClasses = []
    XQuiverLength, YQuiverLength = quiverLengths(allData.T[0])    
    for i in range(len(allData[0])):
        holdClasses.append(Data(allData.T[i],XQuiverLength))
    buildParameters(holdClasses[0],holdClasses[1],XQuiverLength,YQuiverLength)
    return holdClasses

def completeData(X,Y,U,V,gradE2X,gradE2Y,scaleX,scaleY):
    # Define coordinates and velocity for particle flow traces
    coordinates = array([X.trace,Y.trace])
    velocity = array([U.trace,V.trace])
    gradE2 = array([gradE2X.trace,gradE2Y.trace])
    
    velocity[0][:] = velocity[0][:]*scaleX
    velocity[1][:] = velocity[1][:]*scaleY
    U.quiver[:] = U.quiver[:]*scaleX
    V.quiver[:] = V.quiver[:]*scaleY
        
    # Transpose fields for easier data handling
    velocityTranspose = velocity.T
    gradE2Transpose = gradE2.T
    return coordinates, velocityTranspose, gradE2Transpose

def buildParameters(X,Y,XQuiverLength,YQuiverLength):
    """Builds useful parameters from X and Y grid points for X and Y objects only
    
    Args:
        X : Data class for X direction 
        Y : Data class for Y direction
        XQuiverLength : integer of elements in X direction
        YQuiverLength : integer of elements in Y direction
    """
    X.quiverLength = XQuiverLength
    X.minValue = min(X.trace)    
    X.maxValue = max(X.trace)
    X.gridSpacing = abs(X.trace[1]-X.trace[0])
    Y.quiverLength = YQuiverLength
    Y.minValue = min(Y.trace)
    Y.maxValue = max(Y.trace)
    Y.gridSpacing = abs(Y.trace[X.quiverLength]-Y.trace[0])
    
def doubleFieldXDirection(X,Y,U,V,gradE2X,gradE2Y):
    objectsList = [Y,U,V,gradE2X,gradE2Y]
    newQList = []
    locationIndexes = zeros(X.quiverLength,int)+X.quiverLength    
    for i in range(len(objectsList)):
        newQList.append(objectsList[i].quiver)
        newQList[i] = insert(newQList[i],locationIndexes,newQList[i],axis=1)
    for i in range(len(objectsList)):
        objectsList[i].quiver = newQList[i]
        objectsList[i].trace = newQList[i].flatten()

    #this for X
    XnewQ = X.quiver    
    locationIndexes = zeros(X.quiverLength,int)+X.quiverLength
    XnewQ = insert(XnewQ,locationIndexes,XnewQ+(X.maxValue+X.minValue),axis=1)   
    X.quiver = XnewQ
    X.trace = XnewQ.flatten()
    xquiverlength,yquiverlength = quiverLengths(X.trace)
    buildParameters(X,Y,xquiverlength,yquiverlength)

def quiverLengths(xTrace):
    """Determines the length of the X and Y coordinates for quiver plots
    
    Args:
        xTrace : numpy.array of Trace of X values
    """
    xquiverlength = 0
    firstNum = xTrace[0]
    for i in range(1,len(xTrace)):
        if xTrace[i] == firstNum:
            xquiverlength = i
            break
    if xquiverlength > 0:
        yquiverlength = len(xTrace)/xquiverlength
    else:
        yquiverlength = 0
    return xquiverlength, yquiverlength

def chunks(List,elements):
    """Takes a List and creates a nested List depending on the number of 'elements' you want in each nested list.
    
    chunks([1,2,3,4,5,6],3) => [[1,2,3],[4,5,6]]
    chunks([1,2,3,4,5,6],2) => [[1,2],[3,4],[5,6]]
    chunks([1,2,3,4,5,6],1) => [[1],[2],[3],[4],[5],[6]]
    
    Args:
        List : list or list variable
        elements : integer length for each nested list 
    """
    return [List[i:i+elements] for i in range(0, len(List), elements)]
       