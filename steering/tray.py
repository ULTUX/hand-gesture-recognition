import threading
import pystray
from PIL import Image, ImageDraw


def create_circle(width, height, background_color, circle_color):
    image = Image.new('RGBA', (width, height), background_color)

    dc = ImageDraw.Draw(image)

    dc.ellipse(
        [(6, 6), (width - 6, height - 6)],
        fill=circle_color,
        outline=(0, 0, 0, 0))

    return image


green_circle = create_circle(32, 32, (255, 255, 255, 0), (0, 255, 0, 255))
red_circle = create_circle(32, 32, (0, 0, 0, 0), (255, 0, 0, 255))

icon = pystray.Icon('Gestownik',
                    icon=green_circle,
                    menu=pystray.Menu(
                        pystray.MenuItem("Zamknij", lambda: icon.stop())
                    ))

tray_icon_thread = threading.Thread(target=lambda: icon.run(), name="trayIconThread")
