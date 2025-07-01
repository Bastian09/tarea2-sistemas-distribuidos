# ingesta_elastic.py
from elasticsearch import Elasticsearch, helpers
import csv

# Conexión a ES
es = Elasticsearch("http://localhost:9200")

# Prepara acciones para bulk insert
actions = []
with open('data/eventos_limpios.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        actions.append({
            '_index': 'trafico_rm',
            '_source': {
                'tipo':        row['tipo'],
                'clase':       row.get('clase', row['tipo']),  # si tu CSV no tiene 'clase', ajusta
                'comuna':      row['comuna'],
                'timestamp':   row['timestamp'],
                'descripcion': row['descripcion']
            }
        })

# Ejecución bulk
helpers.bulk(es, actions)
print(f"Insertados {len(actions)} documentos en Elasticsearch")
