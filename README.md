nano /home/esd-kiosk1/kiosk/start_kiosk.sh

#!/bin/bash

# Warten bis Desktop bereit
until pgrep -u "$(id -u)" pcmanfm-pi > /dev/null 2>&1; do sleep 1; done
sleep 3

# Warten bis Flask antwortet
until curl -sf http://127.0.0.1:8080 > /dev/null 2>&1; do sleep 1; done

# Sessions löschen + Preferences reparieren
rm -rf "/home/esd-kiosk1/.config/chromium/Default/Sessions/"* 2>/dev/null
python3 -c "
import json, os
p = '/home/esd-kiosk1/.config/chromium/Default/Preferences'
if os.path.exists(p):
    with open(p) as f: d = json.load(f)
    d.setdefault('profile', {})['exit_type'] = 'Normal'
    d['profile']['exited_cleanly'] = True
    with open(p, 'w') as f: json.dump(d, f)
" 2>/dev/null

# Panel beenden
pkill wf-panel-pi 2>/dev/null
sleep 1

# Chromium starten - ohne Google-Dienste (verhindert SSL-Timeout bei falschem Datum)
WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR="/run/user/$(id -u)" \
chromium --start-fullscreen \
  --noerrdialogs --disable-infobars \
  --ozone-platform=wayland --password-store=basic \
  --disable-background-networking \
  --disable-sync \
  --no-first-run \
  --disable-features=Translate,SafeBrowsing \
  http://127.0.0.1:8080 &

# F5 senden sobald GPU bereit (mehrfach als Backup)
sleep 12
WAYLAND_DISPLAY=wayland-0 wtype -k F5
sleep 8
WAYLAND_DISPLAY=wayland-0 wtype -k F5
