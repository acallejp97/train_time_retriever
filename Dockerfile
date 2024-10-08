FROM python:3.11-alpine

# Instalar dependencias necesarias, incluyendo bash
RUN apk add --no-cache bash curl dcron

# Crear directorio de trabajo para la app
WORKDIR /usr/src/app

# Copiar y instalar los requisitos de Python
COPY app/ /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script main.py

# Copiar el entrypoint.sh
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Crear un archivo de log para cron
RUN touch /var/log/cron.log

# Usar el entrypoint para manejar cron
CMD ["/entrypoint.sh"]