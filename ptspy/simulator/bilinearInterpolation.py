from numpy import isnan
from numpy import array
from math import floor
from math import ceil
from ptspy.physical.particle import Particle

class BilinearInterpolation:
    def __init__(self,X=array([0,0]),Y=array([0,0]),coordinates=array([0,0]),
                    velocityTranspose=array([0,0]),gradESquaredTranspose=array([0,0]),repeatX=True,repeatY=False):
        """Bilinear Interpolation class for bilinear interpolation including averageVelocity
        
        Args:
            X : X object for grid points
            Y : Y object for grid points
            coordinates : np.array([[x1,x2,x3,...],[y1,y2,y3,...]])
            velocityTranspose : np.array([[x1,y1],[x2,y2],[x3,y3]...])
            fluid : fluid object
            forces : forces object
        """
        self.X = X
        self.Y = Y
        self.coordinates = coordinates
        self.coordinatesTranspose = coordinates.T
        self.velocityTranspose = velocityTranspose
        self.gradESquaredTranspose = gradESquaredTranspose
        self.repeatX = repeatX
        self.repeatY = repeatY
        #self.time = time

    def checkPointVsBoundaries(self,point=array([0,0]),obj=1):
        """Checks if point is within the boundaries for interpolation
        
        Args:
            point : numpy.array([x',y'])
            obj : pass the Particle object so it can be repeated if it reaches the end of the channel
        """        
        if point[0] > self.X.maxValue:
            if self.repeatX:
                point[0] = self.X.minValue
                if isinstance(obj,Particle):
                    obj.repeatCnt +=1
            else:
                point[0] = self.X.maxValue-(1e-5*self.X.maxValue)
        if point[0] < self.X.minValue:
            if self.repeatX:
                point[0] = self.X.maxValue
                if isinstance(obj,Particle):
                    obj.repeatCnt +=1
            else:
                point[0] = self.X.minValue
                
                
        if point[1] > self.Y.maxValue:
            if self.repeatY:
                point[1] = self.Y.minValue
            else:
                point[1] = self.Y.maxValue-(1e-5*self.Y.maxValue)    
        if point[1] < self.Y.minValue:
            if self.repeatY:
                point[1] = self.Y.maxValue
            else:
                point[1] = self.Y.minValue
        return point
        
    def buildNearestIndexes(self,point):
        i = (self.X.quiverLength-1)*(point[0]-self.X.minValue)/(self.X.maxValue-self.X.minValue)
        j = (self.Y.quiverLength-1)*(point[1]-self.Y.minValue)/(self.Y.maxValue-self.Y.minValue)
        i0, i1 = int(floor(i)),int(ceil(i))  
        j0, j1 = int(floor(j)),int(ceil(j))
        if i0 == i1:
            i0, i1 = self.fixIndexes(i0,i1)
        if j0 == j1:
            j0, j1 = self.fixIndexes(j0,j1)
        ind00 = self.ijToFlatIndex(i0,j0)
        ind10 = self.ijToFlatIndex(i1,j0)
        ind01 = self.ijToFlatIndex(i0,j1)
        ind11 = self.ijToFlatIndex(i1,j1)
        return [ind00,ind10,ind01,ind11]
    
    def ijToFlatIndex(self,i,j):
        return i+(j*self.X.quiverLength)  
    
    def interpolate(self,point,indexList,fieldName='none'):
        if fieldName=='none':
            print 'no interpolation occurring\nreturning array([0,0])\n'
            return array([0,0])
        if fieldName=='velocity':
            return self.bilinearInterpolation(point,indexList,self.velocityTranspose)
        if fieldName=='Efield':
            return self.bilinearInterpolation(point,indexList,self.gradESquaredTranspose)
            
    def bilinearInterpolation(self,point,indexes,fieldTranspose):
        """Bilinear interpolation of a 2D field numpy.array([[x1,y1],[x2,y2],[x3,y3],...]) at point within a rectangular grid
        
        Args:
            point : numpy.array([x',y'])
            indexes : indexes of nearest 4 points
            coordinates : coordinates built from X and Y objects
            velocityTranspose : transposed velocity build from U and V objects
        """
        x,y = point
        x1,x2 = self.coordinates[0][indexes[0]],self.coordinates[0][indexes[1]]
        y1,y2 = self.coordinates[1][indexes[1]],self.coordinates[1][indexes[2]]
        f11 = fieldTranspose[indexes[0]]
        f21 = fieldTranspose[indexes[1]]
        f12 = fieldTranspose[indexes[2]]
        f22 = fieldTranspose[indexes[3]]
        return 1/((x2-x1)*(y2-y1))*(f11*(x2-x)*(y2-y)+f21*(x-x1)*(y2-y)+f12*(x2-x)*(y-y1)+f22*(x-x1)*(y-y1))
            
    def fixIndexes(self,ind1,ind2):
        """Fixes indexes if they're equal to each other. (indexes need to be different so bilinear Interpolation works)
        
        Note : ind1 < ind2
        
        Args:        
            ind1 : first index (eg. indY1 or indX1)
            ind2 : second index (eg. indY2 or indX2)
        """
        if ind1 > 0:
            ind1 -= 1
        else:
            ind2 += 1
        return ind1,ind2
    