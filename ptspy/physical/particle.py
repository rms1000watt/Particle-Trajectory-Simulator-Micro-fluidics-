from numpy import array

class Particle:
    """The 2D particle object (SI units).
    
    Attributes:
        position : 2D numpy.array for particle's initial position (defaults to array([0,0]))
        velocity : 2D numpy.array for particle's initial velocity (defaults to array([0,0]))
        acceleration : 2D numpy.array for particle's initial acceleration (defaults to array([0,0]))
        mass : An integer for particle mass (defaults to 1)
        radius : An integer for particle radius (defaults to 1)
        density : An integer for particle density (defaults to 1)
        name : A string to define the particle's name (defaults to 'particle')
        DEPFactor : An integer for particle Dielectrophoresis or Clausius-Mossotti Factor (defaults to 1, ranges from -.5 to 1.5)
        positionList : 2D numpy.array for particle's position during simulation time (numpy.array([[x1,x2,x3,...],[y1,y2,y3,...]])
        velocityList : 2D numpy.array for particle's velocity during simulation time (numpy.array([[vx1,vx2,vx3,...],[vy1,vy2,vy3,...]])
        accelerationList : 2D numpy.array for particle's acceleration during simulation time (numpy.array([[ax1,ax2,ax3,...],[ay1,ay2,ay3,...]])
        repeatCnt : An integer used internally to keep track if particle went off screen and re-spawned at beginning
    """
    def __init__(self,position=[0,0],velocity=[0,0],acceleration=[0,0],mass=1,radius=1,\
                 density=1,DEPFactor=1, name='particle'):
        self.position = array(position)
        self.velocity = array(velocity)
        self.acceleration = array(acceleration)
        self.mass = mass
        self.radius = radius
        self.density = density
        self.name = name
        self.DEPFactor = DEPFactor
        self.positionList = array([[],[]])
        self.velocityList = array([[],[]])
        self.accelerationList = array([[],[]])
        self.repeatCnt = 0