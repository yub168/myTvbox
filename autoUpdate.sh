#!/bin/sh -e
git pull origin master
python3 AutoScrapy.py
git add .
git commit -m 'update'
git push origin master
git push github master