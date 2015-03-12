from numpy import array

class PhysicalConstants:
    """
    Define physical constants (defaults to SI units)
    
    Physical Constants List
    -----------------------
    gravitationalAcceleration : acceleration due to gravity (defaults to numpy.array([0,-9.8]) (m/s))
    boltzmannConstant : boltzmann's constant (defaults to 1.38e-23 (J/K))
    vacuumPermittivity : vacuum permittivity (defaults to 8.85e-12 (F/m))
    """
    def __init__(self,gravitationalAcceleration=[0,-9.8],boltzmannConstant=1.38e-23,vacuumPermittivity=8.85e-12):
        self.gravitationalAcceleration = array(gravitationalAcceleration)
        self.boltzmannConstant = boltzmannConstant
        self.vacuumPermittivity = vacuumPermittivity