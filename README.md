nano /home/esd-kiosk1/kiosk/start_kiosk.sh

#!/bin/bash

# Warten bis Desktop-Manager läuft (= Desktop vollständig bereit)
until pgrep -u "$(id -u)" pcmanfm-pi > /dev/null 2>&1; do
    sleep 1
done
sleep 5

# Umgebungsvariablen explizit setzen
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"

# Warten bis Flask antwortet
until curl -sf http://127.0.0.1:8080 > /dev/null 2>&1; do
    sleep 1
done

# Sessions löschen
rm -rf "/home/esd-kiosk1/.config/chromium/Default/Sessions/"* 2>/dev/null

# Kiosk starten (Panel diesmal NICHT beenden)
chromium --kiosk --noerrdialogs --disable-infobars \
  --ozone-platform=wayland --password-store=basic \
  http://127.0.0.1:8080
