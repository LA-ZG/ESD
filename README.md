mkdir -p /home/esd-kiosk1/.config
nano /home/esd-kiosk1/.config/wayfire.ini

[autostart]
esd_kiosk = sleep 6 && chromium --kiosk --noerrdialogs --disable-infobars --ozone-platform=wayland http://localhost:8080
