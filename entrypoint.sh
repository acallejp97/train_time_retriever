#!/bin/sh
crontab -l|sed "\$a$CRON_ONE_WAY python3 /usr/src/app/main.py $ORIGIN $DESTINATION"|crontab -
crontab -l|sed "\$a$CRON_RETURN_1 python3 /usr/src/app/main.py $DESTINATION $ORIGIN"|crontab -
crontab -l|sed "\$a$CRON_RETURN_2 python3 /usr/src/app/main.py $DESTINATION $ORIGIN"|crontab 