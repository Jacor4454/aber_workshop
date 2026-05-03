# micropython streetpass smart lanyard
## Overview

This project was supposed to be a 1 piece of code (main.py) that did everything 

now its 2:
lanywrd pulls an image and user data from an api over wifi
streetpass listens and broadcasts from espnow to identify others nearby and log through the API who you passed by

The idea was a smart lanyard that would track your interactions throughout an event

## how it works
### lanyard

simply it connects to the wifi network using the WIFI_PASSWORD and WIFI_SSID parameters at the top of the file

Then it sends get requests to the api for:
 - an image
 - a photo
 - a job title

finally it decodes the image and displays it on the screen

### streetpass
first it performs the same connection script as lanyyard, but then starts a apir of async functions, 1 constantly broadcasts the username (at the top of the file) and one constantly listens for a transmission.

Once a transmission is heard, it is then checked against a set of previous encounters and, if it is new, it is sent to the API and logged in the users table to track encounters centrally for later viewing, to see who you met that day

## API
To add users to the apu, simply add entries to the users table at the top of main.js. 

WARNING: The storage is not persistent, so when restarted all interactions will be lost

also add a 64x64 image linking the name to that table entry, you can make one by running helper.py locally
