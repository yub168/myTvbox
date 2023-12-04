#!/bin/sh -e
cd /home/yub168/myTvbox
python3 AutoScrapy.py
git add .
git commit -m 'update'
git push origin master