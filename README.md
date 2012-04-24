coauthor
========

An experiment in etherpad, persona, and a more publishing-oriented model



Run etherpadlite (generates an APIKEY.txt, and runs on port 9001 by default)

* cd etherpad-lite
* bin/run.sh

Copy API key to shared location:
* cp etherpad-lite/APIKEY.txt coauthor_site/

Run django server
* python manage.py runserver

Run http proxy
* npm install -g http-proxy
* node-http-proxy --config config.json --port 8081
