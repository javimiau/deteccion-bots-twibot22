# Resume la composición de los conjuntos de datos y genera tablas en LaTeX.
# Uso: ejecutarlo desde la carpeta del proyecto (la que contiene datos/) o desde datos/:
#   python scripts/resumen_datos.py        (desde la carpeta del proyecto)
#   python ../scripts/resumen_datos.py     (desde datos/)
import csv
import os
import sys
from collections import Counter, defaultdict

csv.field_size_limit(sys.maxsize)

ORDEN_PARTICIONES = ['train', 'val', 'test']
ORDEN_CLASES = ['bot', 'humano']


def buscar(nombre):
    """Busca el archivo en la carpeta actual, en datos/ o en ../datos/."""
    for carpeta in ('.', 'datos', '../datos'):
        ruta = os.path.join(carpeta, nombre)
        if os.path.exists(ruta):
            return ruta
    return None


def miles(n):
    """Formatea un entero con punto como separador de miles (estilo español)."""
    return f"{n:,}".replace(",", ".")


def resumir(nombre):
    tweets = Counter()               # (partición, clase) -> cantidad de tweets
    cuentas = defaultdict(set)       # (partición, clase) -> ids de cuentas
    particiones_por_cuenta = defaultdict(set)
    with open(nombre, newline='', encoding='utf-8-sig') as f:
        for fila in csv.DictReader(f):
            clave = (fila['split'], fila['label'])
            tweets[clave] += 1
            cuentas[clave].add(fila['author_id'])
            particiones_por_cuenta[fila['author_id']].add(fila['split'])
    mezcladas = sum(1 for s in particiones_por_cuenta.values() if len(s) > 1)
    return tweets, cuentas, mezcladas


def mostrar(nombre, tweets, cuentas, mezcladas):
    print(f"\n=== {nombre} ===")
    print(f"{'partición':<10}{'clase':<8}{'tweets':>10}{'cuentas':>10}")
    for p in ORDEN_PARTICIONES + sorted({k[0] for k in tweets} - set(ORDEN_PARTICIONES)):
        for c in ORDEN_CLASES:
            if (p, c) in tweets:
                print(f"{p:<10}{c:<8}{tweets[(p, c)]:>10,}{len(cuentas[(p, c)]):>10,}")
    total_tweets = sum(tweets.values())
    todas = set().union(*cuentas.values()) if cuentas else set()
    print(f"{'TOTAL':<18}{total_tweets:>10,}{len(todas):>10,}")
    print(f"Cuentas presentes en más de una partición: {mezcladas}")


def tabla_latex(titulo, etiqueta, tweets, cuentas):
    filas = []
    for p in ORDEN_PARTICIONES + sorted({k[0] for k in tweets} - set(ORDEN_PARTICIONES)):
        for c in ORDEN_CLASES:
            if (p, c) in tweets:
                filas.append(f"{p} & {c} & {miles(tweets[(p, c)])} & {miles(len(cuentas[(p, c)]))} \\\\ \\hline")
    total_tweets = sum(tweets.values())
    todas = set().union(*cuentas.values()) if cuentas else set()
    filas.append(f"\\textbf{{Total}} & & \\textbf{{{miles(total_tweets)}}} & \\textbf{{{miles(len(todas))}}} \\\\ \\hline")
    cuerpo = "\n".join(filas)
    return (
        "\\begin{table}[H]\n\\centering\n"
        f"\\caption{{{titulo}}}\n\\label{{{etiqueta}}}\n"
        "\\begin{tabular}{|l|l|r|r|}\n\\hline\n"
        "\\textbf{Partición} & \\textbf{Clase} & \\textbf{Tweets} & \\textbf{Cuentas} \\\\ \\hline\n"
        f"{cuerpo}\n\\end{{tabular}}\n\\end{{table}}\n"
    )


if __name__ == '__main__':
    salida = []
    for archivo, titulo, etiqueta in [
        ('dataset_es_completo.csv', 'Composición del conjunto de datos en español (dataset\\_es\\_completo.csv).', 'tab:dataset-completo'),
        ('orange_todo.csv', 'Composición de la muestra utilizada en Orange (orange\\_todo.csv).', 'tab:muestra'),
    ]:
        ruta = buscar(archivo)
        if ruta is None:
            print(f"No se encontró {archivo} (se buscó en la carpeta actual y en datos/); se omite.")
            continue
        t, c, m = resumir(ruta)
        mostrar(ruta, t, c, m)
        salida.append(tabla_latex(titulo, etiqueta, t, c))

    if salida:
        with open('tablas_datos.tex', 'w', encoding='utf-8') as f:
            f.write("\n".join(salida))
        print("\nSe generó tablas_datos.tex (pegar su contenido en el capítulo 7).")
    else:
        print("\nNo se generó ningún archivo: no se encontraron los CSV.")