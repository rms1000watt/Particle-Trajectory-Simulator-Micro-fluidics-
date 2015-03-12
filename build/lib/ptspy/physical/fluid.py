from numpy import array

class Fluid:
    """The fluid object (SI units).
    
    Attributes:
        density : An integer for density (defaults to 1)
        viscosity : An integer for viscosity (defaults to 1)
        name : A string to define the fluid's name (defaults to 'fluid')
        velocity : A numpy.array for velocity field (numpy.array([[x1,y1],[x2,y2],[x3,y3],...]))
        relativePermittivity : An integer for fluid permittivity (defaults to 81)
    """
    def __init__(self,density=1,viscosity=1,name='fluid',velocity=array([0,0]),relativePermittivity=81):
        self.density = density 
        self.viscosity = viscosity
        self.name = name
        self.velocity = velocity
        self.relativePermittivity = relativePermittivity