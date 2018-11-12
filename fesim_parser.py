""" 
Class fesim_parser provides functions and utilities to  
parse the input lines and returns a dictionary of the variable 
names and values.
By: Mehdi Paak
"""
import os

class FEParser:
    """
    The input file structure
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
        $GEOFILE = 'path_to_iges_file'

        # Salome
        $SALOME = 'path_to_salome'

        # Working Directory
        $WRKDIR = 'path_to_wdir'

        # Material Prop: Young Modulus (Pa), Poisson Ratio, Plate Thickness (m)
        $E = 2.0e11
        $NU = 0.3
        $H = 0.001

        # Mesh Info: number of segments along side a and b
        $SEG_A = 10
        $SEG_B = 20

        # Pressure (Pa)
        $PRESS = 200.0

        # Boundary Conditions: Simply supported all edges-> SSSS, Clamped all edges-> CCCC
        $BC = SSSS

    """

    def __init__(self, lines):
        self.lines = lines
        self.symbstr = ('GEOFILE', 'SALOME', 'WRKDIR','BC')
        self.symbfloat = ('E', 'NU', 'H', 'PRES')
        self.symbint = ('SEG_A', 'SEG_B')
        self.allsymb = self.symbstr+ self.symbfloat + self.symbint


    def parse_input(self):
        """ """
        vardict = {}
        for line in self.lines:
            line = line.strip()
            if line[0] == '$':
                line = line[1:]
                line.strip()
                if '=' not in line:
                    print('bad line!')
                else:
                    lst = line.split('=')
                    lst[0] = lst[0].strip()
                    lst[1] = lst[1].strip()
                    key = lst[0]
                    if(key in self.symbstr):
                        vardict[key] = lst[1]
                    elif(key in self.symbfloat):
                        vardict[key] = float(lst[1])
                    elif(key in self.symbint):
                        vardict[key] = int(lst[1])
                    else:
                        pass
            else:
                continue

        #convert possible relative path to absolute path
        vardict['WRKDIR'] = os.path.abspath(vardict['WRKDIR'])
        vardict['SALOME'] = os.path.abspath(vardict['SALOME'])
        vardict['GEOFILE'] = os.path.abspath(vardict['GEOFILE'])

        return vardict

    def is_parsing_valid(self, i_vardict):
        """
        validating the parsed input
        dictionary must include all
        the keywords. this is a weak validation
        as it does not check the value type.
        """
        missing_keys=[]
        for key in self.allsymb:
            if(key not in i_vardict):
                #print("Keyword {0:s} is missing",key)
                missing_keys.append(key)

        return missing_keys


