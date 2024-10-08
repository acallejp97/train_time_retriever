FROM python:3.11-alpine

RUN apk add --no-cache bash curl dcron

WORKDIR /usr/src/app

COPY app/constants.py /usr/src/app/
COPY app/main.py /usr/src/app/
COPY app/notification_service.py /usr/src/app/
COPY app/requirements.txt /usr/src/app/
COPY app/train_schedule.py /usr/src/app/
COPY app/utils.py /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN touch /var/log/cron.log

CMD ["/entrypoint.sh"]