#!/bin/bash
git fetch -q
git pull -q
pip install -r requirements.txt
pkill -9 -f kultivator.py
sleep 3
python "$(pwd)/kultivator.py" &