"""
Utility class for fesim
By: Mehdi Paak
"""

import os
import subprocess



def create_meshinput_file(vardict):
    """
    generate temporary mesh data input file
    to be read by salome_mesh.py script.
    """
    try:
        geofile = vardict['GEOFILE']
        wrkdir = vardict['WRKDIR']
        seg_a = vardict['SEG_A']
        seg_b = vardict['SEG_B']

        mshdatafile = 'mesh_data.txt'

        #TODO: check seg_a and seg_b type and value
        if(os.path.isfile(geofile) == False):
            raise Exception("Error: incorrect path to geofile")

        if(os.path.isdir(wrkdir) == False):
            raise Exception("Error: incorrect path to working director")

        with open(mshdatafile, 'w') as mshfile:
            mshfile.write(geofile+'\n')
            mshfile.write(wrkdir+'\n')
            mshfile.write(str(seg_a)+'\n')
            mshfile.write(str(seg_b)+'\n')

    except:
        print('Error ocurred creating mesh input file')
        raise

def call_salome_mesh(vardict):
    """
    create command and call salome to run
    salome_mesh.py.
    file mesh.med with be created if successful.
    """

    salome = vardict['SALOME']
    wrkdir = vardict['WRKDIR']
    salmsgfile = os.path.join(wrkdir,'Salome_msg.txt')
    mshdatafile = 'mesh_data.txt'
    try:

        if(os.path.isfile(salome) == False):
            raise Exception("Error: incorrect path to salome file,include filename e.g. .../.../salome")

        if (os.path.isfile(mshdatafile) == False):
            raise Exception("Error: mesh_data.txt does not exist")

        if (os.path.isfile('salome_mesh.py') == False):
            raise Exception("Error: salome_mesh.py does not exist")

        with open(salmsgfile,'w') as salmsg:
            runstr_salome = salome + ' -t' + ' salome_mesh.py'
            subprocess.call(runstr_salome, shell=True, stdout = salmsg, stderr = salmsg)

    except:
        raise


def create_export_file(vardict):
    """
    generate export file for Aster solver
    :param vardict:
    :return:
    """
    wrkdir = vardict['WRKDIR']
    exportfile = os.path.join(wrkdir,'fesim.export')

    runfile = os.path.join(wrkdir,'fesim_run.comm')
    mshfile = os.path.join(wrkdir,'mesh.med')
    resfiletxt = os.path.join(wrkdir,'Results.txt')
    resfilemed = os.path.join(wrkdir, 'Results.med')
    msgfile = os.path.join(wrkdir,'Aster_msg')

    try:
        with open(exportfile,'w') as expfile:
            expfile.write('P actions make_etude'+ '\n')
            expfile.write('P mode interactif'+ '\n')
            expfile.write('P ncpus 1'+ '\n')
            expfile.write('P nomjob Plate_Bending'+ '\n')
            expfile.write('P time_limit 1000.0'+ '\n')
            expfile.write('P version stable'+ '\n')
            expfile.write('A memjeveux 256'+ '\n')
            expfile.write('F comm '+ runfile+ ' D  1'+ '\n')
            expfile.write('F libr '+ mshfile+ ' D  20'+ '\n')
            expfile.write('F libr '+ resfiletxt+ ' R  80'+ '\n')
            expfile.write('F libr '+ resfilemed+ ' R  2'+ '\n')
            expfile.write('F mess '+ msgfile+ ' R  6'+ '\n')

    except:
        raise


def create_comm_script(vardict):
    """
    Read the comm schema and replace the tags with
    values. Finally write fesim_run.comm

    :param vardict:
    :return:
    """

    tags={'<H>':'H', '<E>':'E', '<NU>':'NU', '<PRES>': 'PRES'}
    bctags = '<bcs>'
    bc_ssss = ('DX = 0.0','DY = 0.0','DZ = 0.0')
    bc_cccc = ('DX = 0.0','DY = 0.0','DZ = 0.0','DRX = 0.0','DRY = 0.0')

    try:

        wrkdir = vardict['WRKDIR']
        bccond = vardict['BC']

        if (bccond == 'SSSS'):
            bcstr = ',\n                                '.join(bc_ssss)

        elif(bccond == 'CCCC'):
            bcstr = ',\n                                '.join(bc_cccc)

        else:
            raise Exception("Wrong BC: at the moment only SSSS or CCCC")

        schmfilename = os.path.join(wrkdir, 'comm_schema')

        if (os.path.isfile(schmfilename) == False):
            raise Exception("Error: schmfile does not exist")

        #TODO: more efficient string handling, avoid copying
        with open(schmfilename,'r') as schmfile:
            schmstr = schmfile.read()

        for tag,val in tags.items():
            schmstr = schmstr.replace(tag,str(vardict[val]))

        schmstr = schmstr.replace(bctags,bcstr)

        runscript = os.path.join(wrkdir, 'fesim_run.comm')
        with open(runscript,'w') as runfile:
            runfile.write(schmstr)

    except:
        raise Exception("Error creating comm file")


def run_aster(vardict):
    """
    create command string and call Aster.
    Upon Successful solution, two results files
    will be generated: (i) Results.med for visualization in Paravis
    and (ii) Results.txt containing the min max values

    :param vardict:
    :return:
    """
    salome = vardict['SALOME']
    wrkdir = vardict['WRKDIR']

    expfile = os.path.join(wrkdir,'fesim.export')

    runstr_aster = salome + ' shell -- as_run ' + expfile

    try:
        subprocess.call(runstr_aster, shell=True)
    except:
        raise

