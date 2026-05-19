nano /home/esd-kiosk1/kiosk/start_kiosk.sh


#!/bin/bash

# Warten bis Wayland-Socket bereit ist
until [ -S "/run/user/$(id -u)/wayland-0" ]; do
    sleep 1
done
sleep 2

# Warten bis Flask antwortet
until curl -sf http://127.0.0.1:8080 > /dev/null 2>&1; do
    sleep 1
done
sleep 2

# Sessions löschen
rm -rf "/home/esd-kiosk1/.config/chromium/Default/Sessions/"* 2>/dev/null

# Panel beenden
pkill wf-panel-pi 2>/dev/null
sleep 1

# Kiosk starten
WAYLAND_DISPLAY=wayland-0 chromium --kiosk --noerrdialogs --disable-infobars \
  --ozone-platform=wayland --password-store=basic \
  http://127.0.0.1:8080


nano /home/esd-kiosk1/.config/labwc/autostart

/home/esd-kiosk1/kiosk/start_kiosk.sh &
