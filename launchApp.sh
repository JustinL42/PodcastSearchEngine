#!/bin/bash

export FLASK_APP=app.py
killall flask
flask run &
printf "\n\nThe Podcast Search Engine has been launched, "
printf "\nand your browser should open to it now."
printf "\nIf not, manually open http://127.0.0.1:5000/"
sleep 1
xdg-open http://127.0.0.1:5000/

