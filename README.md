nano /home/esd-kiosk1/kiosk/start_kiosk.sh


#!/bin/bash
sleep 10

# Chromium Session löschen
rm -f "/home/esd-kiosk1/.config/chromium/Default/Last Session"
rm -f "/home/esd-kiosk1/.config/chromium/Default/Last Tabs"

# Kiosk starten
chromium --start-fullscreen --noerrdialogs --disable-infobars \
  --ozone-platform=wayland --password-store=basic \
  http://localhost:8080


  chmod +x /home/esd-kiosk1/kiosk/start_kiosk.sh


nano /home/esd-kiosk1/.config/labwc/autostart


/home/esd-kiosk1/kiosk/start_kiosk.sh &
