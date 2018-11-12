"""
module for testing fesim
The test is performed by comparing the maximum displacement results
from simulation with that predicted by analytical solution.
Note that the boundary condition in the input file must be SSSS
(simply-supported) as the analytical solution is valid for this
BCs.

By: Mehdi Paak
"""
import os
import re
import fesim_run_func as fesimrun
import plate_analytical_sol as plate_analytical

def test():
    # Path to test input file is fixed; modify if necessary
    inputfile = r'./test_data/inputdata_test.txt'
    if os.path.isfile(inputfile) == False:
        print("Error: test input file does not exist")
        exit(-1)

    vardict = fesimrun.fesim_run(inputfile)

    # Extract the maximum deflection in z direction (normal)
    print("Extracting the maximum DZ from Results.txt")
    with open('./test_data/Results.txt','r') as resfile:
        for line in resfile:
            if 'LA VALEUR MAXIMALE DE DZ' in line:
                MaxDzStr = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", line)[0]
                fesim_max_Dz = float(MaxDzStr.strip())
                break

    x=0.5
    y=1.0
    a = 1.0
    b = 2.0
    h = vardict['H']
    nu = vardict['NU']
    E = vardict['E']
    p0 = vardict['PRES']

    # w(x,y,a,b,h,nu,E,P0)
    analytical_max_Dz = plate_analytical.w(x,y,a,b,h,nu,E,p0)

    print("Max DZ from simulation = {0:f}".format(fesim_max_Dz))
    print("Max DZ from analytical = {0:f}".format(analytical_max_Dz))
    print("Rel Error = {0:2.2f}%".format(abs((fesim_max_Dz - analytical_max_Dz)/analytical_max_Dz)*100.0))