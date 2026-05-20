nano /home/esd-kiosk1/Desktop/Kiosk-Starten.sh

#!/bin/bash
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
pkill -f "lwrespawn.*wf-panel" 2>/dev/null
sleep 0.5
pkill wf-panel-pi 2>/dev/null
sleep 0.5
WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR="/run/user/$(id -u)" \
chromium --kiosk --noerrdialogs --disable-infobars \
  --ozone-platform=wayland --password-store=basic \
  --disable-background-networking --disable-sync --no-first-run \
  --disable-features=Translate,SafeBrowsing \
  http://127.0.0.1:8080


  chmod +x /home/esd-kiosk1/Desktop/Kiosk-Starten.sh
