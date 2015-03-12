from numpy import array

class TrilinearInterpolation:
    def __init__(self,X=array([0,0,0]),Y=array([0,0,0]),Z=array([0,0,0]),coordinates=array([0,0,0]),
                    velocityTranspose=array([0,0,0]),gradESquaredTranspose=array([0,0,0])):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.coordinates = coordinates
        self.velocityTranspose = velocityTranspose
        self.gradESquaredTranspose = gradESquaredTranspose
        
    def buildNearestIndexes3D(self,point):
        i = (self.X.quiverLength-1)*(point[0]-self.X.minValue)/(self.X.maxValue-self.X.minValue)
        j = (self.Y.quiverLength-1)*(point[1]-self.Y.minValue)/(self.Y.maxValue-self.Y.minValue)
        k = (self.Z.quiverLength-1)*(point[2]-self.Z.minValue)/(self.Z.maxValue-self.Z.minValue)
        i0, i1 = int(floor(i)),int(ceil(i))  
        j0, j1 = int(floor(j)),int(ceil(j))
        k0, k1 = int(floor(k)),int(ceil(k))         
        if i0 == i1:
            i0,i1 = self.fixIndexes(i0,i1)
        if j0 == j1:
            j0,j1 = self.fixIndexes(j0,j1)
        if k0 == k1:
            k0,k1 = self.fixIndexes(k0,k1)
        return [i0,i1,j0,j1,k0,k1]
        
    def fixIndexes(self,ind1,ind2):
        if ind1 > 0:
            ind1 -= 1
        else:
            ind2 += 1
        return ind1,ind2
        
    def trilinearInterpolation(self,point,indexList):
        i0,i1,j0,j1,k0,k1 = indexList
        x,y,z = point        
        ind000 = self.ijkToFlatIndex(i0,j0,k0)
        ind100 = self.ijkToFlatIndex(i1,j0,k0)
        ind010 = self.ijkToFlatIndex(i0,j1,k0)
        ind110 = self.ijkToFlatIndex(i1,j1,k0)
        ind001 = self.ijkToFlatIndex(i0,j0,k1)
        ind101 = self.ijkToFlatIndex(i1,j0,k1)
        ind011 = self.ijkToFlatIndex(i0,j1,k1)
        ind111 = self.ijkToFlatIndex(i1,j1,k1)
        x0, x1 = self.coordinates[0][ind000],self.coordinates[0][ind100]
        y0, y1 = self.coordinates[1][ind000],self.coordinates[1][ind010]
        z0, z1 = self.coordinates[2][ind000],self.coordinates[2][ind001]
        xd = (x-x0)/(x1-x0)
        yd = (y-y0)/(y1-y0)
        zd = (z-z0)/(z1-z0)
        f000 = self.velocityTranspose[ind000]
        f100 = self.velocityTranspose[ind100]
        f010 = self.velocityTranspose[ind010]
        f110 = self.velocityTranspose[ind110]
        f001 = self.velocityTranspose[ind001]
        f101 = self.velocityTranspose[ind101]
        f011 = self.velocityTranspose[ind011]
        f111 = self.velocityTranspose[ind111]
        f00 = f000*(1-xd)+(f100*xd)
        f10 = f010*(1-xd)+(f110*xd)
        f01 = f001*(1-xd)+(f101*xd)
        f11 = f011*(1-xd)+(f111*xd)
        f0 = f00*(1-yd)+(f10*yd)
        f1 = f01*(1-yd)+(f11*yd)
        return f0*(1-zd)+(f1*zd)
    
    def ijkToFlatIndex(self,i,j,k):
        return i+(j*self.X.quiverLength)+(k*self.X.quiverLength*self.Y.quiverLength)