import argparse
 
def parseArgs():
    parser = argparse.ArgumentParser(description="Basic Particle Trajectory Simulator for Dielectrophoresis in Microfluidics.")
    parser.add_argument("configFile", type=str, help="The configuration file.")
    return parser.parse_args()