import threading
import pystray
from PIL import Image, ImageDraw

import keys

WZNOW_WYKRYWANIE_GESTOW = "Wznów wykrywanie gestów"
ZATRZYMAJ_WYKRYWANIE_GESTOW = "Zatrzymaj wykrywanie gestów"


def create_circle(width, height, background_color, circle_color):
    image = Image.new('RGBA', (width, height), background_color)

    dc = ImageDraw.Draw(image)

    dc.ellipse(
        [(6, 6), (width - 6, height - 6)],
        fill=circle_color,
        outline=(0, 0, 0, 0))

    return image


def start_stop_gesture_recognition():
    global start_stop_menu_item_text
    keys.set_ignore_events(not keys.ignore_events)

    if keys.ignore_events:
        start_stop_menu_item_text = WZNOW_WYKRYWANIE_GESTOW
    else:
        start_stop_menu_item_text = ZATRZYMAJ_WYKRYWANIE_GESTOW


green_circle = create_circle(32, 32, (255, 255, 255, 0), (0, 255, 0, 255))
red_circle = create_circle(32, 32, (0, 0, 0, 0), (255, 0, 0, 255))

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
