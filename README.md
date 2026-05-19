nano /home/esd-kiosk1/kiosk/start_kiosk.sh


#!/bin/bash

# Warten bis Flask-Server antwortet
until curl -sf http://127.0.0.1:8080 > /dev/null 2>&1; do
    sleep 1
done

sleep 2
pkill wf-panel-pi 2>/dev/null
sleep 1

# Chromium über XWayland starten
DISPLAY=:0 chromium --noerrdialogs --disable-infobars \
  --password-store=basic \
  http://127.0.0.1:8080 &

# Warten bis Fenster sichtbar, dann F11
sleep 6
DISPLAY=:0 xdotool search --sync --onlyvisible --name "Chromium" key F11
