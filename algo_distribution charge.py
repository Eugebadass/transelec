import random
import numpy as np
import ControlOpenDSS
from Resultats_Finaux import *


class Test:

    def __init__(self, filepath="", runfile="", penetration=0.0, coincidence=0.0):

        self.filepath = filepath
        self.runfile = runfile
        self.prob = penetration*coincidence
        self.buses = []
        self.aleatoire = []
        self.openDss = 0

        if self.filepath == "":
            print("There is not filename entered")

        if self.runfile == "":
            print("There is not runfile entered")

        if self.prob == 0.0:
            print("Please enter another value then 0.0 as a penetration factor or a coincidence factor")

    def find_buses(self):

        file = open(self.filepath, "r")
        for line in file:
            if "Load" in line:
                self.buses.append(line[line.find("bus1=") + 5: line.find(" ", line.find("bus1="))])
        file.close()

    def add_car_loads(self):
        self.aleatoire = np.random.uniform(0, 1, len(self.buses))
        cnt = 0
        file = open(self.filepath, "a")
        for i in self.aleatoire:

            if i < (self.prob):
                file.write("\nNew Load." + "vehicule_" + str(cnt) + "  phases=1  bus1=" + str(self.buses[cnt])
                           + "  kv=0.24  kW=5.149  pf=0.997 conn=wye")
            cnt += 1
        file.close()

    def remove_car_loads(self):

        file = open(self.filepath).read().splitlines()
        cnt = 0
        for line in file:
            if "Load.vehicule" in line:
                file[cnt] = ""
            file[cnt].replace("\n", "")
            cnt += 1
        file = filter(lambda x: x.strip(), file)
        lines = open(self.filepath, "w")
        lines.write("\n".join(file))
        lines.close()

    def open_dss_connection(self):
        self.openDss = ControlOpenDSS.DSS(self.runfile)

    def iterative_test(self, n):
        if not self.buses:
            self.find_buses()

        self.add_car_loads()
        self.open_dss_connection()
        SubTransfoPower(r"C:\Users\abcotech\Documents\transelec")
        self.remove_car_loads()
        n = n - 1
        while n != 0:
            self.add_car_loads()
            self.openDss.run_simple_test()
            SubTransfoPower(r"C:\Users\abcotech\Documents\transelec")
            self.remove_car_loads()
            n -= 1
        Monte_Carlo(KW_IT)
        Monte_Carlo(listeSurcharge)
        print(KW_IT)
        print(len(KW_IT))
        print(listeSurcharge)
        print(len(listeSurcharge))
        KW_IT==[]
        listeSurcharge==[]



    def simple_test(self):
        if not self.buses:
            self.find_buses()
        self.remove_car_loads()
        self.add_car_loads()
        self.open_dss_connection()


if __name__ == '__main__':

    test1 = Test("Loads_ckt5_test.dss", r"C:\Users\abcotech\Documents\transelec\Run_Master_ckt5_testing",
                 0.6, 0.7)
    test1.remove_car_loads()
    test1.iterative_test(n=1000)
