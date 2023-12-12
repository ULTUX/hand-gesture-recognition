import threading

import pystray

import steering.keys as keys
from steering.icon import green_circle

WZNOW_WYKRYWANIE_GESTOW = "Wznów wykrywanie gestów"
ZATRZYMAJ_WYKRYWANIE_GESTOW = "Zatrzymaj wykrywanie gestów"


def start_stop_gesture_recognition():
    global start_stop_menu_item_text
    keys.set_ignore_events(not keys.ignore_events)

    if keys.ignore_events:
        start_stop_menu_item_text = WZNOW_WYKRYWANIE_GESTOW
    else:
        start_stop_menu_item_text = ZATRZYMAJ_WYKRYWANIE_GESTOW


start_stop_menu_item_text = ZATRZYMAJ_WYKRYWANIE_GESTOW
start_stop_menu_item = pystray.MenuItem(lambda text: start_stop_menu_item_text,
                                        lambda: start_stop_gesture_recognition())
close_app_menu_item = pystray.MenuItem("Zamknij", lambda: tray_icon.stop())

tray_icon = pystray.Icon('Gestownik',
                         icon=green_circle,
                         menu=pystray.Menu(
                             start_stop_menu_item,
                             close_app_menu_item
                         ))

tray_icon_thread = threading.Thread(target=lambda: tray_icon.run(), name="trayIconThread")


def display_config_notification():
    tray_icon.notify("Uruchomiono rozpoznawanie gestów.", "Gestownik")
