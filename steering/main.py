import platform
import threading
import time

from flask import Flask
from waitress import create_server

import config
from keys import press_keys
from tray import tray_icon_thread, tray_icon

app = Flask("__name__")


@app.route('/gesture/<gesture>', methods=['GET','POST'])
def on_gesture(gesture=None):
    if gesture in config.gesture_dict:
        press_keys(config.gesture_dict[gesture])
    return "Done"


rest_server = create_server(app, host="0.0.0.0", port=12345)
server_thread = threading.Thread(name="restApiThread", target=lambda: rest_server.run())


def display_config_notification():
    config_string = ('Wczytana konfiguracja gestów: \n' +
                     '\n'.join([f'{a} : {config.gesture_dict[a]}' for a in config.gesture_dict]) +
                     f'\nCzas wstrzymania: {config.hold_time} ms.')
    tray_icon.notify(config_string, "Gestownik")


if __name__ == '__main__':
    config.read_config()

    server_thread.start()
    tray_icon_thread.start()
    time.sleep(2)
    if platform.system() == "Windows":
        display_config_notification()

    tray_icon_thread.join()
    rest_server.close()
    server_thread.join(timeout=10)
    print("exited")
