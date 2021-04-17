# -*-coding: utf-8 -*
#!/usr/bin/python3.9

import sys

def vigenere(message, key, encryption):

    encrypted_message = ""
    decrypted_message = ""

    # Affichage de la cle et du message : 
    print("Clé donnée : " + key + " Message initiale : " + message)

    for index in range(len(message)) :

        # Caractère de la clé corespondant à la lettre du message : 
        key_char = key[index%len(key)]
        # print("Caractère du message: " + message[index] + ", de la clé : " + key_char)

        # L'entier ascii du caractère du message et de la clé.
        # Remarque : 
        # On fait le modulo afin de trouver l'emplacement correct 
        # dans l'intervalle entier [0,95] (caractère ASCII : 32 à 126 (95)).

        asciiInt_messageChar = ord(message[index])
        asciiInt_keyChar     = ord(key_char)
        # print("Unicode caractère du message: " + str(asciiInt_messageChar) + 
        # ", de la clé : " + str(asciiInt_keyChar))
        
        # Je vérifie que les caractères sont bien dans l'intervalle de l'alphabet connue : 
        if asciiInt_messageChar in range(32,127) and asciiInt_keyChar in range(32,127):
            
            # En soustrayant 32, sachant que nous sommes dans l'intervalle entier [32,127].
            # Nous ramenons unicode du caractère dans [0,95]
            asciiInt_messageChar = asciiInt_messageChar - 32
            asciiInt_keyChar     = asciiInt_keyChar - 32
            # print("Dans l'alphabet concerné caractère " + str(asciiInt_messageChar) + 
            # ", clé : " + str(asciiInt_keyChar))
            
            # Si l'utilisateur à entré "chiffrement" alors : 
            if encryption == True:
                # On enchiffre décalage en ajoutant le rang du caractère de la clé :
                encrypted_message += chr(32 + (asciiInt_messageChar + asciiInt_keyChar)%95)
            # Sinon si l'utilisateur à entré "dechiffrement" alors : 
            elif encryption == False:
                # On dechiffre décalage soustrayant le rang du caractère de la clé :
                decrypted_message += chr(32 + (asciiInt_messageChar - asciiInt_keyChar)%95)

                # Remarque : 
                # On fait le modulo afin de trouver l'emplacement correct 
                # dans l'intervalle entier [0,95] (caractère ASCII : 32 à 126 (95)).

        else:
            print ("\"" + message[index] + "\"" + " ou " + "\"" + key_char + "\"" + " ne se trouve pas dans " +
            "l'alphabet de ce chiffrement de Vigenère.")
            print("Pour rappel, alphabet connue est l'intervalle entier [32,126] de la table ASCII.")
            break

    if(encryption == True):
        print("Chiffrement terminé avec succès ! ")
        print("Message initial : " + message)
        print("Message chiffré : " + encrypted_message)
        return encrypted_message
    elif(encryption == False):
        print("Déchiffrement terminé avec succès ! ")
        print("Message chiffré : " + message)
        print("Message déchiffré : " + decrypted_message)
        return decrypted_message

    return None

    # ord(c) Renvoie le nombre entier représentant le code Unicode du caractère 
    # chr(i)Renvoie la chaîne représentant un caractère dont le code de caractère Unicode 
    # est le nombre entier i.


##################
# Méthode MAIN : #
##################
# Debut_Main
if __name__ == "__main__":
    if len(sys.argv)!=3:
        # print("\nNombre d'arguments : " + str(len(sys.argv)))
        print("Utilisation des commandes : <-c ou -d> <clé> ")
        print("Options :")
        print("clé : chaine de caractères de la table ASCII [32, 126]\n "+
        "-c : \"chiffrement\" ou -d : \"dechiffrement\"")
    else:
        arg = sys.argv[1:]
        encryption = str(arg[0])
        cle = str(arg[1])
        message = input("Entrer le message : \n")
        # print(f'Le message a chiffrer est : {message}')
        if encryption == "-c":
            encryption = True
            vigenere(message, cle, encryption)
        elif encryption == "-d":
            encryption = False
            vigenere(message, cle, encryption)
        else:
            print("Mauvaise utilisation de la commande.")
            print("Pour voir les utilisations, lancer le programme sans aucun paramètre")
# Fin_Main