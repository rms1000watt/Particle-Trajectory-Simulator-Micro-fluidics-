from numpy import array
from numpy import pi

class Forces:
    def __init__(self,physicalConstants,includeGravitational,includeStokes,includeBuoyant,includeDEP):
        self.physicalConstants = physicalConstants
        self.vacuumPermittivity = physicalConstants.vacuumPermittivity
        self.includeGravitational = includeGravitational == "True"
        self.includeStokes = includeStokes == "True"
        self.includeBuoyant = includeBuoyant == "True"
        self.includeDEP = includeDEP == "True"
        
    def sumForces(self):
        forceList = []
        if self.includeGravitational:
            forceList.append(self.gravitational())
        if self.includeStokes:
            forceList.append(self.stokes())
        if self.includeBuoyant:
            forceList.append(self.buoyant())                    
        if self.includeDEP:
            forceList.append(self.DEP())
        pass
        
    def gravitational(self,mass=1):
        """
        the gravitational force 
        
        F = mass * gravitationalAcceleration , where mass can be defined as = density * volume
        
        Parameters
        ----------
        mass : mass defaults to 1
        """
        return (self.gravitationalAcceleration*mass)*self.includeGravitational
        
    def stokes(self,radius=1,viscosity=1,relativeVelocity=array([0,0])):
        """
        the stokes force 
        
        F = 6 * pi * fluid.viscosity * particle.radius * relativeVelocity
        
        Parameters
        ----------
        radius : particle radius (default to 1)
        viscosity : fluid viscosity (default to 1)
        relativeVelocity : difference from particle.velocity and fluid.velocity (default numpy.array([0,0]))
        """
        return (6*pi*viscosity*radius*relativeVelocity)*self.includeStokes
        
    def buoyant(self,radius=1,density=1):
        """
        the buoyant force (for sphere) (SI units)

        F = particle.volume * fluid.density * gravitationalAcceleration
        
        where particle.volume = 4/3*pi*radius**3
        
        Parameters
        ----------
        radius : radius of the particle (default to 1)
        """
        return ((-self.gravitationalAcceleration)*((pi)*(4/3)*(radius**3))*(density))*(self.includeBuoyant)
        
    def DEP(self,CMFactor=1,relativePermittivity=81,radius=1,gradESquared=array([0,0])):
        """
        the dielectrophoresis (DEP) force
        
        F = 2*pi * CMFactor * relativePermittivity*vacuumPermittivity * radius^3 * gradESquared
        
        Parameters
        ----------
        CMFactor : Clausius-Mossotti factor
        relativePermittivity : relative permittivity of the medium at specific frequency
        radius : radius of the particle
        gradESquared : vector quantity of the grad(|E|^2) numpy.array([Ex',Ey'])
        """
        return (2*pi*CMFactor*relativePermittivity*self.vacuumPermittivity)*(radius**3)*(gradESquared)*(self.includeDEP)
