sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

@chromium-browser --kiosk --noerrdialogs --disable-infobars --disable-session-crashed-bubble http://localhost:8080


nano /home/esd-kiosk1/.config/lxsession/rpd-x/autostart


mkdir -p /home/esd-kiosk1/.config/autostart
nano /home/esd-kiosk1/.config/autostart/esd-kiosk.desktop


[Desktop Entry]
Type=Application
Name=ESD Kiosk
Exec=bash -c 'sleep 6 && chromium --kiosk --noerrdialogs --disable-infobars --disable-session-crashed-bubble http://localhost:8080'
X-GNOME-Autostart-enabled=true
