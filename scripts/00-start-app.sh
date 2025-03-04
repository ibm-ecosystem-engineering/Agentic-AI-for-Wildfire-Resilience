#!/usr/bin/env bash

echo "app Started ...."

cd /Users/gandhi/GandhiMain/700-Apps/BlazeBreakers

python -m venv myvenv
source myvenv/bin/activate

cd /Users/gandhi/GandhiMain/700-Apps/BlazeBreakers/src

python -m pip install -r requirements.txt


python main.py


echo "app completed ...."