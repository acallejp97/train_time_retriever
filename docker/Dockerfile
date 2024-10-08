FROM python:3.11-alpine

RUN apt-get update && apt-get install -y cron

WORKDIR /usr/src/app

COPY app/ /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt


COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN touch /var/log/cron.log

CMD ["/entrypoint.sh"]