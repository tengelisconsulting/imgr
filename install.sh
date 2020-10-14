#!/bin/bash


python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r ./requirements.txt
python3 -m pip install shiv==0.3.1

python3 -m shiv -e imgr:main -o ./bin/imgr .
