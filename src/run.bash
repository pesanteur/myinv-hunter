#!/bin/bash

export DISPLAY=:0

Xvfb $DISPLAY -screen 0 1920x1080x24+32 &

# Selenium and/or chromedrive leave around zombie processes
# However, this issue goes away if bash owns the python process. 
python /src/run.py $@
