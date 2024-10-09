#!/bin/sh

# Crear el cronjob con la variable de entorno CRON
echo "$CRON_ONE_WAY python3 /usr/src/app/main.py $ORIGIN $DESTINATION >> /var/log/cron.log 2>&1" > /etc/cron.d/cron_execution_1
echo "$CRON_RETURN_1 python3 /usr/src/app/main.py $DESTINATION $ORIGIN >> /var/log/cron.log 2>&1" > /etc/cron.d/cron_execution_2
echo "$CRON_RETURN_2 python3 /usr/src/app/main.py $DESTINATION $ORIGIN >> /var/log/cron.log 2>&1" > /etc/cron.d/cron_execution_3

# Otorgar permisos correctos
chmod 0644 /etc/cron.d/cron_execution_1
chmod 0644 /etc/cron.d/cron_execution_2
chmod 0644 /etc/cron.d/cron_execution_3

# Iniciar cron y mantenerlo corriendo
crond && tail -f /var/log/cron.log
