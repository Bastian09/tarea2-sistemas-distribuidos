from pymongo import MongoClient
from cache import CacheLRU, CacheLFU
import numpy as np
import random
import time

def conectar_mongo():
    cliente = MongoClient("mongodb://localhost:27017/")
    db = cliente["trafico_rm"]
    coleccion = db["eventos"]
    return coleccion

def generar_llegadas(distribucion="poisson", tasa=5, total_eventos=50):
    tiempos = []
    if distribucion == "poisson":
        tiempos = np.random.poisson(lam=tasa, size=total_eventos)
    elif distribucion == "uniforme":
        tiempos = np.random.uniform(low=1, high=tasa*2, size=total_eventos)
    return tiempos

def main():
    coleccion = conectar_mongo()

    # Configurar cache
    politica = input("Selecciona política de cache (lru / lfu): ").strip().lower()
    if politica not in ["lru", "lfu"]:
        print("Política no válida.")
        return

    capacidad_cache = int(input("Capacidad máxima del cache (por ejemplo 100): "))

    if politica == "lru":
        cache = CacheLRU(capacidad_cache)
    else:
        cache = CacheLFU(capacidad_cache)

    # Configurar simulación de tráfico
    distribucion = input("Selecciona distribución de tráfico (poisson / uniforme): ").strip().lower()
    if distribucion not in ["poisson", "uniforme"]:
        print("Distribución no válida.")
        return

    tasa = int(input("Ingrese la tasa base (por ejemplo, 5): "))
    total_eventos = int(input("Cantidad total de consultas a generar: "))

    tiempos = generar_llegadas(distribucion=distribucion, tasa=tasa, total_eventos=total_eventos)

    # Obtener todos los IDs de eventos
    eventos = list(coleccion.find({}, {"_id": 1}))
    ids = [evento["_id"] for evento in eventos]

    if not ids:
        print("No hay eventos en la base de datos.")
        return

    print(f"\nGenerando {total_eventos} consultas siguiendo distribución {distribucion}...\n")

    for i, t in enumerate(tiempos):
        id_consultado = random.choice(ids)

        # Consultar primero en el cache
        evento = cache.get(id_consultado)

        if evento is None:
            # Si no está en el cache, buscar en MongoDB
            evento = coleccion.find_one({"_id": id_consultado})
            if evento:
                cache.put(id_consultado, evento)

        print(f"[{i+1}] Consultado evento ID: {id_consultado} -> {evento.get('descripcion', 'Sin descripción') if evento else 'Evento no encontrado'}")
        
        sleep_time = max(t, 0.1)  # Nunca dormir 0 segundos
        time.sleep(sleep_time)

    print("\n--- Estadísticas del Cache ---")
    print(f"Cache Hits: {cache.hits}")
    print(f"Cache Misses: {cache.misses}")

if __name__ == "__main__":
    main()
