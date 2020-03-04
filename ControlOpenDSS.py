author = "Paulo Radatz"
version = "01.00.05"
last_update = "11/30/2016"

import win32com.client
from win32com.client import makepy
from numpy import *
from pylab import *
import os
import math

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) #Variable globale correspondant au dossier local du projet

class DSS(object):

    #------------------------------------------------------------------------------------------------------------------#
    def __init__(self, dssFileName):
        """ Compile OpenDSS model and initialize variables."""

        self.dssFileName = dssFileName

        if self.dssFileName == "":
            print("Need to add the file path of the run file")

        # These variables provide direct interface into OpenDSS
        sys.argv = ["makepy", r"OpenDSSEngine.DSS"]
        makepy.main()  # ensures early binding and improves speed

        # Create a new instance of the DSS
        self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")

        # Start the DSS
        if self.dssObj.Start(0) == False:
            print("DSS Failed to Start")
        else:
            #Assign a variable to each of the interfaces for easier access
            self.dssText = self.dssObj.Text
            self.dssCircuit = self.dssObj.ActiveCircuit
            self.dssSolution = self.dssCircuit.Solution
            self.dssCktElement = self.dssCircuit.ActiveCktElement
            self.dssBus = self.dssCircuit.ActiveBus
            self.dssMeters = self.dssCircuit.Meters
            self.dssPDElement = self.dssCircuit.PDElements
            self.dssLoads = self.dssCircuit.Loads
            self.dssLines = self.dssCircuit.Lines
            self.dssTransformers = self.dssCircuit.Transformers

        # Always a good idea to clear the DSS when loading a new circuit
        self.dssObj.ClearAll()

        # Loads the given circuit master file into OpenDSS
        self.dssText.Command = "compile " + dssFileName

        # Lists
        self.transformersNames = []
        self.busesNames = []
        self.consumersNames = []
        self.transformersNames_ltc = []
        self.busesNames_ltc = []
        self.consumersNames_ltc = []
    #------------------------------------------------------------------------------------------------------------------#

    def run_simple_test(self): #the new runmaster script
        self.dssText.Command = "clearAll"
        self.dssText.Command = "compile " + self.dssFileName
        self.dssText.Command = "Set Datapath=" + ROOT_DIR

    #------------------------------------------------------------------------------------------------------------------#
    def redirect_curves(self, OpenDSS_folder_path, loadinglevel, pvGenCurve):
        '''
        Redirect the curves selected by the functions in the Settings Class
        '''

        self.dssText.Command = "Redirect " + OpenDSS_folder_path + "/LoadShapes_" + loadinglevel + ".dss"
        self.dssText.Command = "Redirect " + OpenDSS_folder_path + "/PVGenCurve_" + str(pvGenCurve) + ".txt"
        self.dssText.Command = "BatchEdit Load.. daily=residential"

    #------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------#
    def pvSystems(self, pvLocations, pf):
        '''
        Places the PVSystems at the buses selected
        '''

        num = len(pvLocations)
        for i in range(num):
            self.dssText.Command = "New PVSystem.PV_" + str(pvLocations[i]) + " phases=1 bus1=" + str(pvLocations[i]) + " kV=0.22 kVA=5 irradiance=1 Pmpp=5 pf=" + str(pf) + " %cutin=0.05 %cutout=0.05 VarFollowInverter=yes  daily=PVshape effcurve=Myeff  P-TCurve=MyPvsT TDaily=MyTemp"
            self.dssText.Command = "New monitor.PVpower" + str(i) + " element=PVSystem.PV_" + str(pvLocations[i]) + " terminal=1 mode=1 PPolar=no"

    #------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------#
    def solve_daily(self, tSinterval):
        '''
        Solves the circuit in daily mode and class function in order to evaluate if there is any issue
        '''

        self.dssObj.AllowForms = "false"
        self.dssText.Command = "set controlmode=static"
        self.dssText.Command = "set maxcontroliter=300"
        self.dssText.Command = "set maxiterations=300"
        self.dssText.Command = "set mode=daily stepsize=1h number=1"

        for i in range(tSinterval):

            self.dssText.Command = "Solve" # Solves just one time step

            # Calls functions in order to evaluate if there is any issue
            self.transformer_Overload_unbalanced()
            self.voltage_loads()

    #------------------------------------------------------------------------------------------------------------------#

    #------------------------------------------------------------------------------------------------------------------#

    def transformer_Overload_unbalanced(self):
        '''
        This function is called every single simulation step in order to evaluate if there
        is either any transformer with overload and unbalanced voltage at the first three-phase bus
        parent of the transformer analyzed
        '''

        self.dssTransformers.First

        # Looks at each sigle-phase transformer
        for i in range(self.dssTransformers.Count):

            numPhasesTrafo = self.dssCktElement.NumPhases
            kVAratedTrafo = self.dssTransformers.kva
            powersTrafo = self.dssCktElement.Powers

            if numPhasesTrafo == 1:

                kVATrafo = math.sqrt(powersTrafo[4]*powersTrafo[4] + powersTrafo[5]*powersTrafo[5])

                if kVATrafo > kVAratedTrafo:

                    # Includes the transformer name with overload. It is used by the ResultsFile function of the Settings Class
                    self.transformersNames.append(self.dssCktElement.Name)

                k = 1
                m = 1

                # Looks for the first parent three-phase bus
                while k >0 and m < 20:

                    m = m + 1
                    self.dssPDElement.ParentPDElement

                    if self.dssCktElement.NumPhases == 3:
                        k = 0

                        bus3phases = self.dssCktElement.BusNames[0]

                        self.dssCircuit.SetActiveBus(bus3phases)

                        if self.dssBus.SeqVoltages[2]/self.dssBus.SeqVoltages[1] > 0.05:

                            # Includes the bus name with unbalanced voltage. It is used by the ResultsFile function of the Settings Class
                            self.busesNames.append(self.dssCktElement.Name)
                            #print self.dssCktElement.Name

            self.dssTransformers.Next


    def voltage_loads(self):
        '''
        This function is called every single simulation step in order to evaluate if there
        is any load if voltage violation
        '''

        self.voltage_violation = 0

        self.loads_step = []

        self.dssLoads.First

        for i in range(self.dssLoads.Count):

            numPhasesLoad = self.dssCktElement.NumPhases

            if numPhasesLoad == 1:

                voltageBase = self.dssLoads.kV*1000
                voltageLoad = self.dssCktElement.VoltagesMagAng[0]/voltageBase

                if voltageLoad < 0.95 or voltageLoad > 1.05:
                    # Includes the load name with voltage violation. It is used by the ResultsFile function of the Settings Class
                    self.consumersNames.append(self.dssCktElement.Name)

            self.dssLoads.Next

