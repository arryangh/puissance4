

def afficherMatrice(matrice):
    for i in range(0, len(matrice)):
        for j in range(0, len(matrice[0])):
            if j==0:
                print(f"[{matrice[i][j]:2d}, ", end="")
            if (j>0 and j<(len(matrice[0]))-1):
                print(f"{matrice[i][j]:2d}, ", end="")
            if j==len(matrice[0])-1:
                print(f"{matrice[i][j]:2d}]", end="")
        print("")
def createMatrice():
    matrice = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

    taille_x = len(matrice)
    taille_y = len(matrice[0])
    n = 1
    for i in range(0, taille_x):
        for j in range(0, taille_y):
            matrice[i][j] = n
            n += 1
    return matrice

def f_sans_nb(matrice):
    taille_x = len(matrice)
    taille_y = len(matrice[0])

    def ligne():
        for i in range(0, taille_y):
            for j in range(0, taille_x-3):
                print(f"{matrice[i][j]}, {matrice[i][j+1]}, {matrice[i][j+2]}, {matrice[i][j+3]}")

    def colonne():
        for i in range(0, taille_y):
            for j in range(0, taille_x-3):
                print(f"{matrice[j][i]}, {matrice[j+1][i]}, {matrice[j+2][i]}, {matrice[j+3][i]}")

    def diagonal():
        for i in range(0, taille_x-3):
            for j in range(0, taille_y-3):
                print(f"{matrice[i][j]}, {matrice[i+1][j+1]}, {matrice[i+2][j+2]}, {matrice[i+3][j+3]}")

    def antidiagonal():
        for i in range(0, taille_x-3):
            for j in range(3, taille_y):
                print(f"{matrice[i][j]}, {matrice[i+1][j-1]}, {matrice[i+2][j-2]}, {matrice[i+3][j-3]}")

    # ligne()
    # colonne()
    diagonal()
    # antidiagonal()


def f_nonFactorise(matrice):
    taille_x = len(matrice)
    taille_y = len(matrice[0])
    nb = 4 # nb jeton à aligner

    def ligne():
        for i in range(0, taille_x):  # i = lignes
            for j in range(0, taille_y - nb + 1):  # j = colonnes
                sum = 0
                for k in range(0, nb):
                    if (k < nb - 1):
                        print(f"{matrice[i][j + k]:3d}", end="")
                    else:
                        print(f"{matrice[i][j + k]:3d}")

                    sum += matrice[i][j + k]

                if sum == nb:
                    return 1  # joueur 1 gagne
                if sum == -nb:
                    return -1  # joueur -1 gagne

        return 0

    def colonne():
        for i in range(0, taille_x - nb + 1):  # i = lignes
            for j in range(0, taille_y):  # j = colonnes
                sum = 0
                for k in range(0, nb):
                    if (k < nb - 1):
                        print(f"{matrice[i + k][j]:3d}", end="")
                    else:
                        print(f"{matrice[i + k][j]:3d}")

                    sum += matrice[i + k][j]

                if sum == nb:
                    return 1
                if sum == -nb:
                    return -1

        return 0

    def diagonal():
        for i in range(0, taille_x - nb+1):
            for j in range(0, taille_y - nb+1):
                # print(f"{matrice[i][j]}, {matrice[i+1][j+1]}, {matrice[i+2][j+2]}, {matrice[i+3][j+3]}")
                # for k in range(0, nb):
                #     print(f"{matrice[i+k][j+k]:3d}", end="")
                # print("")

                sum = 0
                for k in range(0, nb):
                    if (k < nb - 1):
                        print(f"{matrice[i+k][j+k]:3d}", end="")
                    else:
                        print(f"{matrice[i+k][j+k]:3d}")

                    sum += matrice[i+k][j+k]
                    if (sum == 1 * nb):
                        return 1  # 1 a gagné
                    if (sum == -1 * nb):
                        return -1  # -1 a gagné

        return 0  # pas de gain

    def antidiagonal():
        for i in range(0, taille_x-nb+1):
            for j in range(nb-1, taille_y):
                # print(f"{matrice[i][j]}, {matrice[i+1][j-1]}, {matrice[i+2][j-2]}, {matrice[i+3][j-3]}")
                # for k in range(0, nb):
                #     print(f"{matrice[i+k][j-k]:3d}", end="")
                # print("")

                sum = 0
                for k in range(0, nb):
                    if (k < nb - 1):
                        print(f"{matrice[i+k][j-k]:3d}", end="")
                    else:
                        print(f"{matrice[i+k][j-k]:3d}")

                    sum += matrice[i+k][j-k]
                    if (sum == 1 * nb):
                        return 1  # 1 a gagné
                    if (sum == -1 * nb):
                        return -1  # -1 a gagné

        return 0  # pas de gain

    ligne = ligne()
    colonne = colonne()
    diagonal = diagonal()
    antidiagonal = antidiagonal()
    return colonne

def f(matrice):
    taille_x = len(matrice)
    taille_y = len(matrice[0])
    nb = 4 # nb jeton à aligner

    def Gain():
        for i in range(0, taille_x):  # i = lignes
            for j in range(0, taille_y - nb + 1):  # j = colonnes
                # ligne = ligne_gain(matrice, i, j)
                colonne = colonne_gain(matrice, i, j)
                diagonal = diagonal_gain(matrice, i, j)
                # if ligne:
                #     return ligne
                # if colonne:
                #     return colonne
                if diagonal:
                    return diagonal
        return 0

    def ligne_gain(matrice, i, j):
        sum = 0
        for k in range(0, nb):
            if (k < nb - 1):
                print(f"{matrice[i][j + k]:3d}", end="")
            else:
                print(f"{matrice[i][j + k]:3d}")

            sum += matrice[i][j + k]

        if sum == nb:
            return 1  # joueur 1 gagne
        if sum == -nb:
            return -1  # joueur -1 gagne

    def colonne_gain(matrice, i, j):
        sum = 0
        for k in range(0, nb):
            if (k < nb - 1):
                print(f"{matrice[i + k][j]:3d}", end="")
            else:
                print(f"{matrice[i + k][j]:3d}")

            sum += matrice[i + k][j]

        if sum == nb:
            return 1
        if sum == -nb:
            return -1

    def diagonal_gain(matrice, i, j):
        sum = 0
        for k in range(0, nb):
            if (k < nb - 1):
                print(f"{matrice[i + k][j + k]:3d}", end="")
            else:
                print(f"{matrice[i + k][j + k]:3d}")

            sum += matrice[i + k][j + k]
            if (sum == 1 * nb):
                return 1  # 1 a gagné
            if (sum == -1 * nb):
                return -1  # -1 a gagné

    def colonne():
        for i in range(0, taille_x - nb + 1):  # i = lignes
            for j in range(0, taille_y):  # j = colonnes
                sum = 0
                for k in range(0, nb):
                    if (k < nb - 1):
                        print(f"{matrice[i + k][j]:3d}", end="")
                    else:
                        print(f"{matrice[i + k][j]:3d}")

                    sum += matrice[i + k][j]

                if sum == nb:
                    return 1
                if sum == -nb:
                    return -1

        return 0

    def diagonal():
        for i in range(0, taille_x - nb+1):
            for j in range(0, taille_y - nb+1):
                # print(f"{matrice[i][j]}, {matrice[i+1][j+1]}, {matrice[i+2][j+2]}, {matrice[i+3][j+3]}")
                # for k in range(0, nb):
                #     print(f"{matrice[i+k][j+k]:3d}", end="")
                # print("")

                sum = 0
                for k in range(0, nb):
                    if (k < nb - 1):
                        print(f"{matrice[i+k][j+k]:3d}", end="")
                    else:
                        print(f"{matrice[i+k][j+k]:3d}")

                    sum += matrice[i+k][j+k]
                    if (sum == 1 * nb):
                        return 1  # 1 a gagné
                    if (sum == -1 * nb):
                        return -1  # -1 a gagné

        return 0  # pas de gain

    def antidiagonal():
        for i in range(0, taille_x-nb+1):
            for j in range(nb-1, taille_y):
                # print(f"{matrice[i][j]}, {matrice[i+1][j-1]}, {matrice[i+2][j-2]}, {matrice[i+3][j-3]}")
                # for k in range(0, nb):
                #     print(f"{matrice[i+k][j-k]:3d}", end="")
                # print("")

                sum = 0
                for k in range(0, nb):
                    if (k < nb - 1):
                        print(f"{matrice[i+k][j-k]:3d}", end="")
                    else:
                        print(f"{matrice[i+k][j-k]:3d}")

                    sum += matrice[i+k][j-k]
                    if (sum == 1 * nb):
                        return 1  # 1 a gagné
                    if (sum == -1 * nb):
                        return -1  # -1 a gagné

        return 0  # pas de gain

    ligne = Gain()
    colonne = colonne()
    diagonal = diagonal()
    antidiagonal = antidiagonal()
    return ligne
def f2(matrice):
    taille_x = len(matrice)
    taille_y = len(matrice[0])
    nb = 4  # nb jetons à aligner

    # -----------------------------
    # Vérification ligne par ligne
    # -----------------------------
    def ligne():
        for i in range(0, taille_x):
            for j in range(0, taille_y - nb + 1):
                s = 0
                for k in range(0, nb):
                    print(f"{matrice[i][j+k]:3d}", end="" if k < nb-1 else "\n")
                    s += matrice[i][j+k]
                if s == nb:
                    return 1
                if s == -nb:
                    return -1
        return 0

    # -----------------------------
    # Vérification colonne par colonne
    # -----------------------------
    def colonne():
        for i in range(0, taille_x - nb + 1):
            for j in range(0, taille_y):
                s = 0
                for k in range(0, nb):
                    print(f"{matrice[i+k][j]:3d}", end="" if k < nb-1 else "\n")
                    s += matrice[i+k][j]
                if s == nb:
                    return 1
                if s == -nb:
                    return -1
        return 0

    # -----------------------------
    # Vérification diagonale (↘)
    # -----------------------------
    def diagonal():
        for i in range(0, taille_x - nb + 1):
            for j in range(0, taille_y - nb + 1):
                s = 0
                for k in range(0, nb):
                    print(f"{matrice[i+k][j+k]:3d}", end="" if k < nb-1 else "\n")
                    s += matrice[i+k][j+k]
                if s == nb:
                    return 1
                if s == -nb:
                    return -1
        return 0

    # -----------------------------
    # Vérification anti-diagonale (↙)
    # -----------------------------
    def antidiagonal():
        for i in range(0, taille_x - nb + 1):
            for j in range(nb-1, taille_y):
                s = 0
                for k in range(0, nb):
                    print(f"{matrice[i+k][j-k]:3d}", end="" if k < nb-1 else "\n")
                    s += matrice[i+k][j-k]
                if s == nb:
                    return 1
                if s == -nb:
                    return -1
        return 0

    # -----------------------------
    # Ordre des vérifications
    # -----------------------------
    r = ligne()
    if r != 0: return r

    r = colonne()
    if r != 0: return r

    r = diagonal()
    if r != 0: return r

    r = antidiagonal()
    if r != 0: return r

    return 0
def f3(matrice):
    taille_x = len(matrice)
    taille_y = len(matrice[0])
    nb = 4  # jetons à aligner

    # ----------------------------------------------------
    # Vérification ligne horizontale (→) depuis (i, j)
    # ----------------------------------------------------
    def ligne_gain(i, j):
        s = 0
        for k in range(nb):
            print(f"{matrice[i][j+k]:3d}", end="" if k < nb-1 else "\n")
            s += matrice[i][j+k]
        if s == nb: return 1
        if s == -nb: return -1
        return 0

    # ----------------------------------------------------
    # Vérification colonne verticale (↓) depuis (i, j)
    # ----------------------------------------------------
    def colonne_gain(i, j):
        s = 0
        for k in range(nb):
            print(f"{matrice[i+k][j]:3d}", end="" if k < nb-1 else "\n")
            s += matrice[i+k][j]
        if s == nb: return 1
        if s == -nb: return -1
        return 0

    # ----------------------------------------------------
    # Vérification diagonale (↘) depuis (i, j)
    # ----------------------------------------------------
    def diagonal_gain(i, j):
        s = 0
        for k in range(nb):
            print(f"{matrice[i+k][j+k]:3d}", end="" if k < nb-1 else "\n")
            s += matrice[i+k][j+k]
        if s == nb: return 1
        if s == -nb: return -1
        return 0

    # ----------------------------------------------------
    # Vérification anti-diagonale (↙) depuis (i, j)
    # ----------------------------------------------------
    def antidiagonal_gain(i, j):
        s = 0
        for k in range(nb):
            print(f"{matrice[i+k][j-k]:3d}", end="" if k < nb-1 else "\n")
            s += matrice[i+k][j-k]
        if s == nb: return 1
        if s == -nb: return -1
        return 0

    # ----------------------------------------------------
    # BOUCLE UNIQUE FACTORISÉE
    # ----------------------------------------------------
    def Gain():
        for i in range(taille_x):
            for j in range(taille_y):

                # ---- LIGNE (→) ----------------------------------
                if j <= taille_y - nb:
                    r = ligne_gain(i, j)
                    if r != 0:
                        return r

                # ---- COLONNE (↓) --------------------------------
                if i <= taille_x - nb:
                    r = colonne_gain(i, j)
                    if r != 0:
                        return r

                # ---- DIAGONALE ↘ --------------------------------
                if i <= taille_x - nb and j <= taille_y - nb:
                    r = diagonal_gain(i, j)
                    if r != 0:
                        return r

                # ---- ANTI-DIAGONALE ↙ ---------------------------
                if i <= taille_x - nb and j >= nb - 1:
                    r = antidiagonal_gain(i, j)
                    if r != 0:
                        return r

        return 0

    # Exécution
    return Gain()



def f_nonFactorise_style_prof(matrice):
    taille_x = len(matrice)
    taille_y = len(matrice[0])
    nb = 4  # nb jetons à aligner

    # -----------------------------
    # Vérification lignes
    # -----------------------------
    def ligne():
        result = 0
        for i in range(taille_x):
            for j in range(taille_y - nb + 1):
                somme = 0
                for k in range(nb):
                    print(f"{matrice[i][j+k]:3d}", end="" if k < nb-1 else "\n")
                    somme += matrice[i][j+k]
                if somme == nb:
                    if result == 0:
                        result = 1
                elif somme == -nb:
                    if result == 0:
                        result = -1
        return result

    # -----------------------------
    # Vérification colonnes
    # -----------------------------
    def colonne():
        result = 0
        for i in range(taille_x - nb + 1):
            for j in range(taille_y):
                somme = 0
                for k in range(nb):
                    print(f"{matrice[i+k][j]:3d}", end="" if k < nb-1 else "\n")
                    somme += matrice[i+k][j]
                if somme == nb:
                    if result == 0:
                        result = 1
                elif somme == -nb:
                    if result == 0:
                        result = -1
        return result

    # -----------------------------
    # Vérification diagonale ↘
    # -----------------------------
    def diagonal():
        result = 0
        for i in range(taille_x - nb + 1):
            for j in range(taille_y - nb + 1):
                somme = 0
                for k in range(nb):
                    print(f"{matrice[i+k][j+k]:3d}", end="" if k < nb-1 else "\n")
                    somme += matrice[i+k][j+k]
                if somme == nb:
                    if result == 0:
                        result = 1
                elif somme == -nb:
                    if result == 0:
                        result = -1
        return result

    # -----------------------------
    # Vérification anti-diagonale ↙
    # -----------------------------
    def antidiagonal():
        result = 0
        for i in range(taille_x - nb + 1):
            for j in range(nb-1, taille_y):
                somme = 0
                for k in range(nb):
                    print(f"{matrice[i+k][j-k]:3d}", end="" if k < nb-1 else "\n")
                    somme += matrice[i+k][j-k]
                if somme == nb:
                    if result == 0:
                        result = 1
                elif somme == -nb:
                    if result == 0:
                        result = -1
        return result

    # -----------------------------
    # Exécution de toutes les vérifications
    # -----------------------------
    result = ligne()
    if result == 0:
        result = colonne()
    if result == 0:
        result = diagonal()
    if result == 0:
        result = antidiagonal()

    return result


#matrice = createMatrice()
matrice = [
        [1, 1, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
]

print(f"taille = {len(matrice)}")
afficherMatrice(matrice)
result = f_nonFactorise_style_prof(matrice)
print(result)


