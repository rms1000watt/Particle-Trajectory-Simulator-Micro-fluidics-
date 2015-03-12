import numpy.ma as ma
from pylab import quiver
from numpy import zeros

class Plot:
    def __init__(self,plotTrajectory=True,plotFields=True,scaleX=1,scaleY=1):
        self.plotTrajectory = plotTrajectory
        self.plotFields = plotFields 
        self.scaleX = scaleX
        self.scaleY = scaleY
    
    def trajectory(self,plt,allData,particleList):
        if self.plotTrajectory:
            lineList = self.buildPlot(plt,allData,particleList)
            self.addData(lineList,particleList)
        
    def addData(self,lineList,particleList):        
        for ind,particle in enumerate(particleList):
            lineList[ind].set_data(particle.positionList)
        
    def buildPlot(self,plt,allData,particleList):        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlim(allData["X"].minValue, allData["X"].maxValue)
        ax.set_ylim(allData["Y"].minValue, allData["Y"].maxValue)
        pos1 = ax.get_position()  
#         pos2 = [pos1.x0+(pos1.width*self.scaleX*.5), pos1.y0+(pos1.height*self.scaleY*.5),  pos1.width*self.scaleX, pos1.height*self.scaleY]
        pos2 = [pos1.x0+((pos1.width - (pos1.width*self.scaleX))*.5), pos1.y0+((pos1.height - (pos1.height*self.scaleY))*.5),  pos1.width*self.scaleX, pos1.height*self.scaleY] 
        ax.set_position(pos2)
        title = str(len(particleList))+' Particle Trajectories'
        plt.title(title)
        plt.xlabel("X [m]")
        plt.ylabel("Y [m]")
        plt.grid()
        return self.buildLineList(ax,particleList)
    
    def buildLineList(self,axis,particleList):
        lineList, lineStyleList = [], []
        for ind,particle in enumerate(particleList):
            if particle.DEPFactor < 0:
                lineStyleList.append('b-')
            else:
                lineStyleList.append('r-')
        for i in range(len(particleList)):
            lineList.extend(axis.plot([],[],lineStyleList[i]))
        return lineList
    
    def vectorField(self,plt,X,Y,U,V,title):
        if self.plotFields:
            # Create mask corresponding to 0 fluid velocity values inside obstructions
            M = zeros([X.quiverLength,Y.quiverLength],dtype='bool')
            M = (U.quiver == 0)
            
            # Mask the obstructions in the fluid velocity vector field
            U.quiver = ma.masked_array(U.quiver,mask=M)
            V.quiver = ma.masked_array(V.quiver,mask=M)
            
            # Build and scale the plot
            fig = plt.figure()        
            ax = fig.add_subplot(111)
            ax.set_ylim(Y.minValue, Y.maxValue)
            ax.set_xlim(X.minValue, X.maxValue)
            pos1 = ax.get_position()  
            pos2 = [pos1.x0+((pos1.width - (pos1.width*self.scaleX))*.5), pos1.y0+((pos1.height - (pos1.height*self.scaleY))*.5),  pos1.width*self.scaleX, pos1.height*self.scaleY] 
            ax.set_position(pos2)
            title = title + ' Vector Field'        
            plt.title(title)
            plt.xlabel("X [m]")
            plt.ylabel("Y [m]")
            plt.grid()
            
            quiver(X.quiver,Y.quiver,U.quiver,V.quiver)        
        
        
    
                