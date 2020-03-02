author = "Paulo Radatz"
version = "01.00.03"
last_update = "11/30/2016"

import csv
import Tkinter  # These three are used for file dialogs
import tkFileDialog  # and message boxes to display information
import tkMessageBox  # to the user.
from pylab import *
import os
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties

fontP = FontProperties()
fontP.set_size('small')


class PlotResults:

    def __init__(self, folder, penetrationLevel, issue, issue_pf, num, num_pf):

        bar_width = 0.35
        index = np.arange(len(penetrationLevel))

        plt.figure("Scenarios with voltage issues")
        plt.subplot(1, 1, 1).set_ylim([0, 100])
        plt.bar(index, issue, bar_width, color = "r" , label = "FP 1")
        plt.bar(index + bar_width, issue_pf, bar_width, color = "b" , label="FP 0,985")
        plt.xlabel("Penetration Level (%)")
        plt.ylabel("Scenarios with voltage issues (%)")
        plt.xticks(index + bar_width, penetrationLevel)
        legend(bbox_to_anchor=(0, .94, 1, .102), loc=3, ncol=4, borderaxespad=0, shadow=True,fancybox=True, prop = fontP)

        grid(True)
        plt.tight_layout()

        savefig(folder + "/ScenariosIssues.png")


        plt.figure("Consumers with voltage issues")
        plt.subplot(1, 1, 1).set_ylim([0, 60])
        plt.bar(index, num, bar_width, color = "r" , label = "FP 1")
        plt.bar(index + bar_width, num_pf, bar_width, color = "b" , label="FP 0,985")
        plt.xlabel("Penetration Level (%)")
        plt.ylabel("Consumers with voltage issues (%)")
        plt.xticks(index + bar_width, penetrationLevel)
        legend(bbox_to_anchor=(0, .94, 1, .102), loc=3, ncol=4, borderaxespad=0, shadow=True,fancybox=True, prop = fontP)

        grid(True)
        plt.tight_layout()

        savefig(folder + "/ConsumersIssue.png")
