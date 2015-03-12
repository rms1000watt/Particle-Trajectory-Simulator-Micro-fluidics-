from ptspy.simulator.rungeKuttaIntegrator import RungeKuttaIntegrator
from numpy import arange
from numpy import append
from numpy import newaxis
    
def startSimulation(allData):
    print "2. Starting Simulation"

    time = allData["time"]
    particleList = allData["particleList"]

    integrator = RungeKuttaIntegrator(
        X = allData["X"], 
        Y = allData["Y"],
        coordinates = allData["coordinates"], 
        velocityTranspose = allData["fluid"].velocity,
        dt = allData["time"].step, 
        gradESquaredTranspose = allData["gradE2"],
        fluid = allData["fluid"], 
        forces = allData["forces"], 
        physConsts = allData["physicalConstants"],
        repeatX = allData["repeatX"],
        repeatY = allData["repeatY"])

    for t in arange(0,time.stop,time.step):
        time.list = append(time.list,t)
        for index,particle in enumerate(particleList):
            particle.position = integrator.particle(particle=particle)
            particle.positionList = append(particle.positionList,particle.position[:,newaxis],1)

    print "2. Done"
    return particleList
    