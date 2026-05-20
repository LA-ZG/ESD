#!/usr/bin/env python3
"""
ESD Kiosk - Lokaler Flask-Proxy-Server fuer Raspberry Pi
=========================================================
Startet einen Webserver auf Port 8080.
- GET  /          -> liefert esd_kiosk.html
- POST /submit    -> leitet Formulardaten an Microsoft Forms weiter

Kein CORS-Problem, da Browser nur localhost anspricht.

Installation (einmalig auf dem Pi):
  pip3 install flask requests

Starten:
  python3 server.py

Autostart beim Boot: siehe Anleitung unten (systemd).
"""

import json
import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime, timezone

app = Flask(__name__)

# ------------------------------------------------------------------ #
# Microsoft Forms - Einstellungen                                     #
# ------------------------------------------------------------------ #
TENANT_ID = "8b206608-a593-4ace-a4b6-ef1fc83c9169"
USER_ID   = "e568d74b-d6f0-4c39-a968-ea70cd733a9e"
FORM_ID   = ("CGYgi5Olzkqktu8fyDyRaUvXaOXw1jlMqWjqcM1zOp5UMER"
             "SSFpXTlUxMThISkVISVdBRU05R1RHVy4u")

FORMS_URL = (
    f"https://forms.office.com/formapi/api/{TENANT_ID}"
    f"/users/{USER_ID}/forms('{FORM_ID}')/responses"
)

Q_BARCODE = "r3ea481149afd4e01bab5d0bcaa487074"
Q_PERSON  = "r4c04e7585ba145418732a7dc2367f666"

# Verzeichnis dieser Datei (dort liegt auch esd_kiosk.html)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------ #
# HTML ausliefern                                                     #
# ------------------------------------------------------------------ #
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "esd_kiosk.html")

# Statische Dateien (falls CSS/JS ausgelagert werden)
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)

# ------------------------------------------------------------------ #
# Proxy-Endpunkt: empfaengt Daten vom Browser, sendet an Forms       #
# ------------------------------------------------------------------ #
@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json(force=True)
        barcode        = (data.get("barcode")        or "").strip()
        personalnummer = (data.get("personalnummer") or "").strip()

        if not barcode and not personalnummer:
            return jsonify({"ok": False, "error": "Keine Daten empfangen"}), 400

        now = datetime.now(timezone.utc).isoformat()

        answers = json.dumps([
            {
                "questionId": Q_BARCODE,
                "answer1": barcode,
                "answer2": None, "answer3": None, "answer4": None,
                "answer5": None, "answer6": None, "answer7": None,
                "answer8": None, "answer9": None, "answer10": None
            },
            {
                "questionId": Q_PERSON,
                "answer1": personalnummer,
                "answer2": None, "answer3": None, "answer4": None,
                "answer5": None, "answer6": None, "answer7": None,
                "answer8": None, "answer9": None, "answer10": None
            }
        ])

        payload = {
            "startDate": now,
            "submitDate": now,
            "answers": answers
        }

        headers = {
            "Content-Type": "application/json",
            "Accept":       "application/json",
            # Referer damit Forms den Request akzeptiert
            "Referer":      "https://forms.office.com/",
            "Origin":       "https://forms.office.com",
            "User-Agent":   "Mozilla/5.0 (ESD-Kiosk/1.0)"
        }

        resp = requests.post(
            FORMS_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        if resp.status_code in (200, 201, 202):
            print(f"[OK]  Barcode={barcode!r}  Person={personalnummer!r}  "
                  f"Status={resp.status_code}")
            return jsonify({"ok": True}), 200
        else:
            print(f"[ERR] Forms antwortete {resp.status_code}: {resp.text[:200]}")
            # Trotzdem als Erfolg zurueckgeben, damit der Kiosk weiterlaueft.
            # Daten werden lokal geloggt (siehe unten).
            _log_local(barcode, personalnummer, now,
                       f"Forms-Fehler {resp.status_code}")
            return jsonify({"ok": True, "warn": f"Forms {resp.status_code}"}), 200

    except requests.exceptions.ConnectionError:
        # Kein Netz -> lokal speichern, trotzdem OK zurueck
        now = datetime.now(timezone.utc).isoformat()
        _log_local(data.get("barcode",""), data.get("personalnummer",""),
                   now, "Kein Netzwerk")
        return jsonify({"ok": True, "warn": "Offline - lokal gespeichert"}), 200

    except Exception as exc:
        print(f"[EXCEPTION] {exc}")
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/shutdown-kiosk", methods=["POST"])
def shutdown_kiosk():
    """Chromium beenden (wird per 5x ESC aus dem Kiosk aufgerufen)."""
    import subprocess
    subprocess.Popen(["pkill", "chromium"])
    return jsonify({"ok": True}), 200


def _log_local(barcode, person, ts, reason):
    """Fallback: Daten in lokale CSV schreiben wenn Forms nicht erreichbar."""
    log_path = os.path.join(BASE_DIR, "esd_offline_log.csv")
    write_header = not os.path.exists(log_path)
    with open(log_path, "a", encoding="utf-8") as f:
        if write_header:
            f.write("Zeitstempel;Barcode;Personalnummer;Grund\n")
        f.write(f"{ts};{barcode};{person};{reason}\n")
    print(f"[LOG] Lokal gespeichert: {barcode} / {person} ({reason})")


# ------------------------------------------------------------------ #
# Start                                                               #
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"ESD Kiosk Server laeuft auf http://localhost:{port}")
    print(f"HTML-Pfad: {os.path.join(BASE_DIR, 'esd_kiosk.html')}")
    # host='0.0.0.0' damit auch andere Geraete im LAN zugreifen koennen
    app.run(host="0.0.0.0", port=port, debug=False)
