#!/bin/sh

# Crear el cronjob con la variable de entorno CRON
echo "$CRON_ONE_WAY python3 /opt/app/main.py $ORIGIN $DESTINATION>> /var/log/cron.log 2>&1" > /etc/cron.d/mycron
echo "$CRON_RETURN_1 python3 /opt/app/main.py $DESTINATION $ORIGIN>> /var/log/cron.log 2>&1" > /etc/cron.d/mycron
echo "$CRON_RETURN_2 python3 /opt/app/main.py $DESTINATION $ORIGIN>> /var/log/cron.log 2>&1" > /etc/cron.d/mycron

# Otorgar permisos correctos
chmod 0644 /etc/cron.d/mycron

# Iniciar cron y mantenerlo corriendo
cron && tail -f /var/log/cron.log
