import matplotlib.pyplot as plt
        
def plotData(allData,particleList):
    print "3. Plotting Data"
    p = allData["plot"]
    p.trajectory(plt,allData,particleList)
    p.vectorField(plt,allData["X"],allData["Y"],allData["U"],allData["V"],"Fluid Velocity")
    p.vectorField(plt,allData["X"],allData["Y"],allData["gradE2X"],allData["gradE2Y"],"grad(|E^2|)")
    plt.show()
    print "3. Done"