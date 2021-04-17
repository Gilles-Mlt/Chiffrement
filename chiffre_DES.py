# -*-coding: utf-8 -*
#!/usr/bin/python3.9

import sys
# import string
import operator

# Permutation tables and Sboxes
IP = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9,  1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
)
IP_INV = (
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
)
PC1 = (
    57, 49, 41, 33, 25, 17, 9,
    1,  58, 50, 42, 34, 26, 18,
    10, 2,  59, 51, 43, 35, 27,
    19, 11, 3,  60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7,  62, 54, 46, 38, 30, 22,
    14, 6,  61, 53, 45, 37, 29,
    21, 13, 5,  28, 20, 12, 4
)
PC2 = (
    14, 17, 11, 24, 1,  5,
    3,  28, 15, 6,  21, 10,
    23, 19, 12, 4,  26, 8,
    16, 7,  27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
)

E  = (
    32, 1,  2,  3,  4,  5,
    4,  5,  6,  7,  8,  9,
    8,  9,  10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
)

Sboxes = {
    0: (
        14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
        0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
        4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
        15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
    ),
    1: (
        15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
        3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
        0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
        13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9 
    ),
    2: (
        10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
        13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
        13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
        1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12 
    ),
    3: (
        7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
        13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
        10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
        3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
    ),
    4: (
        2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
        14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
        4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
        11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
    ),
    5: (
        12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
        10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
        9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
        4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
    ),
    6: (
        4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
        13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
        1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
        6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
    ),
    7: (
        13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
        1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
        7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
        2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
    )
}

P = (
    16,  7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11, 4,  25
)

def binary_tranformation(string):  
    string = bin(int(string, 16)).removeprefix("0b")
    string = string.zfill(64)
    return string

def group_of4(string):
    table = [x for x in range(80) if x%5==0]
    # table.remove(0)
    # print(table)
    for index in table:
        sub_string_temp1 = string[0 : index + 4]
        sub_string_temp2 = string[index + 4 : len(string)]
        string = sub_string_temp1 + " " + sub_string_temp2
    print("L'affichage par groupement de 4 donne : \n%s\n" %string)
    return string

def permutation_by_table(block, table):
    perm = []
    for pos in range(0,len(table)):
        perm.append(block[table[pos]-1])
    return ''.join(perm)

def generate_sub_keys(C0, D0):
    # Tableau qui va acceuillir mes Ki clées i appartenant à [1,16]
    sub_keys  = []
    # C0 28 premiers bits de K (la clé principale).
    C = C0
    # D0 28 derniers bits de K.
    D = D0
    for index in range(1,17):
        # Pour les valeur de [1,2,9,16] une seule rotation à gauche.
        if index in [1,2,9,16]:
            # Récupération du 1er caractère
            temp = [C[0], D[0]]
            # Je récupère le reste hormis le 1er :
            reste = [C[1:28], D[1:28]]
            # J'ajoute le 1er caractère à la fin :
            C = reste[0] + temp[0]
            D = reste[1] + temp[1]
        # 2 rotation à gauche sinon.
        else:
            # Ici je prends les 2 premiers :
            temp = [C[0:2], D[0:2]]
            reste = [C[2:28], D[2:28]]
            # Que j'ajoute à la fin :
            C = reste[0] + temp[0]
            D = reste[1] + temp[1]
        # Je concatène C e t D
        CD = C + D
        # J'applique PC2 et je stockes
        sub_keys.append(permutation_by_table(CD, PC2))
    return sub_keys

    # rotg = lambda b, k, n: ((b << k) | (b >> (n-k))) & ((1<<n)-1)
    # Explication de ma fonction anonyme pour décalage d'une position à gauche: 
        # Je fais un décalage à gauche d'une position de l'ensemble j'obtiens la même chaine
        # avec un 0 tout à droite.
        # Je décale ensuite l'ensemble-1 à droite il me restera une série de 0 et 
        # comme caractère toute à droite, le premier caractère de ma chaine. Car j'ai fais 
        # l'ensemble-1.
        # Lorsque je fais un ou logique entre les deux chaines précédentes, j'obtiens 
        # la valeur de la position 1 ajouté en dernière position. Mais j'ai toujours mon premier 
        # caractère en première position.
        # Lorsque je fais un et logique entre la chaine obtenue qui a en plus sa premiere valeur
        # ajouter à la fin et une chaine de même taille composé uniquement de 1 sauf à la première
        # position où j'ai un 0.
        # J'obtiens le décalage à gauche avec une récupération de la première valeur à droite
        # C = int(1110000011011000101101000001,2)
        
        # Exemple à la main pour plus de précision: 
            # print(bin(C << 1) + " (1)" )
            # print(bin(C >> (len(C0)-1)) + " (2) (les zéros à gauche ne s'affiche pas)" )
            # print(bin((C << 1) | (C >> (len(C0)-1))) + " (3) avec (1) ou (2) = (3)")
            # print(bin((1<<len(C0))-1)+ "(4)")
            # print(bin(((C << 1) | (C >> (len(C0)-1))) & ((1<<len(C0))-1))+ "(5) avec (3) & (4) = (5)")

def confusion_function(Ri,Ki):
    # J'applique la fonction d'expansion E à Ri :
    E_Ri =  permutation_by_table(Ri, E)
    print("1) Application de la fonction d'expansion E à D :")
    print("E(D) = %s" %E_Ri)
    # J'obtiens B par l'opération ou exclusif entre E_Ri et Ki
    B = operator.xor (int(E_Ri,2), int(Ki,2))
    B = bin(B).removeprefix("0b")
    B = B.zfill(48)
    print("\n2) Ou exclusif entre E(D) et K : ")
    print("B = E(D)⊕K  = %s" % B)
    print("Taille de B : %d bits" %(len(B)))
    print("\nDécoupage de B en 8 chaines de 6 bits : ")
    B_copy = B
    Bi = []
    for index in range(0,8):
        # Je récupère les 6 premiers bits :
        Bi.append(B_copy[0:6])
        print("B%d = %s" %(index,B_copy[0:6]))
        # Je B_copy  = B_copie - les 6 premiers bits :
        B_copy = B_copy[6:]

    print("\nA la sortie des Sboxes, nous obtenons les Ci : ")
    Ci = []
    for index in range(0,len(Bi)):
        # Ligne  = 1er bit + dernier bit
        row = int(Bi[index][0] + Bi[index][-1],2)
        # Colonne = 4 bit du milieu [1,2,3,4]
        col = int(Bi[index][1:5],2)
        Sboxe = bin(Sboxes[index][16*row+col]).removeprefix("0b")
        Sboxe = Sboxe.zfill(4)
        Ci.append(Sboxe)
        print("C%d = %s"%(index+1, Sboxe))
    # C est la concaténation de tous les Ci :
    C = ''.join(Ci)

    print("\nLa concaténation de tous les Ci donne C :")
    print("C = %s" %C)
    print("Taille de C : %d bits\n" %len(C))

    print("On applique la permutation P et C devient :")
    P_C = permutation_by_table(C, P)
    print("P(C) = %s\n" %P_C)
    return P_C

def des(key, message, encryption):
    # Affichage du message : 
    print("\n#################################")
    print("# Verification des longueurs : #")
    print("#################################\n")

    print("* Pour la cle : \n")
    key_hex = hex(int(key, 16))
    key = binary_tranformation(key)
    print("La clé principale en hexadecimal est : \n%s" %key_hex)
    print("La clé principale en binaire est : \n%s\n" %key)
    print("Et elle comporte %d bits.\n" %len(key))
    group_of4(key)
    print("------------------------------------------------------\n")
    
    print("* Pour le message : \n")
    message_hex = hex(int(message, 16))
    message_binary = binary_tranformation(message)
    print("Le message en hexadecimal est :\n%s" %message_hex)
    print("Le message en binaire est : \n%s\n" %message_binary)
    print("Et il comporte %d bits.\n" %len(message_binary))
    group_of4(message_binary)

    print("\n######################")
    print("# Calcule des cles : #")
    print("######################\n")

    print("K = %s" %key)
    C0D0 = permutation_by_table(key,PC1) 
    print("PC1(K) = C0D0 = %s\n" %C0D0)
    print ("Longueur de C0D0 : %d bits (8 bits de contrôles)\n" %len(C0D0))
    group_of4(C0D0)

    print("La séparation donne :")
    C0 = C0D0[0 : len(C0D0)//2]
    D0 = C0D0[len(C0D0)//2 : len(C0D0)]
    print("C0  = %s \nD0  = %s" %(C0, D0))
    print("C0 : %d bits et D0 : %d bits."%(len(C0),len(D0)))
    print("\nCalcule des  16 sous clées à l'aide de PC2...\n")
    sub_keys = generate_sub_keys(C0, D0)

    print("Les sous clées sont : ")
    for index in range(0,  len(sub_keys)):
        print("PC2(C%2dD%2d) = K%2d = %s" %(index + 1,index + 1,index + 1, sub_keys[index]))
    
##################
# Chiffrement :  #
##################
    if encryption == True :
        print("\n##########################")
        print("# Permutation initiale : #")
        print("##########################\n")

        Y = permutation_by_table(message_binary, IP)
        print("On obtient :\nY = L0R0 = %s" %Y)
        print("Affichage en hexadécimal : %s" %hex(int(Y,2)))
        group_of4(Y)

        print("De cette permutation initiale nous obtenons : L0 et R0")
        L0 = Y[0 : len(Y)//2]
        R0 = Y[len(Y)//2 : len(Y)]
        print(len(L0))
        print(len(R0))
        print ("L0 = %s\nR0 = %s\n" %(L0, R0))

        print("\n###########################")
        print("# Fonction de confusion : #")
        print("##########################\n")
        left  = L0
        right = R0
        print("Les 16 itérations donnes : \n")
        for index in range(0,16):
            print("*Itération %d : \n" %(index+1))
            P_C = confusion_function(right,sub_keys[index])
            right1 = operator.xor(int(left,2),int(P_C,2))
            right1 = bin(right1).removeprefix("0b")
            right1 = right1.zfill(32)
            # L1  = R0
            left  = right
            right = right1
            print("L%d = %s "%(index+1, left))
            print("L%d = %s "%(index+1, hex(int(left,2))))
            print("R%d = %s "%(index+1, right))
            print("R%d = %s "%(index+1, hex(int(right,2))))
            print("-------------------------------------------------")

        # B = operator.xor (int(E_Ri,2), int(Ki,2))
        # B = bin(B).removeprefix("0b")
        # B = B.zfill(len(Ki))

        # P_C = confusion_function(R0,sub_keys[0])
        # R1  = operator.xor(L0,P_C)
        # L1  = R0
        # P_C = confusion_function(R1,sub_keys[1])
        # R2  = operator.xor(L1,P_C)
        # L2  = R1
        # P_C = confusion_function(R2,sub_keys[2])
        # R3  = operator.xor(L2,P_C)
        # L3  = R2
        # P_C = confusion_function(R3,sub_keys[2])
        # R4  = operator.xor(L3,P_C)

        print("\n##########################")
        print("# Permutation finale : #")
        print("##########################\n")

        message_encrypted = permutation_by_table(left + right, IP_INV)
        print("Le message obtenue suite à la permutation finale est le message chiffré.\n\n"
        +  "Message chiffré : %s" % message_encrypted)
        print("Taille du message chiffré binaire: %d\n" %len(message_encrypted))
        print("En hexadecimal  : %s" % hex(int(message_encrypted,2)))
        print("Taille du message hexadécimal : %d\n" %(len(hex(int(message_encrypted,2)))-2))

##################
# Déchiffrement :#
##################
    elif encryption == False :
        print("\n**** DECHIFFREMENT ****** \n")
        print("J'applique  IP au message, IP(m) = L16R16.")
        L16R16 = permutation_by_table(message_binary,IP)
        print("L16R16 = %s" %L16R16)
        print(" Taille de L16R16 = %d bits\n" %len(L16R16))
        
        L16 = L16R16[0:len(L16R16)//2]
        R16 = L16R16[len(L16R16)//2:]
        print("Je sépares et j'obtiens :\nL16 = %s\nR16 = %s" %(L16, R16))
        print("Taille de L16 : %d bits, taille de R16 : %d bits.\n"%(len(L16), len(R16)))
        print("Ayant mes sous-clées, je fait l'inverse des inversion 16 fois.\n")

        # initialement R = R16 et L1  = L16
        # L = xor(confusion_function(L1, Ki), R)
        # R = L1
        # L1 = L

        left1  = L16
        right = R16

        # L'inversement du XOR est un XOR, donc on peut convenablement inversé les itérations.
        # J'ai laissé pour plus de détail les commentaires du dessous qui montre,
        #  comment j'ai trouvé l'inversement entre Left et Right pour la remonté.
        for index in range(0,16):
            print("*Itération %d : \n" %(16-index))
            P_C = confusion_function(left1,sub_keys[15-index])
            print(15-index)
            left = operator.xor(int(P_C,2), int(right,2))
            left = bin(left).removeprefix("0b")
            left = left.zfill(32)
            right = left1
            left1 = left

            print("L%d = %s "%(15-index, left1))
            print("L%d = %s "%(15-index, hex(int(left1,2))))
            print("R%d = %s "%(15-index, right))
            print("R%d = %s "%(15-index, hex(int(right,2))))
            print("-------------------------------------------------")

        # L16
        # R16

        # # R15 = L16                  L16
        # L15 = xor(confusion_function(R15, K16), R16)
        # R15 = L16

        # # R14 = L15                  L15
        # L14 = xor(confusion_function(R14, K15), R15)
        # R14 = L15                    L15

        # # R13 = L14
        # L13 = xor(confusion_function(R13, K14), R14)
        # R13 = L14                    L14

        # Boucle for  :
        # initialement R = R16 et L1  = L16
        # L = xor(confusion_function(L1, Ki), R)
        # R = L1
        # L1 = L

        L0R0 = left1 + right
        print("\nA la suite des 16 permutations, j'obtiens L0R0 :\nL0R0 = %s"%L0R0)
        print("L0R0 en hexadecimal : %s" %hex(int(L0R0,2)))
        print("Puis j'applique IP_INV(L0R0) = message.")
        message = permutation_by_table(L0R0, IP_INV)
        print("\nLe message initiale est en binaire : %s" %message)
        print("Taille de message en bin: %d" %len(message))
        print("\nLe message initiale est en hexadecimale : %s" %hex(int(message,2)))
        print("Taille de message en hexa: %d\n" %len(hex(int(message,2))))

##################
# Méthode MAIN : #
##################
# Debut_Main
if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("\nUtilisation des commandes : <-c ou -d> <clé >")
        print("Options :")
        print("-c : \"chiffrement\" ou -d : \"dechiffrement\" " +
            "clé : chaine hexadimal de taille 16 sans spécifier 0x\n")
    else:
        arg = sys.argv[1:]
        encryption = str(arg[0])
        # encryption = "dechiffrement"
        key = str(arg[1])
        # key = "133457799BBCDFF1"
        # message = "0123456789ABCDEF"
        # message = "4ad423a80f05780a"
        message = input("Entre le message en hexadecimal de taille 16 sans 0x: \n")
        # print(f'Le message a chiffrer est : {message}')

        if encryption == "-c":
            encryption = True
        elif encryption == "-d":
            encryption = False
        else:
            print("\nMauvaise utilisation de la commande.")
            print("Pour voir les utilisations, lancer le programme sans aucun paramètre.\n")

        des(key, message, encryption)
# Fin_Main


