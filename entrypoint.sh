#!/bin/sh

echo "Configuring cron jobs..."

echo "$CRON_ONE_WAY root python3 /usr/src/app/main.py $ORIGIN $DESTINATION >> /var/log/cron.log 2>&1" > /etc/cron.d/cron_execution_1
echo "$CRON_RETURN_1 root python3 /usr/src/app/main.py $DESTINATION $ORIGIN >> /var/log/cron.log 2>&1" > /etc/cron.d/cron_execution_2
echo "$CRON_RETURN_2 root python3 /usr/src/app/main.py $DESTINATION $ORIGIN >> /var/log/cron.log 2>&1" > /etc/cron.d/cron_execution_3

chmod 0644 /etc/cron.d/cron_execution_1
chmod 0644 /etc/cron.d/cron_execution_2
chmod 0644 /etc/cron.d/cron_execution_3

cat /etc/cron.d/cron_execution_1
cat /etc/cron.d/cron_execution_2
cat /etc/cron.d/cron_execution_3

echo "Starting cron..."
crond -l 2 && tail -f /var/log/cron.log
