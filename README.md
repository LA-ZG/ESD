nano /home/esd-kiosk1/.config/labwc/autostart

sleep 6 && chromium --kiosk --noerrdialogs --disable-infobars --ozone-platform=wayland http://localhost:8080 &
