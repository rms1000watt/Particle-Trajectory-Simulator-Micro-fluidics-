from numpy import array

class Time:
    def __init__(self,start,stop,step):
        self.start = start
        self.stop = stop
        self.step = step
        self.list = array([])