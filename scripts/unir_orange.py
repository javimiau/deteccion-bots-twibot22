import csv

archivos = ['orange_train.csv', 'orange_val.csv', 'orange_test.csv']
total = 0

with open('orange_todo.csv', 'w', newline='', encoding='utf-8') as salida:
    w = csv.writer(salida)
    for i, nombre in enumerate(archivos):
        with open(nombre, newline='', encoding='utf-8-sig') as f:
            lector = csv.reader(f)
            encabezado = next(lector)
            if i == 0:
                w.writerow(encabezado)  # el encabezado se escribe una sola vez
            for fila in lector:
                w.writerow(fila)
                total += 1
        print(f"{nombre} agregado")

print(f"\nGuardado orange_todo.csv con {total} filas")