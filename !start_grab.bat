@echo off
setlocal
set PYTHONPATH=%cd%\!python

start "" python "art scraper.py"
exit
