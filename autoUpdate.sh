#!/bin/sh -e
cd /home/yub168/myTvbox
git fetch origin
git reset --hard origin/master
chmod -R 755 /home/yub168/myTvbox
venv/bin/python AutoScrapy.py
git add .
git commit -m 'update'
git push origin master