from numpy import array
from numpy import pi
from ptspy.simulator.bilinearInterpolation import BilinearInterpolation
from ptspy.simulator.trilinearInterpolation import TrilinearInterpolation

class RungeKuttaIntegrator:
    """2nd Order Runge Kutta Integrator for specific Objects (Tracker,Particle,ParticleAdvanced)
    
    Methods:
        tracker : Tracker object with only velocity interpolation
        particle : Particle object with stokes and gravitational forces
        particleAdvanced : Particle object with stokes, gravitational, and buoyant forces
    
    Attributes:        
        X : X object data
        Y : Y object data
        coordinates : np.array([[x1,x2,x3,...],[y1,y2,y3,...]])
        velocityTranspose : np.array([[x1,y1],[x2,y2],[x3,y3]...])
        dt : time step value
    """
    def __init__(self,X,Y,Z=array([0,0,0]),coordinates=array([0,0]),velocityTranspose=array([0,0]),dt=.1,gradESquaredTranspose=array([0,0]),fluid=1,forces=1,physConsts=1,repeatX=True,repeatY=False):
        self.dt = dt
        rx = (repeatX == "True" or repeatX == True) 
        ry = (repeatY == "True" or repeatY == True)
        self.BI = BilinearInterpolation(X,Y,coordinates,velocityTranspose,gradESquaredTranspose,repeatX=rx,repeatY=ry)
        self.TI = TrilinearInterpolation(X,Y,Z,coordinates,velocityTranspose,gradESquaredTranspose)
        self.fluid = fluid
        self.forces = forces
        self.physConsts = physConsts
        
    def tracker(self,tracker):
        """Does not include any force calculations, only velocity tracing"""
        #avgVel = self.BI.averageVelocity(tracker.position)
        tracker.position = self.BI.checkPointVsBoundaries(point=tracker.position)
        nearestIndexes = self.BI.buildNearestIndexes(tracker.position)
        avgVel = self.BI.interpolate(point=tracker.position,indexList=nearestIndexes,fieldName='velocity')        
        posTmp = tracker.position+avgVel*self.dt/2.
        
        posTmp = self.BI.checkPointVsBoundaries(point = posTmp)
        nearestIndexes = self.BI.buildNearestIndexes(posTmp)
        avgVelTmp = self.BI.interpolate(point=posTmp,indexList=nearestIndexes,fieldName='velocity')         
        
        #avgVelTmp = self.BI.averageVelocity(posTmp)
        return tracker.position+avgVelTmp*self.dt

    def particle(self,particle):
        """2nd order Runge-Kutta integrator for a particle
        
        Args:
            particle : Particle object
            fluid : Fluid object
            forces : Forces object
        """
        radius = particle.radius
        mass = particle.mass
        DEPFactor = particle.DEPFactor
        viscosity = self.fluid.viscosity
        relativePermittivity = self.fluid.relativePermittivity
        chkPvsBnd = self.BI.checkPointVsBoundaries
        chkPvsTV = self.checkParticleVsTerminalVelocity
        nearInds = self.BI.buildNearestIndexes
        interp = self.BI.interpolate
        stokes = self.forces.stokes
        DEP = self.forces.DEP
        dt = self.dt
        
        nearestIndexes = nearInds(particle.position)
        avgVel = interp(point=particle.position,indexList=nearestIndexes,fieldName='velocity')
        avgEField = interp(point=particle.position,indexList=nearestIndexes,fieldName='Efield')
        
        particle.velocity = chkPvsTV(particleVelocity=particle.velocity,fluidVelocity=avgVel
                                            ,DEPFactor=DEPFactor,radius=radius,Efield=avgEField)
        relativeVel = avgVel - particle.velocity
        sumForces = stokes(radius=radius,relativeVelocity=relativeVel,viscosity=viscosity)+\
                    DEP(CMFactor=DEPFactor,relativePermittivity=relativePermittivity,radius=radius,gradESquared=avgEField)      
        acceleration = sumForces/mass
        
        velocityTmp = particle.velocity+acceleration*dt/2
        positionTmp = particle.position+particle.velocity*dt/2
        
        positionTmp = chkPvsBnd(point = positionTmp)
        nearestIndexes = nearInds(positionTmp)
        avgVelTmp = interp(point=positionTmp,indexList=nearestIndexes,fieldName='velocity')
        avgEFieldTmp = interp(point=positionTmp,indexList=nearestIndexes,fieldName='Efield')
        
        particle.velocity = chkPvsTV(particleVelocity=velocityTmp,fluidVelocity=avgVelTmp
                                            ,DEPFactor=DEPFactor,radius=radius,Efield=avgEFieldTmp)       
        relativeVelTmp = avgVelTmp - velocityTmp
        sumForcesTmp = stokes(radius=radius,relativeVelocity=relativeVelTmp,viscosity=viscosity)+\
                        DEP(CMFactor=DEPFactor,relativePermittivity=relativePermittivity,radius=radius,gradESquared=avgEFieldTmp)
        accelerationTmp = sumForcesTmp/mass
        
        particle.velocity = particle.velocity + accelerationTmp*dt
        return chkPvsBnd(point=(particle.position+velocityTmp*dt),obj=particle)
        
    def particle3D(self,particle):
        """2nd order Runge-Kutta integrator for a particle
        
        Args:
            particle : Particle object
            fluid : Fluid object
            forces : Forces object
        """
        radius = particle.radius
        mass = particle.mass
        viscosity = self.fluid.viscosity
        #chkPvsBnd = self.TI.checkPointVsBoundaries
        chkPvsTV = self.checkParticleVsTerminalVelocity3D
        nearInds = self.TI.buildNearestIndexes3D
        interp = self.TI.trilinearInterpolation
        stokes = self.forces.stokes
        dt = self.dt
        
        nearestIndexes = nearInds(particle.position)
        avgVel = interp(point=particle.position,indexList=nearestIndexes)
        
        particle.velocity = chkPvsTV(particleVelocity=particle.velocity,fluidVelocity=avgVel)
        relativeVel = avgVel - particle.velocity
        sumForces = stokes(radius=radius,relativeVelocity=relativeVel,viscosity=viscosity)  
        acceleration = sumForces/mass
        
        velocityTmp = particle.velocity+acceleration*dt/2
        positionTmp = particle.position+particle.velocity*dt/2
        
        #positionTmp = chkPvsBnd(point = positionTmp)
        nearestIndexes = nearInds(positionTmp)
        avgVelTmp = interp(point=positionTmp,indexList=nearestIndexes)
        
        particle.velocity = chkPvsTV(particleVelocity=velocityTmp,fluidVelocity=avgVelTmp)      
        relativeVelTmp = avgVelTmp - velocityTmp
        sumForcesTmp = stokes(radius=radius,relativeVelocity=relativeVelTmp,viscosity=viscosity)
        accelerationTmp = sumForcesTmp/mass
        
        particle.velocity = particle.velocity + accelerationTmp*dt
        #return chkPvsBnd(point=(particle.position+velocityTmp*dt),obj=particle)
        return particle.position+velocityTmp*dt

    def checkParticleVsTerminalVelocity(self,particleVelocity,fluidVelocity,DEPFactor,radius,Efield):
        relativePermittivity=self.fluid.relativePermittivity
        vacuumPermittivity=self.physConsts.vacuumPermittivity
        viscosity=self.fluid.viscosity
        terminalVelocity = (DEPFactor*relativePermittivity*vacuumPermittivity*(radius**2)*Efield*((viscosity*3)**-1))+fluidVelocity
        if particleVelocity[0] > terminalVelocity[0]:
            particleVelocity[0] = terminalVelocity[0]
        if particleVelocity[1] > terminalVelocity[1]:
            particleVelocity[1] = terminalVelocity[1]
        return particleVelocity
        
    def checkParticleVsTerminalVelocity3D(self,particleVelocity,fluidVelocity):
        terminalVelocity = fluidVelocity
        if particleVelocity[0] > terminalVelocity[0]:
            particleVelocity[0] = terminalVelocity[0]
        if particleVelocity[1] > terminalVelocity[1]:
            particleVelocity[1] = terminalVelocity[1]
        if particleVelocity[2] > terminalVelocity[2]:
            particleVelocity[2] = terminalVelocity[2]
        return particleVelocity