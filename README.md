PyPlate
---
PyPlate is a program that uses Salome-Meca and Code Aster to simulate the 
bending of a Kirchohhff plate (i.e. no transverse shear) of 
rectangular shape under uniform pressure (see [wiki](https://en.wikipedia.org/wiki/Kirchhoff%E2%80%93Love_plate_theory)).

To recieve a copy of the code, send me an email on `matti.logiko@gmail.com`

## Installation
Just copy the contents (i.e., scripts and folders).
This program is developed using Python 3 and makes use
of modules that might not be installed on your system.
Please, make sure to resolve the dependencies first.

Dependencies are listed in `requirements.txt`; the packages
in the list can be installed using:
```bash
pip install -r requirements.txt
```

## How to use
The driver script is fesim.py:
To run an analysis: 
```
$ ./fesim -f inputdata.txt 
or
$ python3 fesim.py -f inputdata.txt
```
To run the unit test: 
```
$ ./fesim --test             
or 
$ python3 fesim.py --test
```
input should be provided in an `input file` (e.g. inputdata.txt)
This file `must` be located in the same directory as fesim or absolute path provided.

## Necessary files
- `input file`: inputdata.txt can be used as a sample; also included at the end of this document.
- `comm_schema`: must be in the working directory
- iges file: better be in the working directory
- for test (--test), the associated files are in the test directory.

## Procedure
1. setup the required information in the inputfile (look at the sample input file provided inputdata.txt)
2. place the geometry file in the location mentioned in the input file.
3. use fesim command described at the begining to run the simulation
4. inspect the results (med files) using salome-meca or visualizer of your choice.

## Test
The "unit test" (to be completed for all modules) for now runs
the whole program for a specific geomtery and compares the results
with the analytical solution. The relative error is reported at the end
of the program execution (usually less than 0.4%).

## program structure
The program workflow pipeline is as following:  
1. read simulation from input file
2. call Salome with the geometry file (iges)
3. create finite element mesh (Quad)
4. set up the comm and export files
5. call CodeAster to solve the finite element simulation
6. save simulation results in Results.med which can be used in Salome and Paraview
7. save the maximum amplitudes of the stress and displacement components in a Results.txt file.

## Authors
Mehdi Paak, _initial work_

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE)  file for details.
For pedagogical purposes, please, do not submit this code as a solution for course assignments,exams and interview
case studies.

## Acknowledgments
Thanks to teams at Salome-Meca and Code Aster for providing
free simulation tools. 

## TODOs
The program in its present form is not optimized. The first
attempt was just to go through all the steps and later improve
the performance and readability. So, feel free to change and modify
where necessary.

## Sample input file
In the input file, comments are indicated by a # and keywords
start by a $:
```
################################################
#       Plate Finite-Element Simulation
#     Plate Bending Under Uniform Pressure
#
#         y|______
#          |      |
#          |      |
#          |      | b
#          |      |
#          |______|___x
#              a
#
# The plate geometry must be provided in iges format, unit meter.
#
#            edge y1
#         y|______
#          |      |
#          |      |
#  edge x0 |      | edge x1
#          |      |
#          |______|___x
#           edge y0
#
#
# Input data required:
#   - GEOFILE:  Path to the iges geometry file
#   - SALOME: path to Salome
      (for Salome-meca 2017: installationdir//salome_meca/appli_V2017.0.2/salome)
#   - WRKDIR: Working Directory
#   - E (Pa): Young modulus
#   - NU: Poisson Ratio
#   - H (m): Plate Thickness
#   - SEG_A: number of segments along side a
#   - SEG_B: number of segments along side b
#   - PRESS (Pa): Uniform pressure
#   - BC: boundary conditions; simply supported along contour SSSS, or clampped CCCC
# Note:
#  The input file is provided to fesim.py as an
#  argument.
################################################

# Geometry file
$GEOFILE = ./wrkdir/plate.iges

# Salome
$SALOME = /opt/salome_meca/appli_V2017.0.2/salome

# Working Directory
$WRKDIR = ./wrkdir

# Material Prop: Young Modulus (Pa), Poisson Ratio, Plate Thickness (m)
$E = 2.0e11
$NU = 0.3
$H = 0.001

# Mesh Info: number of segments along side a and b
$SEG_A = 10
$SEG_B = 20

# Pressure (Pa)
$PRES = 200.0

# Boundary conditions
$BC = SSSS
```