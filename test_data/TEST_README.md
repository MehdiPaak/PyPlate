Test
---

This folder contains the input files for "unit" testing
and accuracy testing.
The problem is that of a plate simply supported on all edges
under a uniform pressure of 200 Pa (see [test input file](./inputdata_test.txt)).

Plat ehas the following parameters:
a = 1 
b = 2
h=0.001
E=2.0e11
nu=0.3

The maximum deflection will be at the middle x=0.5, y =1.
The analytical result for the max deflection at this point will be compared with that of
Salome-meca.

test should be performed using --test flag.
./fesim --test

Note that refining the mesh produces better accuracy.
