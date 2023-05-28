#!/bin/bash
git fetch -q
git pull -q
pkill -9 -f kultivator.py
sleep 3
python "$(pwd)/kultivator.py" &