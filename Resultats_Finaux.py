import csv
import os
import math
import statistics
import pylatex
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) #Variable globale correspondant au dossier local du projet

# Mettre le Path qui se rend où vous mettez tous les fichiers provenant d'OpenDSS (les exports)


# changer le working directory à celui que je veux
os.chdir(ROOT_DIR)
#C:\Users\LinaMarcelaZuluaga\Documents\OpenDSS\EPRITestCircuits\ckt5
#C:\ProgramData\Microsoft\Windows\Start Menu\Programs\OpenDSS

# M'assurer que je suis dans le bon directory
print("current working directory",os.getcwd())
# Ouvrir le fichier désiré

#######################################################################
# Number of time the condensators are open

KW_IT=[] #VARIABLE GLOBALE POUR LES TESTS ITÉRATIFS
KVAR_IT=[]
listeSurcharge=[]


def CondensateurOuvert(Path):
    os.chdir(Path)
    boolyCond = False
    sommeCond = 0
    with open("ckt5_EXP_EventLog.CSV") as csv_Condensateur:
        csv_reader2 = csv.reader(csv_Condensateur, delimiter=',')
        for row in csv_reader2:
            boolyCond = row[4].find('OPENED')
            if boolyCond != -1:
                sommeCond = sommeCond + 1

    csv_Condensateur.close()
    print("Somme des fois où les condensateurs ont été ouverts = ", sommeCond)
    return sommeCond
###########################################################################
# Régulateur de tension
def surcharge_souscharge(borneMax, borneMin, Path):
    os.chdir(Path)
    NombreSurcharge = 0
    NombreSousCharge = 0
    NombreIteration = 0
    Liste_nom_noeud_surcharge = []
    Liste_nom_noeud_souscharge = []

    with open("ckt5_EXP_Profile.csv") as csv_Voltage:
        csv_reader3 = csv.reader(csv_Voltage, delimiter=',')
        for row in csv_reader3:
            BoolyVoltage = row[0].find('Name')
            if BoolyVoltage == -1:
                if float(row[2]) > borneMax or float(row[4]) > borneMax:
                    NombreSurcharge = NombreSurcharge + 1
                    Liste_nom_noeud_surcharge.append(row[0])

                    if float(row[2]) > borneMax:
                        surcharge = float(row[2]) - borneMax
                        Liste_nom_noeud_surcharge.append(surcharge)
                    else:
                        surcharge = float(row[4]) - borneMax
                        Liste_nom_noeud_surcharge.append(surcharge)

                if float(row[2]) < borneMin or float(row[4]) < borneMin:
                    NombreSousCharge = NombreSousCharge + 1
                    Liste_nom_noeud_souscharge.append(row[0])

                    if float(row[2]) < borneMin:
                        soustension =  borneMin - float(row[2])
                        Liste_nom_noeud_souscharge.append(soustension)
                    else:
                        soustension = borneMin - float(row[4])
                        Liste_nom_noeud_souscharge.append(soustension)

            NombreIteration= NombreIteration + 1

    csv_Voltage.close()
    print("Nombre de Surcharge en tension sur le réseau = ", NombreSurcharge)
    print("Nombre de Sous Charge en tension sur le réseau = ", NombreSousCharge)
    return Liste_nom_noeud_surcharge, Liste_nom_noeud_souscharge

###########################################################################################
#Fonction pour additionner 2 listes ensemble
def addUpList(Liste1, Liste2):
   Liste = []
   Liste.append(Liste1)
   Liste.append(Liste2)
   return Liste

###########################################################################################
#Fonction pour transformer une liste en dictionnaire( compte les occurences des noms)
def ListToDict(liste):
    from collections import Counter
    Count = Counter(liste)
    Dict = dict(Count)
    return Dict
###########################################################################################
# Fonction qui compte combien de surcharge et de sous-charge durant chaque itérations

def surcharge_souschargeLOOP():
    os.chdir(ROOT_DIR)


    Heure = 1
    Liste_Surcharge = []
    Liste_Souscharge = []
    borneMax = 1.00
    borneMin = 1.00

    for i in range(24):
        heure_string = str(Heure)
        NombreSurcharge = 0.0
        NombreSousCharge = 0.0
        with open(heure_string + "h_EXP_Profile.csv") as csv_Voltage:
            csv_reader4 = csv.reader(csv_Voltage, delimiter=',')
            for row in csv_reader4:
                BoolyVoltage = row[0].find('Name')

                if BoolyVoltage == -1:
                    if float(row[2]) > borneMax or float(row[4]) > borneMax:
                         NombreSurcharge = NombreSurcharge + 1

                    if float(row[2]) < borneMin or float(row[4]) < borneMin:
                         NombreSousCharge = NombreSousCharge + 1

            csv_Voltage.close()
            Heure = Heure + 1
            Liste_Souscharge.append(NombreSousCharge)
            Liste_Surcharge.append(NombreSurcharge)
    print("Liste surcharge = ", Liste_Surcharge)
    print("Liste souschsrge = ", Liste_Souscharge)
    return Liste_Surcharge, Liste_Souscharge

###########################################################################################
# fonction qui retourne la variation min-max en pu
#Fonction qui ne prend pas en compte la variation en temps
def Variation_tension(Path):
    os.chdir(Path)
    Maximum = 0.0
    Minimum = 1.0
    with open("ckt5_EXP_Profile.csv") as csv_Variation_Voltage:
        csv_reader4 = csv.reader(csv_Variation_Voltage, delimiter=',')
        for row in csv_reader4:
            BoolyVoltage = row[0].find('Name')
            if BoolyVoltage == -1:
                if Maximum < float(row[2]):
                    Maximum = float(row[2])
                if Maximum < float(row[4]):
                    Maximum = float(row[4])
                if Minimum > float(row[2]):
                    Minimum = float(row[2])
                if Minimum > float(row[4]):
                    Minimum = float(row[4])
    csv_Variation_Voltage.close()
    print("Maximum de tension est = ", Maximum)
    print("Minimum de tension est = ", Minimum)
    print("La variation de tension est = ", Maximum-Minimum)

    return Maximum, Minimum, Maximum-Minimum

#Fonction qui prend en compte la variation dans le temps
def Variation_tensionLOOP(Path):
    os.chdir(Path)
    Heure = 1
    Liste_max = []
    Liste_min = []
    Liste_variation = []

    for i in range(24):
        heure_string = str(Heure)
        Maximum = 0.0
        Minimum = 1.0
        with open(heure_string + "h_EXP_Profile.csv") as csv_Variation_Voltage:
            csv_reader4 = csv.reader(csv_Variation_Voltage, delimiter=',')
            for row in csv_reader4:
                BoolyVoltage = row[0].find('Name')
                if BoolyVoltage == -1:
                    if Maximum < float(row[2]):
                        Maximum = float(row[2])
                    if Maximum < float(row[4]):
                        Maximum = float(row[4])
                    if Minimum > float(row[2]):
                        Minimum = float(row[2])
                    if Minimum > float(row[4]):
                        Minimum = float(row[4])
        csv_Variation_Voltage.close()
        Liste_max.append(Maximum)
        Liste_min.append(Minimum)
        Liste_variation.append(Maximum - Minimum)
        Heure = Heure + 1

    print("Maximum de tension est = ", Liste_max)
    print("Minimum de tension est = ", Liste_min)
    print("LA variation de tension est = ",Liste_variation )

    return Liste_max, Liste_min, Liste_variation
#########################################################################################
# Fonctions qui renvoient les pertes totales dans le réseau à chaque intervalle de temps
#Cette fonction ne prend pas en compte la variation du temps
def listerPertesTotales(Path):
    os.chdir(Path)
    somme = 0.0
    with open("ckt5_EXP_LOSSES.CSV") as csv_losses:
        csv_reader6 = csv.reader(csv_losses, delimiter=',')
        list_iterator = iter(csv_reader6)
        next(list_iterator)
        for row in csv_reader6:
            somme = somme + float(row[1])
    csv_losses.close()
    print("Voici la liste des pertes totales = ", somme)
    return somme

#Cette fonction prend en compte la variation du temps
def listerPertesTotalesLOOP(Path):
    # Change directory
    os.chdir(Path)
    Heure = 1
    List_somme=[]
    for i in range(24):
        somme = 0.0
        heure_string = str(Heure)
        with open(heure_string + "h_EXP_LOSSES.csv") as csv_losses:
            csv_reader6 = csv.reader(csv_losses, delimiter=',')
            list_iterator = iter(csv_reader6)
            next(list_iterator)
            for row in csv_reader6:
                somme = somme + float(row[1])
        csv_losses.close()

        List_somme.append(int(somme))
        Heure = Heure+1

    print("Voici la liste des pertes totales = ", List_somme)
    return List_somme
##################################################################################################
# Fonction pour trouver le nombre de surcharge dans les transfos
def SurchargeTransfos(Path):
    import math
    os.chdir(Path)
    dict = {}
    dict2 = {}
    dict3 = {}
    dict4 = {}
    with open("XFR_Loads_ckt5_results.csv") as csv_file:
        NombreTransfo = 0
        csv_reader = csv.reader(csv_file, delimiter = ';')
        for row in csv_reader:
            name = row[1]
            puissanceNominale = row[6]
            dict[name] = puissanceNominale
    csv_file.close()
    #print("Dictionnaire des transfos : ",dict)

    with open("ckt5_EXP_POWERS.csv") as file_csv:
        reader_csv = csv.reader(file_csv, delimiter = ',')
        for ROW in reader_csv:
            Booly = ROW[0].find("Transformer")
            if Booly != -1:
                NAME = ROW[0][12:]
                #J'ai fait un calcul pour obtenir la puissance apparente, ainsi je peux la comparer avec la puissance nominale du transfos (KVA)
                PUISSANCE_CONSOMMÉE = math.sqrt((float(ROW[2])**2)+(float(ROW[3])**2))
                dict2[NAME] = PUISSANCE_CONSOMMÉE #puissance apparente
    file_csv.close()
    for keys in dict2:
        for KEYS in dict:
            if keys==KEYS:
                if float(dict[KEYS])<dict2[keys]:
                    dict3[keys] = dict2[keys]
                    dict4[keys] = float(dict2[keys])-float(dict[KEYS])
                    #print("Transfos en surcharge:", keys)
                    #print("Valeurs des transfos en surcharge: ", dict2[keys])

    print("Transfos en surcharge et leur puiss apparente totale",dict3)
    print("Transfos en surcharge et diff avec puiss nominale",dict4)
    print("Nombre de transfos en surcharge : ", len(dict3))

    #Le dictionnaire dict3 indique les transformateurs en surcharge et la puissance apparente total
    #Le dictionnaire dict4 indique les transformateurs en surcharge et la puissance apparente qui dépasse la puissance nminale
    return dict3, dict4
####################################################################################################
#Transformer.MDV_SUB_1
#ckt5_EXP_Power.csv

def SubTransfoPower(Path):
    KVAR = 0.0
    KW = 0.0
    FP = 0.0
    with open("ckt5_EXP_POWERS.csv") as csv_file:
        csv_reader1 = csv.reader(csv_file, delimiter=',')
        for row in csv_reader1:
            booly = row[0].find('Transformer.MDV_SUB_1')
            if booly > -1:
                KVAR= abs(float(row[3]))
                KW = abs(float(row[2]))
                # La données de la puissance apparente n'était pas dans le fichier, je l'ai donc calculé
                KVA = math.sqrt((float(row[3])**2)+(float(row[2])**2))
                FP = abs((float(row[2]))/KVA)
                KW_IT.append(KW)
                KVAR_IT.append(KVAR)
                if KVA > 10000:
                    Surcharge = ((KVA - 10000) / 10000) * 100
                    listeSurcharge.append(Surcharge)
                    print("Sub transfos en surcharge de :", Surcharge)
                break
    csv_file.close()

    print("Puissance du transfo principal:",KW)
    print("Puissance réactive du transfo principal:", KVAR)
    print("Puissance apparente du transfo principal :", KVA)
    print("Facteur de puissance du transfo princiapl:", FP)
    return KW, KVAR, FP



####################################################################################################
# Fonction pour calculer les pertes totales dans les lignes et dans les tranfos et ce à chaque intervalle de temps
#Fonction sans la variable temps
def ListerPertesTransfoLines(Path):
    os.chdir(Path)
    sommeLine1 = 0.0
    sommeTransformer1 = 0.0
    with open("ckt5_EXP_LOSSES.csv") as csv_file:
        csv_reader1 = csv.reader(csv_file, delimiter=',')
        for row in csv_reader1:
            booly = row[0].find('Line')
            boolyTrans = row[0].find('Transformer')
            if booly != -1:
                sommeLine1 = sommeLine1 + float(row[1])
            if boolyTrans != -1:
                sommeTransformer1 = sommeTransformer1 + float(row[1])
        csv_file.close()
    print("Somme des pertes dans les Lignes = ", sommeLine1)
    print("Somme des pertes dans les Transformers = ", sommeTransformer1)
    return sommeLine1, sommeTransformer1


# Fonction avec variable temps
def listerPertesTransfoLinesLOOP(Path):
    os.chdir(Path)
    Heure = 1
    Liste_losses_transfos = []
    Liste_losses_lines = []
    for i in range(24):
        sommeLine1 = 0.0
        sommeTransformer1 = 0.0
        heure_string = str(Heure)
        with open(heure_string + "h_EXP_LOSSES.csv") as csv_file:
            csv_reader1 = csv.reader(csv_file, delimiter=',')
            for row in csv_reader1:
                booly = row[0].find('Line')
                boolyTrans = row[0].find('Transformer')
                if booly != -1:
                    sommeLine1 = sommeLine1 + float(row[1])
                if boolyTrans != -1:
                    sommeTransformer1 = sommeTransformer1 + float(row[1])
            csv_file.close()
            Liste_losses_lines.append(int(sommeLine1))
            Liste_losses_transfos.append(int(sommeTransformer1))
            Heure = Heure + 1

    print("Somme des pertes dans les Lignes = ", Liste_losses_lines)
    print("Somme des pertes dans les Transformers = ", Liste_losses_transfos)
    return Liste_losses_lines, Liste_losses_transfos


#############################################################################################
# Fonction pour plotter tous les graphes de la même façon
def Plotter_Graphes(Titre, Xaxis, Yaxis, dataX, dataY, nomFichier, SavePAth):
    from matplotlib import pyplot as plt
    fig = plt.figure()
    plt.plot(dataX, dataY, color = 'gray')
    plt.ylabel(Yaxis)
    plt.xlabel(Xaxis)
    plt.title(Titre)
    plt.show()
    fig.savefig(SavePAth + nomFichier)
    print("Figure saved at: ", SavePAth + nomFichier)

###########################################################################################
# Fonction qui save les informations dans un csv
def SaveInfoCSV(éléments_à_sauvegarder, nomDuFichier, Path):
    os.chdir(Path)
    if type(éléments_à_sauvegarder) == dict:
        with open(nomDuFichier, 'w') as file:
            writer = csv.writer(file, delimiter = ";")
            for key, val in éléments_à_sauvegarder.items():
                writer.writerow([key,val])

        print("Dictionnaire enregistré en csv sous le nom:" , nomDuFichier)
        file.close()

    if type(éléments_à_sauvegarder) == list:
        with open(nomDuFichier, 'w') as FILE:
            wr = csv.writer(FILE, quoting=csv.QUOTE_ALL)
            wr.writerow(éléments_à_sauvegarder)
        print("Liste enregistrée en csv sous le nom:", nomDuFichier)
        FILE.close()


def Monte_Carlo(liste_Valeurs):
    values = liste_Valeurs
    Moy= statistics.mean(values)
    ecart_type= statistics.stdev(values)
    int_min = Moy-2*ecart_type
    int_max = Moy+2*ecart_type
    print("95% des valeurs sont comprises entre",int_min,"et",int_max)


Heure = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]

# Il faut faire quelques petites modifs pour rendre le graphe beau et lisible
# Plotter_Graphes("Pertes de puissance dans les lignes (Simulation témoin)", "Heures", "Pertes en KW",Heure, Pertes1[0], "SimulationTPertesLignes")
# Plotter_Graphes("Pertes de puissance dans les transformateur (Simulation témoin", "Heures", "Pertes en KW", Heure, Pertes1[1], "SimulationTPertesTransfos")
# Plotter_Graphes("Pertes de puissance totale dans le réseau (Simulation témoin)", "Heures", "Pertes en KW", Heure, Pertes2, "SimulationTAllPertes")
# Plotter_Graphes("Évolution du maximum de tension sur le réseau (Simulation témoin)", "Heures", "Tension en V", Heure, Variation[0], "SimulationTMax")
# Plotter_Graphes("Évolution du minimum de tension sur le réseau (Simulation témoin)", "Heures", "Tension en V", Heure, Variation[1], "SimulationTMin")
# Plotter_Graphes("Évolution de la variation de tension sur le réseau (Simulation témoin)", "Heures", "Tension en V", Heure, Variation[2], "SimulationTVariation")




