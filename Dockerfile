# Usa una imagen base oficial de Python ligera
FROM python:3.9-slim 

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app 

# Copia el archivo de requisitos e instala las dependencias
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt 

# Copia el resto del código de la aplicación
COPY . . 

# El puerto en el que Uvicorn se ejecutará dentro del contenedor
EXPOSE 8000 

# Comando para ejecutar la aplicación (cambia 'main:app' si tu módulo principal y objeto de FastAPI son diferentes)
# Cambia tu última línea por esta (usa la variable de entorno $PORT)
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"]