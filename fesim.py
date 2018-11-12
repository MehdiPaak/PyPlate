#!/usr/bin/python3
#/usr/bin/env python

"""
Program to simulate bending of a Kirchohhff plate (i.e. no transverse shear)
of rectangular shape under uniform pressure.

By: Mehdi Paak

"""
import os
import argparse
import fesim_test as ftest
import fesim_run_func as fesimrun

parser = argparse.ArgumentParser(description='Read input file, Run plate simulation')

parser.add_argument('-f', action='store',
                    dest='inpfile',
                    help='Input File')

parser.add_argument('--test', action='store_true',
                    dest='perftest',
                    help='Perform Test')

args = parser.parse_args()
#print(args)

if(args.perftest == True):
    print("-- performing test --")
    ftest.test()
    exit(0)



if(args.inpfile == None):
    print("Error: specify an input file, e.g. fesim -f inpfile")
    exit(-1)

if(os.path.isfile(args.inpfile) == False):
    print("Error: input file does not exist")
    exit(-2)

fesimrun.fesim_run(args.inpfile)
