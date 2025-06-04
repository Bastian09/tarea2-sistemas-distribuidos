Proyecto Sistemas Distribuidos - Tarea 1

Este proyecto implementa un sistema distribuido compuesto por:
- Un módulo de scraping de eventos de tráfico desde Waze.
- Almacenamiento en MongoDB.
- Un generador de tráfico de consultas simuladas.
- Un sistema de cache con políticas LRU y LFU.
- Docker para contenerizar y facilitar la ejecución de los servicios.

---

Requisitos

- Docker y Docker Compose instalados.
- Python 3.12 instalado localmente (para ejecutar los scripts fuera del contenedor).
- Google Chrome instalado localmente (para Selenium).

---

Levantar MongoDB con Docker

Desde la raíz del proyecto, ejecutar:

```bash
docker compose up -d
```
- Esto levantará un contenedor con MongoDB accesible desde localhost:27017.

- Para detener los contenedores:
```bash
docker compose down
```
---

Ejecutar el Scraper (fuera de Docker)
- Crear y activar un entorno virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```
---
Instalar dependencias:
```bash
pip install -r requirements.txt
```
Ejecutar el scraper:
```bash
python scraper.py
```
Ejecutar el Generador de Tráfico
Dentro del entorno virtual, correr:
```bash
python generador_trafico.py
```
El generador te pedirá los siguientes parámetros:
- Política de cache: lru o lfu.
- Tamaño máximo del cache.
- Distribución de tráfico: poisson o uniforme.
- Tasa base de llegada.
- Cantidad total de consultas.

Al finalizar, se mostrarán estadísticas de rendimiento del cache








