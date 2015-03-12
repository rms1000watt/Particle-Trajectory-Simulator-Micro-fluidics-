from numpy import array, isnan
from ptspy.utilities.datahandler import chunks

class Data:
    """2D Vector field data object. 
    
    Configures the vector field data for interpolation and 
    data handling (Data.trace) and plotting vector fields 
    using pylab.quiver (Data.quiver)
    
    Attributes:
        quiver : 
    """
    def __init__(self,dataArray,XQuiverLength):
        """    
        Args:
            dataArray : the column vector from the .txt or .csv file
            XQuiverLength : the number of elements for the quiver in X direction
        """
        self.quiver = array(chunks(dataArray.tolist(),XQuiverLength))
        self.quiver[isnan(self.quiver)] = 0
        self.trace = dataArray
        self.trace[isnan(self.trace)] = 0
        self.trace = self.trace.tolist()