author = "Paulo Radatz"
version = "01.00.08"
last_update = "11/30/2016"

import ControlOpenDSS # Class which creates the OpenDSS object
import PlotResults # Class which creates the plots
import string
import numpy as np
import os
import csv
import timeit
import shutil
import random

class Settings(object):

    def __init__(self, dssFileName, perCent, numSimulations):

        start_time = timeit.default_timer()

        # OpenDSS options
        self.stepsize = 1
        self.tSinterval = 24

        # Number of load connected into the CKT5 feeder
        self.numConsumersTotal = 1379.0

        # defining lists in order to create some plots
        issueList = []
        issue_ltcList = []
        issue_pf_ltcList = []
        issue_pfList = []
        numList = []
        num_ltcList = []
        num_pf_ltcList = []
        num_pfList = []
        penetrationLevel = []

        # Each penetration level will be simulated
        for k in range(len(perCent)):

            # Global variables
            self.perCent = perCent[k]
            self.folderOpenDSS(dssFileName)
            self.pvPF = ["1", "-0.985"]

            # Function that creates the output files
            self.resultsFileHead()

            issue = 0
            issue_ltc = 0
            issue_pf_ltc = 0
            issue_pf = 0

            # Defining lists for each penetration level
            num = []
            num_ltc = []
            num_pf_ltc = []
            num_pf = []

            for i in range(numSimulations):

                # Calls a function that returns randomly one loadshape and also one couple of irradiation and temperature curves
                self.loadinglevel, self.pvGenCurve = self.curvesDefinition()

                # Calls a function that returns the costumers buses that will have the PVSystem connected.
                self.pvLocations = self.pvLocationDefinition(self.perCent)

                # Each scenario will be simulated with two different PVSystem's pf: 1 and -0.985
                for j in range(len(self.pvPF)):

                    pf = self.pvPF[j]

                    # Calls a function that creates the OpenDSS object
                    self.runCase(dssFileName, pf)

                    # Calls a function that write the actually results at the output file
                    self.resultsFile(pf)

                    if j == 0:
                        issue = issue + self.issue

                        if self.issue == 1:
                            num.append(self.numConsumers/self.numConsumersTotal)

                    if j == 1:
                        issue_pf = issue_pf + self.issue

                        if self.issue == 1:
                            num_pf.append(self.numConsumers/self.numConsumersTotal)


            if len(num) == 0:
                num.append(0)
            if len(num_pf) == 0:
                num_pf.append(0)

            numList.append(np.average(num)*100)
            num_pfList.append(np.average(num_pf)*100)

            issueList.append(issue*100.0/numSimulations)
            issue_pfList.append(issue_pf*100.0/numSimulations)

            penetrationLevel.append(self.perCent)

        # Creates an object by using the PlotResults Class. Bear in mind that this class is defined in PlotResults.py file
        PlotResults.PlotResults(self.path_plot, penetrationLevel, issueList, issue_pfList, numList, num_pfList)



        elapsed = timeit.default_timer() - start_time

        print "RunTime is: " + str(elapsed)

    def folderOpenDSS(self, dssFileName):

        # OpenDSS folder
        self.OpenDSS_folder_path = os.path.dirname(dssFileName)
        self.path_plot = self.OpenDSS_folder_path + "/Results"
        self.path_complete = self.OpenDSS_folder_path + "/Results" + "/" + str(self.perCent)

        if os.path.exists(self.path_complete):
            shutil.rmtree(self.path_complete)
        os.makedirs(self.path_complete)


    def runCase(self, dssFileName, pf):

        # Creates the self.Case object by using the ControlOpenDSS Class. Bear in mind that this class is defined in ControlOpenDSS.py file
        self.Case = ControlOpenDSS.DSS(dssFileName)

        # Calls functions defined at the DSS class
        self.Case.redirect_curves(self.OpenDSS_folder_path, self.loadinglevel, self.pvGenCurve) # Redirect the curves
        self.Case.pvSystems(self.pvLocations, pf) # Sets the PVSystems at the buses
        self.Case.solve_daily(self.tSinterval) # Solve in daily mode

    def resultsFileHead(self):

        self.cr_1 = csv.writer(open(self.path_complete + "/summaryResults_pf1.csv", "wb"))
        first_line = ["PerCent", "Loading Level", "Solar Curve", "Transformer Overload", "Number of Transformers", "Voltage Unbalanced",
                      "Number of 3phase Buses", "Voltage Level", "Number of Consumers", "Issue", "Transformers Names", "Buses Names", "Consumers Names"]
        self.cr_1.writerow(first_line)

        self.cr_985 = csv.writer(open(self.path_complete + "/summaryResults_pf985.csv", "wb"))
        self.cr_985.writerow(first_line)

    def resultsFile(self, pf):

        # Looks if there is any transformer with overload
        transformerOverLoad = 0
        numTransformes = 0
        if len(self.Case.transformersNames) > 0:
            transformerOverLoad = 1
            numTransformes = len(list(set(self.Case.transformersNames)))

        # Looks if there is unbalanced voltage at any first transformer parent bus
        voltageUnbalanced = 0
        numBuses = 0
        if len(self.Case.busesNames) > 0:
            voltageUnbalanced = 1
            numBuses = len(list(set(self.Case.busesNames)))

        # Looks if there is load with voltage violation
        voltageLevel = 0
        self.numConsumers = 0
        if len(self.Case.consumersNames) > 0:
            voltageLevel = 1
            self.numConsumers = len(list(set(self.Case.consumersNames)))

        # writes the results at the output files
        self.issue = 0

        if len(self.Case.transformersNames) > 0 or len(self.Case.busesNames) > 0 or len(self.Case.consumersNames) > 0:
            self.issue = 1

        line = [str(self.perCent), self.loadinglevel, self.pvGenCurve, str(transformerOverLoad), str(numTransformes), str(voltageUnbalanced),
                      str(numBuses), str(voltageLevel), str(self.numConsumers), str(self.issue), str(list(set(self.Case.transformersNames))), str(list(set(self.Case.busesNames))), str(list(set(self.Case.consumersNames)))]
        if pf == "1":
            self.cr_1.writerow(line)
        if pf == "-0.985":
            self.cr_985.writerow(line)

    def pvLocationDefinition(self, perCent):

        cr = csv.reader(open("C:\Users\PauloRicardo\Desktop\CodigoOpenDSS_v4\ckt5\\buses.csv")) # You need to change this directory and use my file buses.csv
        buses = []
        flag = 0
        for row in cr:
            if flag == 0:
                buses.append(row[0])
                flag = 1
            else:
                flag = 0

        consumers = len(buses)

        numPV = perCent*consumers/100

        return random.sample(buses,numPV)

    def curvesDefinition(self):

        # Loadshape option, we have just two options here
        loadingLevel = ["offpeak", "peak"] # You need to have those files

        # Irradiation and temperature options
        pvCurve = ["1","2"] # You need to have those files

        return str(random.sample(loadingLevel,1)[0]), str(random.sample(pvCurve,1)[0])


if __name__ == '__main__':

    # The code starts here

    perCent = [0, 10, 20 ,30, 40, 50, 60, 70, 80, 90, 100] # Sets the penetration level options: perCent=10 means (number of Costumers with PV)/(Total Costumers)
    numSimulations = 2 # Sets how many scenarios will be simulated for each penetration level

    # This code was made to work with Ckt5 circuit. That been said, you should include its address below without any space.
    myObject = Settings("C:\Users\PauloRicardo\Desktop\CodigoOpenDSS_v4\ckt5\Master_ckt5.dss", perCent, numSimulations) # This line creates an object "myObject" using the Settings Class

