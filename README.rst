==============
ptspy: Particle Trajectory Simulator for Python
==============

Introduction
============

This project simulates trajectories of micro-scale particles flowing through fluid and electric fields. The simulator was intended to study Stoke's and Dielectrophoresis forces acting on particles traversing microfluidic, biomedical devices. For instance, particles are separated based on their dielectric properties which would allow us to isolate cancer cells in the blood. 

This project was used during the design process of a microfluidic device to significantly cut down on manufacturing time. This simulator allowed us to say, "..this design could be best, go manufacture it..." rather than saying, "..manufacture these 15 designs and lets see what's best.."

Example code can be found in the "examples" folder.

Requirements
============

Python 2.7 (Haven't tested with other Python 2.X, but I assume it should be fine. However, most likely not compatible with Python 3.X.)

Python Libraries:
	numpy
	matplotlib
	pylab
	math
	json
	argparse

Installing 
==========

Do the standard git process.

Alternatively:
	1. Download zip file
	2. Unzip file in a known location
	3. Go into your Terminal and change directory to where the project was unzipped
	4. "$ cd Documents/Libraries/Particle-Trajectory-Simulator-Microfluidics-"
	5. Install the ptspy library
	6. "$ sudo python setup.py install"

Usage
=====

This project was designed for the command line. Follow this process for the example code.

Process:
	1. Go into your Terminal and change directory to the project in the example folder
	2. "$ cd "example/Basic DEP"
	3. Run the example code and pass the location of the config.json
	4. "$ python basic_dep.py config.json"
	
You can change the config.json and particle_data.csv files as you please.

Notes
=====

Vector fields must first be generated for this simulator to work. COMSOL was used to generate and export vector fields in .csv format. You can see the example format with the example code.

Acknowledgements
===========

This simulator was developed at UC Irvine for Microfluidic device simulation in the Micro Integrated Devices and Systems (MIDAS) Lab.

As seen in: http://scitation.aip.org/content/aip/journal/bmf/8/3/10.1063/1.4880244