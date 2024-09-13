#!/bin/bash
#!/usr/bin/env python3

#export DISPLAY=:1 #needed if you are running a simple gui app.

cd "$(dirname "$0")"

process=api_voip
while true
do
    if ! ps aux | grep -v grep | grep 'python3 main.py' > /dev/null
    then #track1.py
        python3 main.py &
        sleep 3
    fi #track1.py
done
exit
