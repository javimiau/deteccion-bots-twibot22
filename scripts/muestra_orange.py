import csv
import random
from collections import defaultdict

random.seed(42)
# Tweets por clase (bot / humano) que se sacan de cada partición
POR_PARTICION = {'train': 1500, 'val': 500, 'test': 500}

grupos = defaultdict(list)  # (partición, etiqueta) -> filas
with open('dataset_es_completo.csv', newline='', encoding='utf-8-sig') as f:
    lector = csv.reader(f)
    encabezado = next(lector)  # author_id, label, split, text
    for fila in lector:
        grupos[(fila[2], fila[1])].append(fila)

print("Particiones encontradas:", sorted({k[0] for k in grupos}))

for particion, n in POR_PARTICION.items():
    muestra = []
    for etiqueta in ('bot', 'humano'):
        disponibles = grupos[(particion, etiqueta)]
        k = min(n, len(disponibles))
        muestra.extend(random.sample(disponibles, k))
        cuentas = len({fila[0] for fila in muestra if fila[1] == etiqueta})
        print(f"{particion:>5} | {etiqueta:<6}: {k} tweets de {cuentas} cuentas distintas "
              f"(disponibles: {len(disponibles)})")
    random.shuffle(muestra)
    nombre = f'orange_{particion}.csv'
    with open(nombre, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(encabezado)
        w.writerows(muestra)
    print(f"      -> guardado {nombre} ({len(muestra)} filas)\n")