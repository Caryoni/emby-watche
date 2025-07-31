FROM python:3.12-slim

RUN pip install watchdog requests

WORKDIR /app
COPY watcher.py /app/
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
