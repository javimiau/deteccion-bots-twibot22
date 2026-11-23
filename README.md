# Detección de bots en comentarios en español: preparación de datos

Scripts en Python con los que se preparó el conjunto de datos del proyecto de título
*Detección de Bots en Comentarios en Español Aplicando Modelos de Machine Learning y Deep Learning*
(Universidad del Bío-Bío). A partir de Twibot-22 se filtran los tweets en español, se cruzan con
la etiqueta (bot o humano) y la partición de cada cuenta, y se genera una muestra balanceada
para las pruebas en Orange.

## Datos

Twibot-22 se obtuvo por solicitud a sus autores para fines de investigación. **Los datos no se
incluyen en este repositorio y no deben redistribuirse.** Para ejecutar los scripts se necesitan
los archivos originales del dataset:

- `tweet_0.json` a `tweet_8.json`
- `label.csv` (etiqueta de cada cuenta)
- `split.csv` (partición de cada cuenta: entrenamiento, validación o prueba)

## Estructura

```
datos/      archivos de entrada y de salida (no se sube a GitHub)
scripts/    scripts de preparación
```

## Requisitos

Python 3 y la biblioteca `ijson`:

```
pip install -r requirements.txt
```

## Ejecución

Los scripts leen y escriben en la carpeta desde la que se ejecutan, así que hay que correrlos
con la terminal ubicada en `datos/`.

| Paso | Comando | Genera | A partir de |
|---|---|---|---|
| 1 | `python ../scripts/procesar.py` | `tweets_es_N.json` | `tweet_N.json` |
| 2 | `python ../scripts/cruzar.py` | `dataset_es_completo.csv` | `tweets_es_*.json`, `label.csv`, `split.csv` |
| 3 | `python ../scripts/muestra_orange.py` | `orange_train.csv`, `orange_val.csv`, `orange_test.csv` | `dataset_es_completo.csv` |
| 4 | `python ../scripts/unir_orange.py` | `orange_todo.csv` | los tres `orange_*.csv` |

Notas:

- `procesar.py` procesa un archivo por ejecución. Hay que cambiar `archivo_entrada` y
  `archivo_salida` dentro del script para cada uno de los nueve archivos (0 a 8).
- `cruzar.py` también genera `muestra_orange.csv`, que no se utilizó en las pruebas; la muestra
  final sale del paso 3.
- `resumen_datos.py` (opcional) cuenta los tweets y las cuentas por clase y partición, comprueba que
  ninguna cuenta esté en más de una partición y genera `tablas_datos.tex` con las tablas para el informe.

## Parámetros

| Script | Parámetro | Valor |
|---|---|---|
| `procesar.py` | idioma | campo `lang` igual a `es` |
| `cruzar.py` | `MAX_POR_CUENTA` | 20 tweets por cuenta |
| `cruzar.py` | `EXCLUIR_RT` | se descartan los retweets |
| `cruzar.py` | `MIN_PALABRAS` | se descartan tweets de menos de 3 palabras |
| `muestra_orange.py` | `POR_PARTICION` | 1.500 (train), 500 (val) y 500 (test) tweets por clase |
| `muestra_orange.py` | semilla | 42 |

## Uso en Orange

`orange_todo.csv` tiene 5.000 comentarios con las columnas `author_id`, `label`, `split` y `text`.
En las pruebas se entrena con las filas de `split = train` (3.000) y se evalúa con las de
`split = test` (1.000). La partición de validación (1.000) no se utilizó en esta etapa.

## Limitaciones

- De cada cuenta se conservan los primeros 20 tweets según el orden de los archivos, no una
  selección aleatoria.
- El idioma se toma del campo `lang` del dataset, sin una verificación adicional.
- La muestra está balanceada por tweets, no por cuentas.
