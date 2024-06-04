import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt

def optimalisatie(medicatie, regels, max):
    # Maak een graaf
    graaf = defaultdict(list)
    for medicatie1, medicatie2 in regels:
        graaf[medicatie1].append(medicatie2)
        graaf[medicatie2].append(medicatie1)

    # Sorteer de knooppunten in aflopende volgorde op graad
    medicatie.sort(key=lambda x: len(graaf[x]), reverse=True)

    # Maak groepen
    groepen = []
    for medicament in medicatie:
        added = False
        for groep in groepen:
            if len(groep) >= max:
                continue
            add = True
            for med in graaf[medicament]:
                if med in groep:
                    add = False
            if add:
                groep.append(medicament)
                added = True
                break
        if not added:
            groepen.append([medicament])

    return groepen