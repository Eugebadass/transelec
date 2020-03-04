# from file import function
import os
import Resultats_Finaux
# Mettre le Path qui se rend où vous mettez tous les fichiers provenant d'OpenDSS (les exports)
Path = r"C:\Users\abcotech\Documents\transelec"
#C:\Users\LinaMarcelaZuluaga\Documents\OpenDSS\EPRITestCircuits\ckt5
from Resultats_Finaux import *

NombreCondensateur = CondensateurOuvert(Path) #Return somme du nombre de fois que le banc de condensateur est activé (À prendre en note)
ListeSurcharge, ListeSouscharge = surcharge_souscharge(1.02, 0.98, Path) #Return une liste des noms des noeuds en surcharge et une liste des noms des noeuds en souscharge
Maximum, Minimum, Variation = Variation_tension(Path) #Return Maximum et minimum de tension sur le réseau et la variation entre les deux (À prendre en note)
PertesTotaleRéseau = listerPertesTotales(Path) #Return la somme des pertes dans tout le réseau
Dict1, Dict2 = SurchargeTransfos(Path) # Return 2 dictionnaires
# Dictionnaire 1: key= nom du transfo ,value = puissance consommée en KVA
# Dictionnaire 2: key= nom du transfo, value = (puissance consommée - puissance nominale) KVA
KW, KVAR, FP = SubTransfoPower(Path) #Return Puissance en KW, Puissance réactive en KVAR et le facteur de puissance
PertesLines, PertesTransfo = ListerPertesTransfoLines(Path) #Return la somme des pertes dans les lignes et la somme des pertes dans les transfos
# Heure = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]


# Plotter_Graphes("Pertes de puissance dans les lignes (Simulation témoin)", "Heures", "Pertes en KW",Heure, str (PertesLines), "SimulationTPertesLignes","C:\\Users\\LinaMarcelaZuluaga\\Documents\\OpenDSS\\EPRITestCircuits\\ckt5\\Resultats")
# Plotter_Graphes("Pertes de puissance dans les transformateur (Simulation témoin", "Heures", "Pertes en KW", Heure, str (PertesTransfo), "SimulationTPertesTransfos","C:\\Users\\LinaMarcelaZuluaga\\Documents\\OpenDSS\\EPRITestCircuits\\ckt5\\Resultats")
# Plotter_Graphes("Pertes de puissance totale dans le réseau (Simulation témoin)", "Heures", "Pertes en KW", Heure, Pertes2, "SimulationTAllPertes","C:\\Users\\LinaMarcelaZuluaga\\Documents\\OpenDSS\\EPRITestCircuits\\ckt5\\Resultats")
# Plotter_Graphes("Évolution du maximum de tension sur le réseau (Simulation témoin)", "Heures", "Tension en V", Heure, Variation[0], "SimulationTMax","C:\\Users\\LinaMarcelaZuluaga\\Documents\\OpenDSS\\EPRITestCircuits\\ckt5\\Resultats")
# Plotter_Graphes("Évolution du minimum de tension sur le réseau (Simulation témoin)", "Heures", "Tension en V", Heure, Variation[1], "SimulationTMin","C:\\Users\\LinaMarcelaZuluaga\\Documents\\OpenDSS\\EPRITestCircuits\\ckt5\\Resultats")
# Plotter_Graphes("Évolution de la variation de tension sur le réseau (Simulation témoin)", "Heures", "Tension en V", Heure, Variation[2], "SimulationTVariation","C:\\Users\\LinaMarcelaZuluaga\\Documents\\OpenDSS\\EPRITestCircuits\\ckt5\\Resultats")

SaveInfoCSV(ListeSurcharge, "ListeSurchargeSimuTémoin", r"C:\Users\abcotech\Desktop\Résultats")
SaveInfoCSV(ListeSouscharge, "ListeSouschargeSimuTémoin", r"C:\Users\abcotech\Desktop\Résultats")
SaveInfoCSV(Dict1, "SurchargeTransfo1SimuTémoin", r"C:\Users\abcotech\Desktop\Résultats")
SaveInfoCSV(Dict2, "SurchargeTransfo2SimuTémoin", r"C:\Users\abcotech\Desktop\Résultats")







