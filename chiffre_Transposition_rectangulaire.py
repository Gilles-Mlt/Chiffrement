# -*-coding: utf-8 -*
#!/usr/bin/python3.9

import sys
import random
import pandas as pd
from collections import Counter

def rankof(character): 
    # print("Caractère du message: " + character)
    asciiInt_character = ord(character)
    # print("Unicode caractère du message: " + str(asciiInt_character))
    # Je vérifie que les caractères sont bien dans l'intervalle de l'alphabet connue : 
    if asciiInt_character in range(32,127):
        # En soustrayant 32, sachant que nous sommes dans l'intervalle entier [32,127].
        # Nous ramenons unicode du caractère dans [0,95]
        asciiInt_character = asciiInt_character - 32
        # print("Dans l'alphabet concerné caractère " + str(asciiInt_character))
        return asciiInt_character
    else:
        print("Le caractère ne faire pas partie de l'alphabet connue")
        return None

def transfomation_rectangulaire(key, message, encryption):
    
    print("\n#########################################################")
    print("# Integration et numerotation de la cle dans le tableau #" )
    print("#########################################################\n")
    print("Initialisation des colonnes de la premiere ligne de mon tableau avec les caracteres de la cle.")
    # Je récupère, le rang ASCII de la clé dans columns_names :
    columns_names = []
    for index in key:
        columns_names.append((index, rankof(index)))

    # Je tris
    columns_names_sorted = sorted(columns_names)

    # En fonction du range ASCII je numérote de 1 à la longeur de la clé :
    for index in range(0,len(key)):
        a,b  = columns_names_sorted[index]
        columns_names_sorted[index] = (a, index + 1)
    print(columns_names_sorted)

    # Je fais la correspondance entre mest colonne trié et mon tableau réel, 
    # afin de passé le rang [1, len(key)] aux vraies nom de colonnes, columns_names :
    for index in range(0,len(key)):
        character_sorted, rank_sorted = columns_names_sorted[index]
        print(columns_names_sorted[index])
        for i in range(0,len(key)):
            character, rank  = columns_names[i]
            # Si le caractère est également et que le rang est différent du rang trié -1,
            # je fais l'association. On peut faire ça car les lettre identique sont numéroté 
            # l'une à la suite de l'autre.
            if character == character_sorted and rank != rank_sorted-1:
                columns_names[i] = columns_names_sorted[index]
                # Dès que j'ai trouvé la correspondance j'arrête.
                break

    print(columns_names)
    dataFrame = pd.DataFrame(columns=columns_names)

    print("Mes colonnes sont ainsi initialisees : ")
    print(dataFrame)
    # a, b = dataFrame.columns[0]
    # print(a)

    # print("\n##########################")
    # print("# Numerotation de la cle #" )
    # print("##########################\n")

    # frequence = Counter(message)
    # print(frequence['i'])
    # table = []
    # position = 1
    # for index in key: 
    #     table.append([index,position])
    #     position += 1
    # print(table)
    # # frequence = Counter(text)
    if encryption == True :
        print("\n##########################################")
        print("# Verification de la longueur du message #" )
        print("##########################################\n")

        print("Verifions si une transformation du message est necessaire.")
        print(" Le message initial a une longeur de : %d" %(len(message)))
        if len(message)%(len(key))!= 0:
            reste = len(message)%(len(key))
            nb_spce_add = len(key) - reste
            print("Une transformation est ici necessaire.")
            print("Nous allons ajouter %d blanc au message afin que le reste soit de 0." %nb_spce_add)
            print("(Les blanc ne sont biensûre pas comptabilise, mais utile au remplissage en ligne)")
            for index in range(0, nb_spce_add):
                message += " "
            # print("Le message a maintenant une longueur de : %d" %(len(message)))

        print("\n#####################################")
        print("# Integration du message au tableau #" )
        print("#####################################\n")
        # J'ai ajouté des blancs si nécessaire pour pouvoir directement 
        # remplir la dataframe, avec un nombre de colonne toujours identiques.
        # Sinon il y avait une levé d'erreur.
        copy_message = message 
        while copy_message != "":
            add_to_tab = []
            for index in range(0,len(key)):
                add_to_tab.append(copy_message[0])
                copy_message = copy_message.removeprefix(copy_message[0])
            # print("La longueur de mon tableau temporaire est %d :" %(len(add_to_tab)))
            df_temp = pd.DataFrame([add_to_tab], columns = columns_names)
            dataFrame = pd.concat([dataFrame, df_temp], ignore_index=True, axis = 0)
        print("Affichage de mon tableau :" )
        print(dataFrame)
        # df.iloc[1:3, 0:3]

        print("\n##############################")
        print("# Chiffrage :                #" )
        print("##############################\n")
        # Ici je récupère en fonction de mes colonnes trié les caractères
        # de la colonnes adéquat (1,2,3...) que j'ajoute à message_encrypted.
        message_encrypted =""
        for index in range(0,len(key)):
            for i in range(0,len(key)):
                if columns_names_sorted[index] == columns_names[i]:
                    for j in range(0,len(dataFrame.iloc[:,i])):
                        # df.values.tolist(dataFrame.iloc[:,i]) 
                        message_encrypted += str(dataFrame.iloc[j,i])
                        message_encrypted = message_encrypted.replace(" ", "")
        print("Message initiale : " + message)
        print("Message chiffre :  " + message_encrypted + "\n")

    elif encryption == False : 
        print("\nInformation lie au dechiffrage : ")
        print("*La longueur du message est : %d" %len(message))
        print("*La longueur de la cle est : %d" %len(key))
        q = len(message)//len(key)
        r = len(message)%len(key)
        if r == 0:
            print("*Nous aurons un tableau de %d colonnes et elles auront une hauteur de %d." %(len(key), q))
        elif r != 0:
            dataFrame = pd.DataFrame(columns=[columns_names], index = range(0,q+1))
            print("*Nous aurons un tableau de %d colonnes, tel que les %d premieres colonnes, " %(len(key), r)
            + "\nont une hauteur de %d et les %d dernieres, auront une hauteur de  %d." % (q+1,len(key)-r, q))

        print("\n#####################################")
        print("# Integration du message au tableau #" )
        print("#####################################\n")
        # Ici je remplis plus ou moins la Dataframe en fonction de r (reste).
        # Tant quand i < au reste les colonne on leur taille max.
        # Dans le cas contraire elles ont une hauteur en moins.
        copy_message = message
        message_decrypted =""
        for index in range(0,len(key)):
            for i in range(0,len(key)):
                if columns_names_sorted[index] == columns_names[i]:
                    add_to_tab  = []
                    if i < r :
                        hauteur = range(0,q+1)
                    elif i >= r :
                        hauteur = range(0,q)
                    for j in hauteur :
                        add_to_tab.append(copy_message[0])
                        copy_message = copy_message.removeprefix(copy_message[0])
                    serie = pd.Series(data=add_to_tab, index=hauteur)
                    dataFrame[dataFrame.columns[i]] = serie

        print("Ma dataframe est :")
        print(dataFrame)

        print("\n##############################")
        print("# dehiffrage :                #" )
        print("##############################\n")
        # Je lis la Dataframe dans sa longueur dès qu'un caractère est > 1 j'arrête.
        for index in range(0,len(dataFrame.index)):
                for i in range(0,len(key)):
                    if len(str(dataFrame.iloc[index,i])) > 1:
                        break
                    message_decrypted += str(dataFrame.iloc[index,i])

        print("Message a dechiffre est :  " + message)
        print("Le message dechiffre est : " + message_decrypted + "\n")

                        # for j in range(0,len(dataFrame.iloc[:,i])):
                        # df.values.tolist(dataFrame.iloc[:,i]) 
                        # message_encrypted += str(dataFrame.iloc[j,i])
                        # message_encrypted = message_encrypted.replace(" ", "")
        # print("Message initiale : " + message)
        # print("Message chiffre :  " + message_encrypted)
# 
# 
        # for index in range(0,r) :
            # add_to_tab  = []
            # for i in range(0,q+1) :
                # add_to_tab.append(copy_message[0])
                # copy_message = copy_message.removeprefix(copy_message[0])
        # serie = pd.Series(data=add_to_tab, index=range(0,q+1))
            # print(serie)
            # dataFrame = pd.concat([dataFrame, serie], ignore_index=True, axis = 1)
            # df_temp = pd.DataFrame([add_to_tab], orient = 'index', columns = columns_names)

##################
# Méthode MAIN : #
##################
# Debut_Main
if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("\nUtilisation des commandes : <-c ou -d> <clé>")
        print("Options :")
        print("-c : \"chiffrement\" ou -d : \"dechiffrement\" " +
            "clé : chaines de caractères ASCII [32,126]\n")
    else:
        arg = sys.argv[1:]
        encryption = str(arg[0])
        key = str(arg[1])
        message = input("\nEntre le message : \n")
        message = message.replace(" ", "")
        print(f'En enlevant les espaces le message est : {message}')
        if encryption == "-c":
            encryption = True
            transfomation_rectangulaire(key, message, encryption)
        elif encryption == "-d":
            encryption = False
            transfomation_rectangulaire(key, message, encryption)
        else:
            print("\nMauvaise utilisation de la commande.")
            print("Pour voir les utilisations, lancer le programme sans aucun paramètre.\n")

# Fin_Main