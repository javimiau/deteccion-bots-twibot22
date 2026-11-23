import csv
import glob
import random
from collections import Counter
import ijson

MAX_POR_CUENTA = 20        # máximo de tweets que se guardan por cuenta
EXCLUIR_RT = True          # sacar retweets (el texto no lo escribió la cuenta)
MIN_PALABRAS = 3           # sacar tweets muy cortos
MUESTRA_POR_CLASE = 2500   # tamaño de la muestra balanceada para Orange
random.seed(42)

def norm_id(x):
    s = str(x).strip()
    return s[1:] if s.lower().startswith('u') else s

def norm_label(x):
    return 'bot' if str(x).strip().lower() in ('bot', '1') else 'humano'

def leer_dos_columnas(nombre, funcion):
    d = {}
    with open(nombre, newline='', encoding='utf-8') as f:
        lector = csv.reader(f)
        next(lector)  # saltar encabezado
        for fila in lector:
            d[norm_id(fila[0])] = funcion(fila[1])
    return d

labels = leer_dos_columnas('label.csv', norm_label)
splits = leer_dos_columnas('split.csv', lambda v: v.strip().lower())
print(f"Cuentas con etiqueta cargadas: {len(labels):,}")

por_cuenta = {}
archivos = sorted(glob.glob('tweets_es_*.json'))
print(f"Archivos a procesar: {archivos}\n")

for archivo in archivos:
    print(f"Procesando {archivo}...")
    # Se abre en modo binario 'rb' para ijson
    with open(archivo, 'rb') as f:
        total_leidos = 0
        usados = 0
        
        for t in ijson.items(f, 'item'):
            total_leidos += 1
            texto = (t.get('text') or '').strip()
            
            if EXCLUIR_RT and texto.startswith('RT @'):
                continue
            if len(texto.split()) < MIN_PALABRAS:
                continue
            
            aid = norm_id(t.get('author_id'))
            if aid not in labels:
                continue
            
            lista = por_cuenta.setdefault(aid, [])
            if len(lista) < MAX_POR_CUENTA:
                lista.append(texto.replace('\n', ' ').replace('\r', ' '))
                usados += 1
                
    print(f"  -> {total_leidos:,} tweets leídos, {usados:,} guardados")

filas = []
for aid, lista in por_cuenta.items():
    for texto in lista:
        filas.append((aid, labels[aid], splits.get(aid, 'sin_split'), texto))

print("\n=== RESUMEN DE EXTRACCIÓN ===")
cuentas = Counter(labels[a] for a in por_cuenta)
tweets_c = Counter(f[1] for f in filas)
print(f"Cuentas únicas en español -> bots: {cuentas['bot']:,}, humanos: {cuentas['humano']:,}")
print(f"Tweets guardados          -> bots: {tweets_c['bot']:,}, humanos: {tweets_c['humano']:,}")
print("Por partición (tweets):", dict(Counter((f[1], f[2]) for f in filas)))

# Guardar dataset consolidado
with open('dataset_es_completo.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['author_id', 'label', 'split', 'text'])
    w.writerows(filas)

# Generar muestra balanceada para prototipo en Orange / KNIME
bots = [f for f in filas if f[1] == 'bot']
humanos = [f for f in filas if f[1] == 'humano']
n = min(MUESTRA_POR_CLASE, len(bots), len(humanos))
muestra = random.sample(bots, n) + random.sample(humanos, n)
random.shuffle(muestra)

with open('muestra_orange.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['author_id', 'label', 'split', 'text'])
    w.writerows(muestra)

print(f"\nArchivos generados exitosamente:\n- dataset_es_completo.csv ({len(filas):,} filas)\n- muestra_orange.csv ({len(muestra):,} filas, {n:,} por clase)")