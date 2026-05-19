nano /home/esd-kiosk1/kiosk/start_kiosk.sh

WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR="/run/user/$(id -u)" \
chromium --noerrdialogs --disable-infobars \
  --ozone-platform=wayland --password-store=basic \
  --restore-last-session \
  http://127.0.0.1:8080

  nano /home/esd-kiosk1/.config/labwc/rc.xml

  <?xml version="1.0"?>
<openbox_config>
  <applications>
    <application class="chromium-browser">
      <fullscreen>yes</fullscreen>
    </application>
    <application class="Chromium-browser">
      <fullscreen>yes</fullscreen>
    </application>
  </applications>
</openbox_config>
