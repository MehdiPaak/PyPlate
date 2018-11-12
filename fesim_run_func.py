"""
This function takes input file as an argument and
runs the analysis.

This function is called by fesim.
By: Mehdi Paak
"""
import os
import fesim_util
from fesim_parser import FEParser

def fesim_run(inputfile):
    print("-- fesim reading the input file {0:s} --".format(inputfile))
    with open(inputfile, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # print(lines)

    feparser = FEParser(lines)
    vardict = feparser.parse_input()
    msk = feparser.is_parsing_valid(vardict)
    if (len(msk) > 0):
        print("missing inputs: ", *msk)

    # print(vardict)

    # Procees to meshing using Salome
    # TODO insert path for import

    print('-- creating mesh input file --')
    try:
        fesim_util.create_meshinput_file(vardict)
        fesim_util.call_salome_mesh(vardict)
    except Exception as e:
        print(str(e))
        exit(-3)

    print('-- Mesh created successfully: mesh.med --')

    # Procees to Aster Solution
    try:

        # 1. create export file
        print('-- creating export file --')
        fesim_util.create_export_file(vardict)

        # 2. create run script
        print('-- creating run file --')
        fesim_util.create_comm_script(vardict)
        # 3. Run Aster
        print('-- Running Salome Aster --')
        fesim_util.run_aster(vardict)

    except Exception as e:
        print(str(e))
        exit(-4)

    print("Solution Successful")

    # cleaning

    try:
        wrkdir = vardict['WRKDIR']
        files_tobe_detelted = (
            'mesh_data.txt',
            os.path.join(wrkdir, 'Aster_msg'),
            os.path.join(wrkdir, 'fesim.export'),
            os.path.join(wrkdir, 'fesim_run.comm'),
            os.path.join(wrkdir, 'Salome_msg.txt'))

        for file in files_tobe_detelted:
            os.remove(file)

    except OSError as e:
        print("Error deleting file " + e.filename)

    return vardict  #useful for test