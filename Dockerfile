FROM python:3.11-alpine

RUN apk add --no-cache bash curl dcron

WORKDIR /usr/src/app

COPY app/constants.py /usr/src/app/constants.py
COPY app/main.py /usr/src/app/main.py
COPY app/notification_service.py /usr/src/app/notification_service.py
COPY app/requirements.txt /usr/src/app/requirements.txt
COPY app/train_schedule.py /usr/src/app/train_schedule.py
COPY app/utils.py /usr/src/app/utils.py

RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN touch /var/log/cron.log

CMD ["/entrypoint.sh"]