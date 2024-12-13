#!/bin/sh -e
cd /home/yub168/myTvbox
git fetch github
git reset --hard github/master
chmod -R 755 /home/yub168/myTvbox
venv/bin/python AutoScrapy.py
git add .
git commit -m 'update'
git push github master