# Usamos una imagen oficial de Python
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el código fuente al contenedor
COPY . /app

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto (puedes cambiarlo luego si quieres iniciar otro script)
CMD ["python", "scraper.py"]
