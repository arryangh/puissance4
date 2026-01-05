
import time

longueur = 50
for i in range(longueur + 1):
    pourcentage = int((i / longueur) * 100)
    load_bar = "#" * i + "-" * (longueur - i)
    print(f"\r[{load_bar}] {pourcentage}%", end='', flush=True)
    time.sleep(0.1)

print()  # Retour à la ligne final