# -*-coding: utf-8 -*
#!/usr/bin/python3.9

import sys
import random
# import pandas as pd

###########################################################
#  ======>>>>  <<<<======#
###########################################################

def inverse_mod(a, b):
    # Calcule l'inverse de a modulo b via l'algorithme d'euclide etendu
    d,u,v,d1,u1,v1 = a,1,0,b,0,1
    # Calcul
    while d1!=0:
        q = d//d1
        d,u,v,d1,u1,v1 = d1,u1,v1,d-q*d1,u-q*u1,v-q*v1
    # print ('pgcd(%d,%d) = %d' % (a,b,d))
    # print("Valeur de u : %d" %u)
    if u>=0:
        # print ('(%d)*%d + (%d)*%d = %d' %(u,a,v,b,d))
        return u
    else :
        # print ('(%d)*%d + (%d)*%d = %d' %(b+u,a,v1+v,b,d))
        return b+u

###########################################################
#  ======>>>> Ajouter un else au if de rankOf() <<<<======#
###########################################################

def rankOf(character): 
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

##################################################################
#  ======>>>>  <<<<======#
##################################################################

def hill(m, a, b, c, d, message, encryption):

    encrypted_message = ""
    decrypted_message = ""

    liste_lettres_rares = ['z','w','k','j','q','x','y']

    # Affichage du message : 
    print("\n################")
    print("# Paramètres : #")
    print("################\n")

    print("Les paramètres pris en compte pour le chiffrage sont : \n")

    print("Séparation en bloque de : %d " %m)
    if m != 2:
        print("m est différent de 2 le programme ne fonctionnera pas.\n")
        return None
    print("Valeur du paramètre a : %d" %a)
    print("Valeur du paramètre b : %d" %b)
    print("Valeur du paramètre c : %d" %c)
    print("Valeur du paramètre d : %d" %d)
    print("Message initiale : " + message + "\n")

    print("\n###########################################")
    print("# Vérification de la convenance de la clé : #")
    print("#############################################\n")

    determinant = int(a) * int(d) - int(c) * int(b) 
    print("Le déterminant vaut : %d" %determinant)
    print("Vérifions si ce dernier est divisible par 5 ou 19 (5x19 = 95)")

    if determinant%5 == 0 or determinant%19 == 0:
        print("\n /!\ LA MATRICE COMPOSE DE a b c d NE CONVIENT PAS, ELLE EST DIVISIBLE PAR 5 OU 19 /!\ ")
        return None
    elif determinant%5 != 0 and determinant%19 != 0:
        print ("La matrice convient !")

    print("\n################################")
    print("# Vérification message paire : #")
    print("################################\n")

    print("Vérifions si la longueur du message est paire : ")
    if (len(message)%2 == 0):
        print("La longueur du message est paire, pas de lettre rare à ajouter.\n")
    elif (len(message)%2 == 1):
        print("\n/!\ LA LONGUEUR DU MESSAGE EST ICI IMPAIRE /!\ \n")
        if encryption == True:
            random_index = random.randint(0, len(liste_lettres_rares))
            lettre_rare = liste_lettres_rares[random_index]
            print("Nous ajoutons la lettre rare : " + lettre_rare + ", afin d'en faire un message paire.")
            message = message + lettre_rare
            print("Le message à chiffrer est maintenant : " + message)
        elif encryption == False:
            print("Le message à déchiffrer est impaire cela ne peux pas provenir d'un chiffrement de Hill " 
            + " avec m = 2 \n \n Fin de l'éxécution du programme... \n")

    if encryption == True :
        print("\n###############")
        print("# Chiffrage : #")
        print("###############\n")
    
    elif encryption == False:
    
        print("\n###############")
        print("# Déhiffrage : #")
        print("###############\n")

        print("Calcule de l'inverse de A dans Z/26/Z : ")
        u = inverse_mod(determinant,95)
        print("Le u trouvé est : %d" %u)
        print("Les composants de l'inverse de A sont :")
        print("a = %d" %(u * d))
        print("b = %d" %(u * (-b)))
        print("c = %d" %(u * (-c)))
        print("d = %d" %(u * a))
        # x1 = (u * d)* - (u * (-b))* 
        # x2 = (u * (-c))* - (u * a)*

    while message != "":

        character_tuple = []
        print ("Application, par bloque de 2 : \n")
        for index in range(0,2) :
            # Rang du caractère : 
            index_rank  = rankOf(message[index])
            print("Le rang dans notre alphabet du caractere : " 
                + message[index] + " est " + str(index_rank))

            # Ajout à ma liste de caractère : 
            character_tuple.append(index_rank)

        if encryption == True :
            # Application de mes équations Hill : 
            print("\nCalcul des valeurs de y1 et y2 : ")
            y1 = int(a) * int(character_tuple[0]) + int(b) * int(character_tuple[1])
            y2  = int(c) * int(character_tuple[0]) + int(d) * int(character_tuple[1])
            print ("Valeur de y1 = " + str(y1) + " et de y2 : " + str(y2))
            #Ajout de me mes 2 caractères chiffré à mon message chiffré :
            encrypted_message += str(chr(32 + y1%95)) 
            encrypted_message += str(chr(32 + y2%95))
        
        elif encryption == False:
            # Application de mes équations Hill : 
            print("\nCalcul des valeurs de x1 et x2 : ")
            x1 = int((u * d)) * int(character_tuple[0]) + int(u * (-b)) * int(character_tuple[1])
            x2  = int(u * (-c)) * int(character_tuple[0]) + int(u * a) * int(character_tuple[1])
            print ("Valeur de x1 = %d et de x2 : %d" %(x1,x2))
            #Ajout de me mes 2 caractères chiffré à mon message chiffré :
            decrypted_message += str(chr(32 + x1%95)) 
            decrypted_message += str(chr(32 + x2%95))

        message = message.removeprefix(message[0:2])
        print("\nMon message initial, est maintenant: " + message)
        
        if encryption == True :
            print("Mon message chiffré est actuellement : " + encrypted_message +"\n")
        elif encryption == False :
            print("Mon message dechiffré est actuellement : " + decrypted_message +"\n")
    
    if encryption == True :
        print("\nMon message chiffré final est : " + encrypted_message)
    elif encryption == False :
        print("\nMon message dechiffré final est : " + decrypted_message)

##################
# Méthode MAIN : #
##################
# Debut_Main
if __name__ == "__main__":
    if len(sys.argv)!=7:
        print("\nUtilisation des commandes : <-c ou -d> <m> <a> <b> <c> <d> ")
        print("Options :")
        print("-c : \"chiffrement\" ou -d : \"dechiffrement\". \nm = 2 (uniquement).\n" +
            "a, b, c, d = nombres entiers.\n")

    else:
        arg = sys.argv[1:]
        encryption = str(arg[0])
        m = int(arg[1])
        a = int(arg[2])
        b = int(arg[3])
        c = int(arg[4])
        d = int(arg[5])
        message = input("Entre le message : \n")
        print(f'Le message entré est : {message}')
        if encryption == "-c":
            encryption = True
            print("Quel est le message à chiffrer ?")
            hill(m, a, b, c, d, message, encryption)
        elif encryption == "-d":
            encryption = False
            hill(m, a, b, c, d, message, encryption)
        else:
            print("\nMauvaise utilisation de la commande.")
            print("Pour voir les utilisations, lancer le programme sans aucun paramètre.\n")

# Fin_Main