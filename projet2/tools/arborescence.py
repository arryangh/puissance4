import os

LIMITE_FICHIERS = 15

def generer_arborescence(dossier, prefixe=""):
    contenu = []
    try:
        elements = sorted(os.listdir(dossier))
    except PermissionError:
        return [prefixe + "└── [Permission Denied]"]

    total = len(elements)
    tronqué = False

    if total > LIMITE_FICHIERS:
        elements_affiches = elements[:LIMITE_FICHIERS]
        tronqué = True
    else:
        elements_affiches = elements

    for i, nom in enumerate(elements_affiches):
        chemin = os.path.join(dossier, nom)
        branche = "├── " if i < len(elements_affiches) - 1 or tronqué else "└── "
        ligne = prefixe + branche + nom
        contenu.append(ligne)

        if os.path.isdir(chemin):
            prolongation = "│   " if i < len(elements_affiches) - 1 or tronqué else "    "
            contenu.extend(generer_arborescence(chemin, prefixe + prolongation))

    if tronqué:
        contenu.append(prefixe + "└── ... ({} fichiers non affichés)".format(total - LIMITE_FICHIERS))

    return contenu

# Point d'entrée
racine = "../../projet2"
arborescence = generer_arborescence(racine)

# Écriture dans un fichier texte
with open("arborescence.txt", "w", encoding="utf-8") as f:
    f.write(racine + "\n")
    for ligne in arborescence:
        f.write(ligne + "\n")

print("✅ Arborescence abrégée générée dans 'arborescence.txt'")

