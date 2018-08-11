#!/bin/bash
#
# Run api inside a linux container.
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_api.sh
set -e
alembic upgrade head
# Prepare log files and start outputting logs to stdout
touch /opt/mannickutd/etc/services/shortened_url/logs/gunicorn.log
touch /opt/mannickutd/etc/services/shortened_url/logs/access.log
tail -n 0 -f /opt/mannickutd/etc/services/shortened_url/logs/*.log &
# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn app_server:app \
    --name shortened-url \
    --bind unix:app.sock \
    --workers 3 \
    --limit-request-line 8000 \
    --timeout 300 \
    --worker-class aiohttp.worker.GunicornWebWorker \
    --log-config=/opt/mannickutd/etc/services/shortened_url/gunicorn_log.conf \
    --log-file=/opt/mannickutd/etc/services/shortened_url/logs/gunicorn.log \
    --access-logfile=/opt/mannickutd/etc/services/shortened_url/logs/access.log & 
exec nginx -g "pid /tmp/nginx.pid; daemon off;"
