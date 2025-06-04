from pymongo import MongoClient
import csv
import os

def conectar_mongo():
    cliente = MongoClient("mongodb://localhost:27017/")
    db = cliente["trafico_rm"]
    return db["eventos"]

def limpiar_y_exportar():
    coleccion = conectar_mongo()
    eventos = coleccion.find()

    vistos = set()
    salida = []

    for e in eventos:
        tipo = e.get("tipo", "").strip()
        direccion = e.get("direccion", "").strip()
        descripcion = e.get("descripcion", "").strip()
        timestamp = e.get("_id").generation_time.isoformat()  # usar fecha real del _id
        comuna = "Desconocida"  # opcional si no la extraes aún

        if not tipo or tipo.lower() == "usuario":
            continue  # saltar usuarios y vacíos

        clave = f"{tipo}-{direccion}"
        if clave in vistos:
            continue
        vistos.add(clave)

        salida.append([tipo, comuna, timestamp, descripcion])

    # Guardar en CSV
    os.makedirs("data", exist_ok=True)
    with open("data/eventos_limpios.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["tipo", "comuna", "timestamp", "descripcion"])
        writer.writerows(salida)

    print(f"[✓] Exportados {len(salida)} eventos a data/eventos_limpios.csv")

if __name__ == "__main__":
    limpiar_y_exportar()
