import random
import numpy as np


def test():

    file = open("XFR_Loads_ckt5.dss", "r")
    buses = []
    for line in file:
        if "kVA=50" in line:
            buses.append("X_" + line[line.find("bus=") + 4: line.find(" ", line.find("bus="))])
    file.close()


    charge = []
    puissance = []
    bus3Charge = []
    for bus in buses:
        cnt = 0
        file2 = open("Loads_ckt5.dss", "r")
        temp = 0
        puissanceTemp = 0
        for line in file2:
            if "Load." in line and (bus[:-2] + "_" in line or bus[:-2] + "." in line):
                cnt +=1
                if temp == 0 and cnt == 2:
                    c = line
                    b = line.find("kW=")
                    puissanceTemp = float(line[line.find("kW=") + 3: line.find(" ", line.find("kW="))])
                    temp = 1
                if cnt > 3:
                    puissanceTemp = 0
        file2.close()
        charge.append(cnt)
        if puissanceTemp != 0:
            puissance.append(puissanceTemp)
            bus3Charge.append(bus)
    somme = 0
    for x in charge:
        somme = somme + x

    moyCharge = somme/(len(charge))
    somme2 = 0
    for y in puissance:
        somme2 =  somme2 + y
    moyPuissance = somme2/(len(puissance))
    file.close()













if __name__ == '__main__':

    test()
