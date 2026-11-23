# Procesa todos los .json originales del dataset, filtrando solo los que están en español
import ijson
import json
import time

archivo_entrada = 'tweet_8.json' # se cambia el nombre según el archivo de entrada
archivo_salida = 'tweets_es_8.json' # se cambia el nombre según el archivo de salida

print(f"Procesando {archivo_entrada}...")
inicio = time.time()

tweets_espanol = []
contador_total = 0
contador_es = 0

with open(archivo_entrada, 'r', encoding='utf-8') as f:
    objetos = ijson.items(f, 'item')
    for tweet in objetos:
        contador_total += 1
        
        if tweet.get('lang') == 'es': # usa lang sin ninguna librería pq ya lo trae el dataset
            contador_es += 1
            tweets_espanol.append({
                "author_id": tweet.get('author_id'),
                "text": tweet.get('text'),
                "created_at": tweet.get('created_at')
            })
        
        if contador_total % 200000 == 0:
            transcurrido = time.time() - inicio
            print(f"  Procesados {contador_total} tweets | En español: {contador_es} | "
                  f"Tiempo: {transcurrido/60:.1f} min")

print(f"\n=== RESUMEN {archivo_entrada} ===")
print(f"Total tweets procesados: {contador_total}")
print(f"Tweets en español encontrados: {contador_es}")
print(f"Tiempo total: {(time.time()-inicio)/60:.1f} minutos")

with open(archivo_salida, 'w', encoding='utf-8') as f:
    json.dump(tweets_espanol, f, ensure_ascii=False, indent=2)

print(f"\nGuardado en '{archivo_salida}'")