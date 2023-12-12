import platform
import threading
import time


import recognition
from recognition import recognition_thread_run
from steering import config
from steering.tray import display_config_notification
from steering.tray import tray_icon_thread

recognition_thread = threading.Thread(name="recognitionThread", target=lambda: recognition_thread_run())

if __name__ == '__main__':
    config.read_config()

    tray_icon_thread.start()
    recognition_thread.start()
    time.sleep(2)
    if platform.system() == "Windows":
        display_config_notification()

    tray_icon_thread.join()
    recognition.run_recognition_thread = False
    recognition_thread.join()
    print("exited")
    exit(0)
