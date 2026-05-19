nano /home/esd-kiosk1/.config/labwc/rc.xml

<?xml version="1.0"?>
<labwc_config>
  <applications>
    <application class="Chromium-browser">
      <fullscreen>yes</fullscreen>
    </application>
  </applications>
</labwc_config>

nano /home/esd-kiosk1/kiosk/start_kiosk.sh

#!/bin/bash

until pgrep -u "$(id -u)" pcmanfm-pi > /dev/null 2>&1; do sleep 1; done
sleep 3

until curl -sf http://127.0.0.1:8080 > /dev/null 2>&1; do sleep 1; done

rm -rf "/home/esd-kiosk1/.config/chromium/Default/Sessions/"* 2>/dev/null

WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR="/run/user/$(id -u)" \
chromium --noerrdialogs --disable-infobars \
  --ozone-platform=wayland --password-store=basic \
  http://127.0.0.1:8080
