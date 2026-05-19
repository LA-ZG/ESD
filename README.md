mkdir -p /home/esd-kiosk1/.config
nano /home/esd-kiosk1/.config/wayfire.ini

[autostart]
esd_kiosk = sleep 6 && chromium --kiosk --noerrdialogs --disable-infobars --ozone-platform=wayland http://localhost:8080

ps aux | grep -E "wayfire|labwc|weston" | grep -v grep
