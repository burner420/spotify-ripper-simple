#!/usr/bin/env bash

cd /app/spotify-ripper-simple/frontend
export FLASK_DEBUG=1
nohup python my_app.py > log.txt &
echo "Open your browser to http://localhost:8000"

cd /app/spotify-ripper-simple
while true
do
    python process_rips.py
    sleep 1
done